<?php

declare(strict_types=1);

namespace Eufrosina;

final class Namesakes
{
    public function __construct(
        private readonly string $rootPath,
        private readonly Cache $cache,
    ) {
    }

    public function introHtml(): string
    {
        $path = $this->rootPath . '/nombre.md';
        if (!is_file($path)) {
            return '';
        }

        $mtime = filemtime($path);
        $stamp = $mtime === false ? '0' : (string) $mtime;

        return $this->cache->remember(
            'namesakes.intro.' . $stamp,
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

    /**
     * @return list<Namesake>
     */
    public function list(): array
    {
        $directory = $this->rootPath . '/lista';
        if (!is_dir($directory)) {
            return [];
        }

        $items = [];
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

            $item = $this->load($entry, $path);
            if ($item !== null) {
                $items[] = $item;
            }
        }

        usort($items, static function (Namesake $a, Namesake $b): int {
            return $a->orden <=> $b->orden ?: strnatcmp($a->slug, $b->slug);
        });

        return $items;
    }

    public function get(string $slug): ?Namesake
    {
        if (!$this->isSlug($slug)) {
            return null;
        }

        foreach ($this->list() as $item) {
            if ($item->slug === $slug) {
                return $item;
            }
        }

        return null;
    }

    public function html(Namesake $item): string
    {
        $mtime = filemtime($item->path);
        $stamp = $mtime === false ? '0' : (string) $mtime;

        return $this->cache->remember(
            'namesakes.html.' . $item->slug . '.' . $stamp,
            0,
            static function () use ($item): string {
                $raw = file_get_contents($item->path);
                if ($raw === false) {
                    return '';
                }

                $split = Markdown::split($raw);

                return Markdown::toHtml($split['body']);
            }
        );
    }

    public function count(): int
    {
        return count($this->list());
    }

    public function isSafeImageName(string $name): bool
    {
        return preg_match('/^[a-zA-Z0-9._-]+\.(jpe?g|png|webp|gif)$/i', $name) === 1
            && !str_contains($name, '..');
    }

    private function load(string $slug, string $directory): ?Namesake
    {
        $path = $directory . '/entrada.md';
        if (!is_file($path)) {
            return null;
        }

        $raw = file_get_contents($path);
        if ($raw === false) {
            return null;
        }

        $split = Markdown::split($raw);
        $meta = $split['meta'];
        $title = $meta['titulo'] ?? Markdown::titleFromBody($split['body']) ?? $slug;
        $epoca = $meta['epoca'] ?? '';
        $orden = isset($meta['orden']) && is_numeric($meta['orden']) ? (int) $meta['orden'] : 0;

        return new Namesake(
            slug: $slug,
            orden: $orden,
            title: $title,
            epoca: $epoca,
            excerpt: $epoca !== '' ? $epoca : Markdown::excerpt($split['body'], 160),
            path: $path,
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

    private function isSlug(string $slug): bool
    {
        return preg_match('/^[a-z0-9]+(?:-[a-z0-9]+)*$/', $slug) === 1;
    }
}
