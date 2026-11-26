// Entrypoint for the 26 November 2026 news image: validate the drawn PNG,
// then copy those exact bytes to the output directory. Standard library only.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { crc32 } from 'node:zlib';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

const MAX_BYTES = 1048576;
const SIDE = 1024;
const PNG_SIGNATURE = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

if (!existsSync(source)) {
  throw new Error(`missing ${source}`);
}
const bytes = readFileSync(source);
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes; limit is ${MAX_BYTES}`);
}
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is not a PNG');
}

// IHDR is the first chunk: length(4), "IHDR", width(4), height(4), ...
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== SIDE || height !== SIDE) {
  throw new Error(`expected ${SIDE}x${SIDE}, got ${width}x${height}`);
}

// CRC covers the IHDR type plus its 13 data bytes (offsets 12..28).
const storedCrc = bytes.readUInt32BE(29);
if (crc32(bytes.subarray(12, 29)) !== storedCrc) {
  throw new Error('entry.png has a corrupt IHDR chunk');
}
const bitDepth = bytes[24];
const colorType = bytes[25];
if (bitDepth !== 8 || (colorType !== 2 && colorType !== 6)) {
  throw new Error(`unexpected PNG format: depth ${bitDepth}, color ${colorType}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
if (statSync(target).size !== bytes.length) {
  throw new Error('output copy differs in size from entry.png');
}
console.log(`entry.png ${width}x${height}, ${bytes.length} bytes -> ${target}`);
