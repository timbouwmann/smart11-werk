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
  const s = `C:\\Users\\Game pc\\.cache\\puppeteer\\chrome-headless-shell\\win64-146.0.7680.153\\chrome-headless-shell-win64\\chrome-headless-shell.exe`;
  if (fs.existsSync(s)) chromePath = s;
}

const browser = await puppeteer.launch({
  headless: true,
  executablePath: chromePath,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
});
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1.5 });

async function shot(label) {
  await page.evaluate(() => document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible')));
  await new Promise(r => setTimeout(r, 500));
  const p = nextPath(label);
  await page.screenshot({ path: p, fullPage: true });
  console.log(`✓ ${label} → ${path.basename(p)}`);
}

await page.goto('http://localhost:3000/smartcoach-lead.html', { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise(r => setTimeout(r, 2000));
await shot('01-landing');

// Click "Gebruik demo"
await page.evaluate(() => {
  const btn = [...document.querySelectorAll('button')].find(b => b.textContent.trim().startsWith('Gebruik demo'));
  if (btn) btn.click();
});
await new Promise(r => setTimeout(r, 1200));
await shot('02-demo-moment1');

// Click correct option moment 1
await page.evaluate(() => {
  const btn = [...document.querySelectorAll('button')].find(b => b.textContent.includes('dribbelt terwijl'));
  if (btn) btn.click();
});
await new Promise(r => setTimeout(r, 700));
await shot('03-demo-moment1-antwoord');

// Next
await page.evaluate(() => {
  const btn = [...document.querySelectorAll('button')].find(b => b.textContent.includes('Volgende moment'));
  if (btn) btn.click();
});
await new Promise(r => setTimeout(r, 1000));
await shot('04-demo-moment2');

// Correct option moment 2 + next
await page.evaluate(() => {
  const btn = [...document.querySelectorAll('button')].find(b => b.textContent.includes('tussen de linies'));
  if (btn) btn.click();
});
await new Promise(r => setTimeout(r, 500));
await page.evaluate(() => {
  const btn = [...document.querySelectorAll('button')].find(b => b.textContent.includes('Volgende moment'));
  if (btn) btn.click();
});
await new Promise(r => setTimeout(r, 1000));
await shot('05-demo-moment3');

// Correct option moment 3
await page.evaluate(() => {
  const btn = [...document.querySelectorAll('button')].find(b => b.textContent.includes('terugkerend patroon'));
  if (btn) btn.click();
});
await new Promise(r => setTimeout(r, 700));
await shot('06-demo-moment3-antwoord');

// Bekijk trainingsplan
await page.evaluate(() => {
  const btn = [...document.querySelectorAll('button')].find(b => b.textContent.includes('trainingsplan'));
  if (btn) btn.click();
});
await new Promise(r => setTimeout(r, 1500));
await shot('07-resultaten');

await browser.close();
console.log('\nKlaar!');
