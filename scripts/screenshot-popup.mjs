import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dir = path.join(__dirname, 'temporary screenshots');

const chromePath = `C:\\Users\\Game pc\\.cache\\puppeteer\\chrome-headless-shell\\win64-146.0.7680.153\\chrome-headless-shell-win64\\chrome-headless-shell.exe`;

async function clickByText(page, text, exact = false) {
  await page.evaluate((txt, exact) => {
    const all = Array.from(document.querySelectorAll('button'));
    const btn = all.find(b => {
      const t = b.textContent.trim().replace(/\s+/g, ' ');
      return exact ? t === txt : (t.includes(txt) && !b.disabled);
    });
    if (btn) btn.click();
    else console.warn('Button not found:', txt);
  }, text, exact);
}

async function wait(ms) { return new Promise(r => setTimeout(r, ms)); }

const browser = await puppeteer.launch({
  headless: true,
  executablePath: chromePath,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 900, deviceScaleFactor: 1.5 });
await page.goto('http://localhost:3000/smartcoach-demo.html', { waitUntil: 'networkidle0' });
await wait(1500);

// 1. Open popup
await clickByText(page, 'Start demo-analyse');
await wait(900);
await page.screenshot({ path: path.join(dir, 'popup-A-intro.png') });
console.log('✓ A: intro');

// 2. Start demo (not "Start demo-analyse")
await page.evaluate(() => {
  const btns = Array.from(document.querySelectorAll('button'));
  const btn = btns.find(b => {
    const t = b.textContent.trim();
    return t.startsWith('Start demo') && !t.includes('analyse') && !b.disabled;
  });
  if (btn) btn.click();
});
await wait(700);
await page.screenshot({ path: path.join(dir, 'popup-B-vraag1.png') });
console.log('✓ B: vraag 1');

// 3. Select option A in moment 1
await page.evaluate(() => {
  const btns = Array.from(document.querySelectorAll('button'));
  // pick any non-disabled option card (not "Volgende" / "Start" / "X")
  const opt = btns.find(b => b.textContent.trim().length > 20 && b.textContent.trim().length < 120 && !b.disabled);
  if (opt) opt.click();
});
await wait(400);
await page.screenshot({ path: path.join(dir, 'popup-C-optie-gekozen.png') });
console.log('✓ C: optie gekozen');

// 4. Click Volgende
await clickByText(page, 'Volgende');
await wait(600);
await page.screenshot({ path: path.join(dir, 'popup-D-vraag2.png') });
console.log('✓ D: vraag 2');

// 5. Pick option for moment 2
await page.evaluate(() => {
  const btns = Array.from(document.querySelectorAll('button'));
  const opt = btns.find(b => b.textContent.trim().length > 20 && b.textContent.trim().length < 120 && !b.disabled);
  if (opt) opt.click();
});
await wait(300);
await clickByText(page, 'Volgende');
await wait(500);

// 6. Pick option for moment 3
await page.evaluate(() => {
  const btns = Array.from(document.querySelectorAll('button'));
  const opt = btns.find(b => b.textContent.trim().length > 20 && b.textContent.trim().length < 120 && !b.disabled);
  if (opt) opt.click();
});
await wait(300);
await clickByText(page, 'Bekijk resultaat');
await wait(800);

// 7. Result — scroll to top
await page.evaluate(() => {
  const s = document.querySelector('.scroll-inner');
  if (s) s.scrollTop = 0;
});
await wait(300);
await page.screenshot({ path: path.join(dir, 'popup-E-resultaat-top.png') });
console.log('✓ E: resultaat top');

// 8. Scroll to product cards
await page.evaluate(() => {
  const s = document.querySelector('.scroll-inner');
  if (s) s.scrollTop = s.scrollHeight;
});
await wait(400);
await page.screenshot({ path: path.join(dir, 'popup-F-product-cards.png') });
console.log('✓ F: product cards');

await browser.close();
console.log('\nKlaar.');
