// Simple test to verify Vercel deployment configuration
console.log('Testing Vercel deployment configuration...');

// Check if required files exist
const fs = require('fs');
const path = require('path');

const requiredFiles = [
  'package.json',
  'vite.config.ts',
  'index.html',
  'src/main.tsx',
  'src/App.tsx'
];

console.log('Checking for required files:');
requiredFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file} - Found`);
  } else {
    console.log(`❌ ${file} - Missing`);
  }
});

// Check vercel.json configuration
const vercelConfigPath = path.join(__dirname, 'vercel.json');
if (fs.existsSync(vercelConfigPath)) {
  try {
    const vercelConfig = JSON.parse(fs.readFileSync(vercelConfigPath, 'utf8'));
    console.log('✅ vercel.json - Found and valid JSON');
    
    // Check if it's configured for static build
    if (vercelConfig.builds && vercelConfig.builds[0].use === '@vercel/static-build') {
      console.log('✅ vercel.json - Correctly configured for static build');
    } else {
      console.log('⚠️ vercel.json - May need adjustment for static build');
    }
  } catch (e) {
    console.log('❌ vercel.json - Invalid JSON');
  }
} else {
  console.log('❌ vercel.json - Missing');
}

console.log('\nVercel deployment test completed.');