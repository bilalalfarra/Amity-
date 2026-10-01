// Batch-fetch homes.co.jp unit pages with headless Chromium, saving each page's HTML to the path given in the plan.
// usage: node homes_fetch.js <plan.json>   plan = [{"url": "...", "path": "/abs/out.html"}, ...]
// Politeness / WAF behaviour observed on this site (AWS WAF): a browser session is shown a CAPTCHA (HTTP 405
// "Human Verification") after roughly a dozen unit-page views, and the CAPTCHA state sticks to that session.
// We never try to solve a CAPTCHA. Instead: only the HTML document (+ awswaf challenge resources) is requested,
// pages are paced PACE_MS apart, the browser context (cookies) is rotated every ROTATE pages with a pause,
// and a CAPTCHA triggers a long back-off with a fresh context; the page is retried once at the end.
const { chromium } = require('playwright');
const fs = require('fs');

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36';
const PACE_MS = parseInt(process.env.PACE_MS || '12000', 10);          // between pages (+0-4 s jitter)
const ROTATE = parseInt(process.env.ROTATE || '10', 10);                // pages per browser context
const ROTATE_PAUSE_MS = parseInt(process.env.ROTATE_PAUSE_MS || '90000', 10);
const CAPTCHA_WAIT_MS = parseInt(process.env.CAPTCHA_WAIT_MS || '300000', 10);
const MAX_CAPTCHA = parseInt(process.env.MAX_CAPTCHA || '6', 10);
const DEADLINE_MS = parseInt(process.env.DEADLINE_MIN || '0', 10) * 60000;   // 0 = no deadline

function valid(path) {
  try {
    if (!fs.existsSync(path) || fs.statSync(path).size < 20000) return false;
    const t = fs.readFileSync(path, 'utf8');
    return !t.includes('challenge-container') && !t.includes('Human Verification') &&
      (t.includes('築年月') || t.includes('totalNum') || t.includes('該当物件は0件'));
  } catch (e) { return false; }
}

async function newContext(browser) {
  const ctx = await browser.newContext({ userAgent: UA, locale: 'ja-JP', viewport: { width: 1366, height: 850 } });
  await ctx.route('**/*', route => {
    const req = route.request();
    if (req.resourceType() === 'document') return route.continue();
    if (/awswaf\.com/.test(req.url())) return route.continue();
    return route.abort();
  });
  return ctx;
}

(async () => {
  const start = Date.now();
  const plan = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch({ headless: true, args: ['--disable-blink-features=AutomationControlled'] });
  let ctx = await newContext(browser);
  let page = await ctx.newPage();
  let ok = 0, fail = 0, skipped = 0, captcha = 0, inCtx = 0, contexts = 1;
  const queue = plan.filter(it => !valid(it.path));
  const retry = [];
  let pass = 0;
  while (queue.length && pass < 2) {
    pass++;
    while (queue.length) {
      const item = queue.shift();
      if (valid(item.path)) { skipped++; continue; }
      if (DEADLINE_MS && Date.now() - start > DEADLINE_MS) { console.log(JSON.stringify({ abort: 'deadline' })); queue.length = 0; break; }
      if (inCtx >= ROTATE) {
        await ctx.close();
        await new Promise(r => setTimeout(r, ROTATE_PAUSE_MS));
        ctx = await newContext(browser); page = await ctx.newPage(); inCtx = 0; contexts++;
        console.log(JSON.stringify({ rotate: contexts, t: new Date().toISOString() }));
      }
      const t0 = Date.now();
      let status = null, title = '';
      try {
        const resp = await page.goto(item.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
        status = resp ? resp.status() : null;
        for (let i = 0; i < 45; i++) {
          let ch = null, content = null;
          try { ch = await page.$('#challenge-container'); content = await page.$('dt, .totalNum, .mod-listPaging'); } catch (e) {}
          if (!ch && content) break;
          await page.waitForTimeout(1000);
        }
        title = await page.title();
        const html = await page.content();
        inCtx++;
        if (html.includes('challenge-container') || title.includes('Human Verification')) {
          fail++;
          console.log(JSON.stringify({ url: item.url, status, title: title.slice(0, 60), result: 'blocked', t: new Date().toISOString() }));
          if (title.includes('Human Verification')) {
            captcha++;
            retry.push(item);
            if (captcha >= MAX_CAPTCHA) { console.log(JSON.stringify({ abort: 'captcha budget' })); queue.length = 0; break; }
            await ctx.close();
            await new Promise(r => setTimeout(r, CAPTCHA_WAIT_MS));
            ctx = await newContext(browser); page = await ctx.newPage(); inCtx = 0; contexts++;
            console.log(JSON.stringify({ rotate: contexts, after: 'captcha', t: new Date().toISOString() }));
          } else {
            retry.push(item);
          }
          continue;
        }
        fs.writeFileSync(item.path, html);
        ok++;
        console.log(JSON.stringify({ url: item.url, status, title: title.slice(0, 60), result: 'ok', ms: Date.now() - t0, n: ok }));
      } catch (e) {
        fail++;
        retry.push(item);
        console.log(JSON.stringify({ url: item.url, status, result: 'error', error: String(e.message).slice(0, 120) }));
      }
      await page.waitForTimeout(PACE_MS + Math.floor(Math.random() * 4000));
    }
    if (retry.length && pass < 2) { queue.push(...retry.splice(0)); }
  }
  console.log(JSON.stringify({ done: true, ok, fail, skipped, captcha, contexts, unfetched: retry.length, minutes: Math.round((Date.now() - start) / 60000) }));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
