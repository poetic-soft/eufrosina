import * as sass from 'sass';
import { mkdirSync, writeFileSync } from 'node:fs';
import { basename, dirname, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const src = resolve(root, 'src/scss/main.scss');
const outCss = resolve(root, 'www/assets/css/main.css');
const outMap = `${outCss}.map`;
const cssDir = dirname(outCss);

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
