import * as fs from 'node:fs';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const sourcePath = path.join(__dirname, 'entry.png');
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const destPath = path.join(outputDir, 'entry.png');

fs.mkdirSync(outputDir, { recursive: true });
fs.copyFileSync(sourcePath, destPath);

const stats = fs.statSync(destPath);
console.log(`Output path: ${destPath}`);
console.log(`File size: ${stats.size} bytes`);
