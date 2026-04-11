import puppeteer from 'puppeteer';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const chromePath = `C:\\Users\\Game pc\\.cache\\puppeteer\\chrome-headless-shell\\win64-146.0.7680.153\\chrome-headless-shell-win64\\chrome-headless-shell.exe`;
const outputPath = path.join(__dirname, '..', 'Smart11', 'html_pages', 'level-courses.pdf');

const browser = await puppeteer.launch({
  headless: true,
  executablePath: chromePath,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

const page = await browser.newPage();
await page.goto('http://localhost:3000/Smart11/html_pages/level-courses.html', {
  waitUntil: 'networkidle0',
  timeout: 30000,
});
await new Promise(r => setTimeout(r, 2500));

await page.pdf({
  path: outputPath,
  format: 'A4',
  printBackground: true,
  margin: { top: 0, right: 0, bottom: 0, left: 0 },
});

await browser.close();
console.log(`PDF opgeslagen: ${outputPath}`);
