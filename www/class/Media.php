<?php

declare(strict_types=1);

namespace Eufrosina;

final class Media
{
    private const HERO_ALTS = [
        'a.png' => 'Retrato de familia',
        'b.png' => 'Eufrosina en el jardín',
    ];

    public function __construct(private readonly string $assetsPath)
    {
    }

    /**
     * @return list<array{src: string, filename: string, width: int, height: int, alt: string}>
     */
    public function hero(): array
    {
        return $this->scanImages(
            $this->assetsPath . '/images/hero',
            '/assets/images/hero',
            self::HERO_ALTS
        );
    }

    /**
     * @return list<array{slug: string, titulo: string, images: list<array{src: string, filename: string, width: int, height: int, alt: string}>}>
     */
    public function galleries(): array
    {
        $root = $this->assetsPath . '/images/galleries';
        if (!is_dir($root)) {
            return [];
        }

        $entries = scandir($root);
        if ($entries === false) {
            return [];
        }

        $series = [];

        foreach ($entries as $entry) {
            if ($entry === '.' || $entry === '..') {
                continue;
            }

            $directory = $root . '/' . $entry;
            if (!is_dir($directory) || !$this->isSlug($entry)) {
                continue;
            }

            $images = $this->scanImages(
                $directory,
                '/assets/images/galleries/' . rawurlencode($entry),
                []
            );

            if ($images === []) {
                continue;
            }

            $series[] = [
                'slug' => $entry,
                'titulo' => $this->seriesTitle($directory),
                'images' => $images,
            ];
        }

        usort($series, static function (array $a, array $b): int {
            return strnatcmp($a['slug'], $b['slug']);
        });

        return $series;
    }

    /**
     * @param array<string, string> $alts
     * @return list<array{src: string, filename: string, width: int, height: int, alt: string}>
     */
    private function scanImages(string $directory, string $urlBase, array $alts): array
    {
        if (!is_dir($directory)) {
            return [];
        }

        $entries = scandir($directory);
        if ($entries === false) {
            return [];
        }

        $images = [];

        foreach ($entries as $entry) {
            if (!$this->isSafeImageName($entry)) {
                continue;
            }

            $path = $directory . '/' . $entry;
            if (!is_file($path)) {
                continue;
            }

            $size = getimagesize($path);
            $mtime = filemtime($path) ?: 0;
            $src = $urlBase . '/' . rawurlencode($entry);
            if ($mtime > 0) {
                $src .= '?v=' . $mtime;
            }

            $images[] = [
                'src' => $src,
                'filename' => $entry,
                'width' => $size !== false ? (int) $size[0] : 0,
                'height' => $size !== false ? (int) $size[1] : 0,
                'alt' => $alts[$entry] ?? '',
            ];
        }

        usort($images, static function (array $a, array $b): int {
            return strnatcmp($a['filename'], $b['filename']);
        });

        return $images;
    }

    private function seriesTitle(string $directory): string
    {
        $file = $directory . '/titulo.txt';
        if (!is_file($file)) {
            return '';
        }

        $raw = file_get_contents($file);
        if ($raw === false) {
            return '';
        }

        return trim($raw);
    }

    private function isSafeImageName(string $name): bool
    {
        return preg_match('/^[a-zA-Z0-9._-]+\.(jpe?g|png|webp|gif)$/i', $name) === 1
            && !str_contains($name, '..');
    }

    private function isSlug(string $slug): bool
    {
        return preg_match('/^[a-z0-9]+(?:-[a-z0-9]+)*$/', $slug) === 1;
    }
}
