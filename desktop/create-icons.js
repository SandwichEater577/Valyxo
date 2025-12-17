const fs = require('fs');
const path = require('path');

const assetsDir = path.join(__dirname, 'assets');
if (!fs.existsSync(assetsDir)) {
  fs.mkdirSync(assetsDir, { recursive: true });
}

const pngBuffer = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==', 'base64');

fs.writeFileSync(path.join(assetsDir, 'icon.png'), pngBuffer);
fs.writeFileSync(path.join(assetsDir, 'icon-small.png'), pngBuffer);

console.log('✓ Created icon.png');
console.log('✓ Created icon-small.png');
