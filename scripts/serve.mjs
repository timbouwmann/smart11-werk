import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// Serve from project root (one level up from scripts/)
const ROOT = path.join(__dirname, '..');
const PORT = 3000;

const MIME = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.mjs': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.mp4': 'video/mp4',
};

const server = http.createServer((req, res) => {
  // Strip query string before building file path
  const pathname = new URL(req.url, 'http://localhost').pathname;
  let decodedPath;
  try {
    decodedPath = decodeURIComponent(pathname);
  } catch {
    res.writeHead(400);
    res.end('Bad request');
    return;
  }
  let filePath = path.resolve(ROOT, '.' + (decodedPath === '/' ? '/index.html' : decodedPath));

  // Block requests outside the project root and to hidden files/folders (.env, .git, ...)
  const relative = path.relative(ROOT, filePath);
  const isOutsideRoot = relative.startsWith('..') || path.isAbsolute(relative);
  const isHidden = relative.split(path.sep).some(part => part.startsWith('.'));
  if (isOutsideRoot || isHidden) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }

  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    filePath = path.join(ROOT, 'index.html');
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
});

// Only accept connections from this computer, not from the rest of the network
server.listen(PORT, '127.0.0.1', () => {
  console.log(`Server draait op http://localhost:${PORT}`);
});
