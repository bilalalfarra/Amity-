// Playwright helper for athome: (mode=list) fetch missing ward list pages; (mode=verify) verify detail URLs of candidates.
const { chromium } = require('playwright');
const fs = require('fs');
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36';
const WARDS = ['kyoto_shimogyo-city','kyoto_nakagyo-city','kyoto_minami-city','kyoto_ukyo-city','kyoto_kamigyo-city','kyoto_nishikyo-city','kyoto_higashiyama-city','kyoto_kita-city','kyoto_fushimi-city'];
const RAW = 'out/raw/parking';
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function main() {
  const mode = process.argv[2];
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ userAgent: UA, locale: 'ja-JP', viewport: { width: 1366, height: 900 } });
  const page = await ctx.newPage();
  await page.route('**/*', route => { const t = route.request().resourceType(); if (['image', 'media', 'font'].includes(t)) return route.abort(); return route.continue(); });
  async function load(url) {
    for (let a = 0; a < 4; a++) {
      let resp;
      try { resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }); } catch (e) { console.log('nav error', e.message.slice(0, 80)); await sleep(5000); continue; }
      let html = await page.content();
      if (!html.includes('認証中')) return { status: resp.status(), html };
      await page.waitForTimeout(6000 + 6000 * a);
      html = await page.content();
      if (!html.includes('認証中')) return { status: resp.status(), html };
      console.log('challenge persists', a, url);
      await sleep(10000);
    }
    return { status: 'challenge', html: null };
  }
  if (mode === 'list') {
    for (const slug of WARDS) {
      const base = `https://www.athome.co.jp/rent_parking/kyoto/${slug}/list/`;
      const f1 = `${RAW}/athome_${slug}_p1.html`;
      let h1 = fs.existsSync(f1) ? fs.readFileSync(f1, 'utf8') : '';
      if (!h1.includes('serverApp-state')) { const r = await load(base); if (r.html) { fs.writeFileSync(f1, r.html); h1 = r.html; } await sleep(1500); }
      const m = h1.match(/bukkenCount(?:&q;|\\?")\s*:\s*(\d+)/); const total = m ? parseInt(m[1]) : 0; const pages = Math.ceil(total / 30);
      console.log(slug, 'total', total, 'pages', pages);
      for (let p = 2; p <= pages; p++) {
        const fn = `${RAW}/athome_${slug}_p${p}.html`;
        if (fs.existsSync(fn) && fs.readFileSync(fn, 'utf8').includes('serverApp-state')) continue;
        const r = await load(`${base}page${p}/`);
        console.log(' page', p, r.status, r.html ? r.html.length : 0);
        if (r.html && r.html.includes('serverApp-state')) fs.writeFileSync(fn, r.html);
        await sleep(1500);
      }
    }
  } else if (mode === 'verify') {
    const cand = JSON.parse(fs.readFileSync('out/athome_list.json', 'utf8')).filter(r => r.distance_km !== null && r.distance_km <= 5.5);
    const sf = 'out/athome_detail_status.json';
    const status = fs.existsSync(sf) ? JSON.parse(fs.readFileSync(sf, 'utf8')) : {};
    let i = 0;
    for (const r of cand) {
      i++;
      if (status[r.url] === 200) continue;
      const res = await load(r.url);
      let code = res.status;
      if (res.html) {
        if (/物件が見つかりません|掲載を終了|お探しのページ/.test(res.html) && !res.html.includes('serverApp-state')) code = 'gone';
        if (i <= 2) fs.writeFileSync(`${RAW}/athome_detail/${r.id}.html`, res.html);
      }
      status[r.url] = code;
      if (i % 10 === 0) { fs.writeFileSync(sf, JSON.stringify(status)); console.log('verify', i, '/', cand.length, 'last', code); }
      await sleep(1500);
    }
    fs.writeFileSync(sf, JSON.stringify(status));
    const dist = {}; for (const v of Object.values(status)) dist[v] = (dist[v] || 0) + 1;
    console.log('VERIFY DONE', JSON.stringify(dist));
  }
  await browser.close();
}
main().catch(e => { console.error('FATAL', e); process.exit(1); });
