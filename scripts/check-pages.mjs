import puppeteer from 'puppeteer';
import fs from 'fs';

const chromePath = `C:\\Users\\Game pc\\.cache\\puppeteer\\chrome-headless-shell\\win64-146.0.7680.153\\chrome-headless-shell-win64\\chrome-headless-shell.exe`;
const screenshotsDir = './scripts/temporary screenshots';

const browser = await puppeteer.launch({
  headless: true,
  executablePath: chromePath,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

const page = await browser.newPage();
await page.setViewport({ width: 1000, height: 1300, deviceScaleFactor: 1.5 });
await page.goto('http://localhost:3000/Smart11/html_pages/ebook-smart11-base-activatiegids.html', { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise(r => setTimeout(r, 1500));

// Check overflow on each page
const info = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('.page')).map((el, i) => ({
    page: i + 1,
    offsetHeight: el.offsetHeight,
    scrollHeight: el.scrollHeight,
    overflow: el.scrollHeight > el.offsetHeight ? 'OVERFLOW!' : 'OK',
  }));
});

console.log('Page overflow check:');
info.forEach(p => console.log(`  Page ${p.page}: height=${p.offsetHeight}px scrollHeight=${p.scrollHeight}px → ${p.overflow}`));

// Screenshot each page individually
const pageCount = await page.evaluate(() => document.querySelectorAll('.page').length);
for (let i = 0; i < pageCount; i++) {
  const clip = await page.evaluate((idx) => {
    const el = document.querySelectorAll('.page')[idx];
    const rect = el.getBoundingClientRect();
    return {
      x: Math.max(0, rect.left),
      y: rect.top + window.scrollY,
      width: rect.width,
      height: rect.height,
    };
  }, i);

  await page.screenshot({
    path: `${screenshotsDir}/page-${i + 1}-check.png`,
    clip: {
      x: clip.x,
      y: clip.y,
      width: clip.width,
      height: clip.height,
    },
  });
  console.log(`  Screenshot saved: page-${i + 1}-check.png`);
}

await browser.close();
