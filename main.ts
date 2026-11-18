import * as fs from 'node:fs';
import * as path from 'node:path';
import * as process from 'node:process';

const __dirname = path.dirname(new URL(import.meta.url).pathname);
const srcPath = path.join(__dirname, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';

fs.mkdirSync(outDir, { recursive: true });

const destPath = path.join(outDir, 'entry.png');
const data = fs.readFileSync(srcPath);
fs.writeFileSync(destPath, data);

const stats = fs.statSync(destPath);
console.log(`Output path: ${destPath}`);
console.log(`File size: ${stats.size} bytes`);
