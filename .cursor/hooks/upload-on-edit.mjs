import { spawnSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

function readStdin() {
  try {
    return readFileSync(0, 'utf8');
  } catch {
    return '';
  }
}

const raw = readStdin().trim();
if (raw === '') process.exit(0);

let payload;
try {
  payload = JSON.parse(raw);
} catch {
  process.exit(0);
}

const file = payload.file_path ?? payload.filePath ?? payload.path;
if (typeof file !== 'string' || file === '') process.exit(0);

const result = spawnSync(process.execPath, [resolve(root, 'scripts/sftp-sync.mjs'), file], {
  cwd: root,
  stdio: ['ignore', 'pipe', 'pipe'],
  windowsHide: true,
});

const out = `${result.stdout ?? ''}${result.stderr ?? ''}`.trim();
if (out) console.error(out);
process.exit(result.status === 0 ? 0 : 0);
