const { chromium } = require('playwright');
(async () => {
  const file = process.argv[2], out = process.argv[3];
  const browser = await chromium.launch();
  const html = require('fs').readFileSync(file, 'utf8');
  const wrap = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body style="margin:0">' + html + '</body></html>';
  for (const [name, w] of [['desktop', 1200], ['mobile', 400]]) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.setContent(wrap, { waitUntil: 'networkidle' });
    await page.screenshot({ path: `${out}_${name}.png`, fullPage: true });
    await page.close();
  }
  const page = await browser.newPage();
  await page.setContent(wrap, { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: `${out}.pdf`, format: 'A4', printBackground: true, margin: { top: '14mm', bottom: '14mm', left: '12mm', right: '12mm' } });
  await browser.close();
  console.log('done');
})().catch(e => { console.error(e); process.exit(1); });
