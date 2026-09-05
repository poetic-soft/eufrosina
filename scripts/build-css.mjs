import * as sass from 'sass';
import { copyFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { basename, dirname, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const src = resolve(root, 'src/scss/main.scss');
const outCss = resolve(root, 'www/assets/css/main.css');
const outMap = `${outCss}.map`;
const cssDir = dirname(outCss);
const fontDst = resolve(root, 'www/assets/fonts');
const fontFiles = [
  // Alegreya (body)
  'alegreya-latin-ext-400-normal.woff2',
  'alegreya-latin-400-normal.woff2',
  'alegreya-latin-ext-400-italic.woff2',
  'alegreya-latin-400-italic.woff2',
  'alegreya-latin-ext-500-normal.woff2',
  'alegreya-latin-500-normal.woff2',
  'alegreya-latin-ext-700-normal.woff2',
  'alegreya-latin-700-normal.woff2',
  // Cormorant Garamond Light (titles)
  'cormorant-garamond-latin-ext-300-italic.woff2',
  'cormorant-garamond-latin-300-italic.woff2',
  'cormorant-garamond-latin-ext-300-normal.woff2',
  'cormorant-garamond-latin-300-normal.woff2',
];

const fontSources = [
  resolve(root, 'node_modules/@fontsource/alegreya/files'),
  resolve(root, 'node_modules/@fontsource/cormorant-garamond/files'),
];

mkdirSync(fontDst, { recursive: true });
for (const file of fontFiles) {
  const from = fontSources
    .map((dir) => resolve(dir, file))
    .find((path) => {
      try {
        copyFileSync(path, resolve(fontDst, file));
        return true;
      } catch {
        return false;
      }
    });
  if (!from) {
    throw new Error(`Fuente no encontrada: ${file}`);
  }
}

const result = sass.compile(src, {
  style: 'expanded',
  sourceMap: true,
  sourceMapIncludeSources: true,
});

const map = result.sourceMap;
map.file = basename(outCss);
map.sources = map.sources.map((source) => {
  if (source.startsWith('file:')) {
    return relative(cssDir, fileURLToPath(source)).replaceAll('\\', '/');
  }

  return source;
});

mkdirSync(cssDir, { recursive: true });
writeFileSync(
  outCss,
  `${result.css}\n/*# sourceMappingURL=${basename(outMap)} */\n`,
);
writeFileSync(outMap, JSON.stringify(map));
console.log(outCss);
console.log(outMap);
