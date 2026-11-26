// Entrypoint for the news-image bounty: hand the judge exactly the PNG that
// render.py drew. The guardrails below fail loudly instead of shipping a
// truncated or oversized image, and keep the run deterministic (one read, one
// write, no clock or network access).

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

const MAX_BYTES = 1024 * 1024;
const MAX_SIDE = 1024;
const PNG_SIGNATURE = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

const bytes = readFileSync(source);
if (bytes.length < 1024) {
  throw new Error('entry.png is implausibly small; the poster was not rendered');
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes; the gate allows ${MAX_BYTES}`);
}
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is not a PNG');
}

// IHDR is the first chunk: 4-byte length, "IHDR", width, height, then depth.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width}x${height}; the side limit is ${MAX_SIDE}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const written = statSync(target).size;
if (written !== bytes.length) {
  throw new Error(`copy is ${written} bytes, source is ${bytes.length}`);
}
console.log(`entry.png ${width}x${height}, ${written} bytes -> ${target}`);
