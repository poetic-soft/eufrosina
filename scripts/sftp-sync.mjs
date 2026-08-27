import { existsSync, readFileSync, statSync } from 'node:fs';
import { dirname, posix, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import SftpClient from 'ssh2-sftp-client';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const configPath = resolve(root, '.vscode/sftp.json');

function loadConfig() {
  if (!existsSync(configPath)) {
    throw new Error(`No encuentro ${configPath}`);
  }

  const cfg = JSON.parse(readFileSync(configPath, 'utf8'));
  if (!cfg.host || !cfg.username || !cfg.remotePath) {
    throw new Error('sftp.json incompleto: hacen falta host, username y remotePath');
  }

  return cfg;
}

function toPosix(filePath) {
  return filePath.split(sep).join('/');
}

function relFromRoot(filePath) {
  return toPosix(relative(root, resolve(filePath)));
}

function shouldIgnore(rel) {
  const n = toPosix(rel);
  if (n.startsWith('..')) return true;
  if (n.startsWith('.vscode/') || n === '.vscode') return true;
  if (n.includes('/.git/') || n.startsWith('.git/') || n === '.git') return true;
  if (n.includes('node_modules/')) return true;
  if (n.startsWith('storage/cache/') && !n.endsWith('.gitkeep') && !n.endsWith('.htaccess')) {
    return true;
  }
  if (n === 'IDEA.md' || n.endsWith('/IDEA.md')) return true;
  if (n === 'composer.lock' || n.endsWith('/composer.lock')) return true;
  return false;
}

function shouldUpload(rel) {
  const n = toPosix(rel);
  if (shouldIgnore(n) || n === '' || n === '.') return false;
  return n === 'www' || n.startsWith('www/');
}

function remoteFor(rel, remotePath) {
  const base = String(remotePath).replace(/\/+$/, '');
  return `${base}/${toPosix(rel)}`;
}

async function connect(cfg) {
  const sftp = new SftpClient();
  await sftp.connect({
    host: cfg.host,
    port: Number(cfg.port) || 22,
    username: cfg.username,
    password: cfg.password,
    readyTimeout: 20000,
  });
  return sftp;
}

async function uploadFiles(sftp, cfg, files) {
  const uploaded = [];

  for (const file of files) {
    const abs = resolve(file);
    if (!existsSync(abs) || !statSync(abs).isFile()) continue;

    const rel = relFromRoot(abs);
    if (!shouldUpload(rel)) continue;

    const remote = remoteFor(rel, cfg.remotePath);
    await sftp.mkdir(posix.dirname(remote), true);
    await sftp.fastPut(abs, remote);
    uploaded.push(rel);
    console.log(`[sftp] ${rel}`);
  }

  return uploaded;
}

async function check(cfg) {
  const sftp = await connect(cfg);
  try {
    const cwd = await sftp.cwd();
    console.log(`[sftp] ok ${cfg.username}@${cfg.host}:${cfg.remotePath} (cwd ${cwd})`);
  } finally {
    await sftp.end();
  }
}

async function uploadOnce(cfg, files) {
  if (files.length === 0) return;
  const sftp = await connect(cfg);
  try {
    await uploadFiles(sftp, cfg, files);
  } finally {
    await sftp.end();
  }
}

async function watch(cfg) {
  const { default: chokidar } = await import('chokidar');
  const sftp = await connect(cfg);
  console.log(`[sftp] watching www → ${cfg.host}:${cfg.remotePath}`);

  let queue = new Set();
  let timer = null;
  let flushing = false;

  const flush = async () => {
    if (flushing) return;
    const batch = [...queue];
    queue.clear();
    if (batch.length === 0) return;
    flushing = true;
    try {
      await uploadFiles(sftp, cfg, batch);
    } catch (error) {
      console.error(`[sftp] ${error instanceof Error ? error.message : error}`);
    } finally {
      flushing = false;
      if (queue.size > 0) timer = setTimeout(flush, 200);
    }
  };

  const enqueue = (filePath) => {
    const rel = relFromRoot(filePath);
    if (!shouldUpload(rel)) return;
    queue.add(resolve(filePath));
    clearTimeout(timer);
    timer = setTimeout(flush, 400);
  };

  const watcher = chokidar.watch(resolve(root, 'www'), {
    ignoreInitial: true,
    awaitWriteFinish: { stabilityThreshold: 200, pollInterval: 50 },
    ignored: (filePath) => shouldIgnore(relFromRoot(filePath)),
  });

  watcher.on('add', enqueue);
  watcher.on('change', enqueue);

  const stop = async () => {
    clearTimeout(timer);
    await watcher.close();
    await sftp.end();
  };

  process.on('SIGINT', () => {
    stop().finally(() => process.exit(0));
  });
  process.on('SIGTERM', () => {
    stop().finally(() => process.exit(0));
  });
}

const args = process.argv.slice(2);
const cfg = loadConfig();

if (args.includes('--check')) {
  await check(cfg);
} else if (args.includes('--watch')) {
  await watch(cfg);
} else {
  await uploadOnce(cfg, args);
}
