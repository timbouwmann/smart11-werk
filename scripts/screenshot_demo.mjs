import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const screenshotsDir = path.join(__dirname, 'temporary screenshots');
if (!fs.existsSync(screenshotsDir)) fs.mkdirSync(screenshotsDir, { recursive: true });

function nextPath(label) {
  const existing = fs.readdirSync(screenshotsDir)
    .filter(f => f.startsWith('screenshot-') && f.endsWith('.png'))
    .map(f => parseInt(f.match(/screenshot-(\d+)/)?.[1] || '0', 10))
    .filter(n => !isNaN(n));
  const n = existing.length > 0 ? Math.max(...existing) + 1 : 1;
  return path.join(screenshotsDir, `screenshot-${n}-${label}.png`);
}

let chromePath = process.env.PUPPETEER_EXECUTABLE_PATH;
if (!chromePath) {
  const headlessShell = `C:\\Users\\Game pc\\.cache\\puppeteer\\chrome-headless-shell\\win64-146.0.7680.153\\chrome-headless-shell-win64\\chrome-headless-shell.exe`;
  if (fs.existsSync(headlessShell)) chromePath = headlessShell;
}

const browser = await puppeteer.launch({
  headless: true,
  executablePath: chromePath,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});

const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1.5 });

async function shot(label) {
  await page.evaluate(() => {
    document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
  });
  await new Promise(r => setTimeout(r, 400));
  const p = nextPath(label);
  await page.screenshot({ path: p, fullPage: true });
  console.log(`Screenshot opgeslagen: ${p}`);
}

await page.goto('http://localhost:3000/smartcoach-demo.html', { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise(r => setTimeout(r, 1500));

// 1. Hero / landing
await shot('01-landing');

// 2. Click "Gebruik demo"
await page.click('button');
await new Promise(r => setTimeout(r, 1000));
await shot('02-demo-stap1');

// 3. Select option A on moment 1, screenshot after reveal
await page.evaluate(() => {
  const btns = document.querySelectorAll('button');
  for (const btn of btns) {
    if (btn.textContent.includes('terwijl een vrije')) { btn.click(); break; }
  }
});
await new Promise(r => setTimeout(r, 600));
await shot('03-demo-stap1-antwoord');

// 4. Click "Volgende moment"
await page.evaluate(() => {
  const btns = document.querySelectorAll('button');
  for (const btn of btns) {
    if (btn.textContent.includes('Volgende moment')) { btn.click(); break; }
  }
});
await new Promise(r => setTimeout(r, 800));
await shot('04-demo-stap2');

// 5. Select correct option on moment 2
await page.evaluate(() => {
  const btns = document.querySelectorAll('button');
  for (const btn of btns) {
    if (btn.textContent.includes('tussen de linies')) { btn.click(); break; }
  }
});
await new Promise(r => setTimeout(r, 600));

// 6. Click "Volgende moment"
await page.evaluate(() => {
  const btns = document.querySelectorAll('button');
  for (const btn of btns) {
    if (btn.textContent.includes('Volgende moment')) { btn.click(); break; }
  }
});
await new Promise(r => setTimeout(r, 800));
await shot('05-demo-stap3');

// 7. Select correct option on moment 3
await page.evaluate(() => {
  const btns = document.querySelectorAll('button');
  for (const btn of btns) {
    if (btn.textContent.includes('terugkerend patroon')) { btn.click(); break; }
  }
});
await new Promise(r => setTimeout(r, 600));
await shot('06-demo-stap3-antwoord');

// 8. Click "Bekijk mijn trainingsplan"
await page.evaluate(() => {
  const btns = document.querySelectorAll('button');
  for (const btn of btns) {
    if (btn.textContent.includes('Bekijk mijn trainingsplan')) { btn.click(); break; }
  }
});
await new Promise(r => setTimeout(r, 1200));
await shot('07-resultaten');

await browser.close();
console.log('\nKlaar — alle screenshots gemaakt.');
