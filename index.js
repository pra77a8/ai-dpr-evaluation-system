// This is a simple entry point for Vercel
// The actual app is built by Vite and served as static files

const { createServer } = require('http');
const { parse } = require('url');
const { join } = require('path');
const { existsSync } = require('fs');

const server = createServer((req, res) => {
  // Serve static files from dist directory
  const parsedUrl = parse(req.url, true);
  let pathname = parsedUrl.pathname;
  
  // Remove leading slash for file system path
  if (pathname === '/') {
    pathname = '/index.html';
  }
  
  const filePath = join(__dirname, 'dist', pathname);
  
  if (existsSync(filePath)) {
    // In a real implementation, you would serve the file content
    // For now, we'll just redirect to the main page
    res.writeHead(302, { Location: '/index.html' });
    res.end();
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not found');
  }
});

const port = process.env.PORT || 3000;
server.listen(port, () => {
  console.log(`Server running on port ${port}`);
});