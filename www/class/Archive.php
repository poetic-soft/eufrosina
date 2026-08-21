<?php

declare(strict_types=1);

namespace Eufrosina;

final class Archive
{
    public const COLLECTIONS = ['escritos', 'diario'];

    public function __construct(
        private readonly string $piezasPath,
        private readonly Cache $cache,
    ) {
    }

    /**
     * @return list<Piece>
     */
    public function list(string $coleccion): array
    {
        $this->assertCollection($coleccion);

        return $this->scan($coleccion, $this->piezasPath . '/' . $coleccion);
    }

    public function get(string $coleccion, string $slug): ?Piece
    {
        if (!$this->isSlug($slug)) {
            return null;
        }

        foreach ($this->list($coleccion) as $piece) {
            if ($piece->slug === $slug) {
                return $piece;
            }
        }

        return null;
    }

    public function html(Piece $piece, string $version): string
    {
        if (!$piece->has($version)) {
            throw new \RuntimeException("Version not found: {$version}");
        }

        $path = $piece->versions[$version];
        $mtime = filemtime($path);
        $stamp = $mtime === false ? '0' : (string) $mtime;

        return $this->cache->remember(
            'archive.html.' . $piece->coleccion . '.' . $piece->slug . '.' . $version . '.' . $stamp,
            0,
            static function () use ($path): string {
                $raw = file_get_contents($path);
                if ($raw === false) {
                    return '';
                }

                $split = Markdown::split($raw);

                return Markdown::toHtml($split['body']);
            }
        );
    }

    public function count(string $coleccion): int
    {
        return count($this->list($coleccion));
    }

    /**
     * @return list<Piece>
     */
    private function scan(string $coleccion, string $directory): array
    {
        if (!is_dir($directory)) {
            return [];
        }

        $pieces = [];

        $entries = scandir($directory);
        if ($entries === false) {
            return [];
        }

        foreach ($entries as $entry) {
            if ($entry === '.' || $entry === '..') {
                continue;
            }

            $path = $directory . '/' . $entry;
            if (!is_dir($path) || !$this->isSlug($entry)) {
                continue;
            }

            $piece = $this->load($coleccion, $entry, $path);
            if ($piece !== null) {
                $pieces[] = $piece;
            }
        }

        usort($pieces, static function (Piece $a, Piece $b): int {
            return $a->orden <=> $b->orden ?: strnatcmp($a->slug, $b->slug);
        });

        return $pieces;
    }

    private function load(string $coleccion, string $slug, string $directory): ?Piece
    {
        $versions = [];

        foreach (Piece::VERSIONS as $version) {
            $file = $directory . '/' . $version . '.md';
            if (is_file($file)) {
                $versions[$version] = $file;
            }
        }

        if ($versions === []) {
            return null;
        }

        $preferred = $versions['corregido'] ?? $versions['original'] ?? $versions['limpia'];
        $raw = file_get_contents($preferred);
        if ($raw === false) {
            return null;
        }

        $split = Markdown::split($raw);
        $meta = $split['meta'];
        $title = Markdown::titleFromBody($split['body']) ?? $slug;
        $orden = isset($meta['orden']) && is_numeric($meta['orden']) ? (int) $meta['orden'] : 0;

        return new Piece(
            coleccion: $coleccion,
            slug: $slug,
            orden: $orden,
            title: $title,
            excerpt: Markdown::excerpt($split['body']),
            versions: $versions,
            imagen: $this->resolveImage($directory, $meta['imagen'] ?? null),
            directory: $directory,
        );
    }

    private function resolveImage(string $directory, ?string $fromMeta): ?string
    {
        $candidates = [];

        if ($fromMeta !== null && $this->isSafeImageName($fromMeta)) {
            $candidates[] = $fromMeta;
        }

        $candidates[] = 'imagen.jpg';

        foreach (array_unique($candidates) as $name) {
            if (is_file($directory . '/' . $name)) {
                return $name;
            }
        }

        return null;
    }

    public function isSafeImageName(string $name): bool
    {
        return preg_match('/^[a-zA-Z0-9._-]+\.(jpe?g|png|webp|gif)$/i', $name) === 1
            && !str_contains($name, '..');
    }

    private function assertCollection(string $coleccion): void
    {
        if (!in_array($coleccion, self::COLLECTIONS, true)) {
            throw new \InvalidArgumentException("Unknown collection: {$coleccion}");
        }
    }

    private function isSlug(string $slug): bool
    {
        return preg_match('/^[a-z0-9]+(?:-[a-z0-9]+)*$/', $slug) === 1;
    }
}
