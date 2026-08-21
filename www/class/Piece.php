<?php

declare(strict_types=1);

namespace Eufrosina;

final class Piece
{
    public const VERSIONS = ['limpia', 'original', 'corregido'];

    public const VERSION_LABELS = [
        'limpia' => 'Limpia',
        'original' => 'Original',
        'corregido' => 'Lectura',
    ];

    /**
     * @param array<string, string> $versions Map of version name => absolute file path
     */
    public function __construct(
        public readonly string $coleccion,
        public readonly string $slug,
        public readonly int $orden,
        public readonly string $title,
        public readonly string $excerpt,
        public readonly array $versions,
        public readonly ?string $imagen,
        public readonly string $directory,
    ) {
    }

    public function url(?string $version = null): string
    {
        $base = '/' . $this->coleccion . '/' . rawurlencode($this->slug);

        if ($version === null || $version === $this->defaultVersion()) {
            return $base;
        }

        return $base . '/' . rawurlencode($version);
    }

    public function imageUrl(): ?string
    {
        if ($this->imagen === null) {
            return null;
        }

        return '/' . $this->coleccion . '/' . rawurlencode($this->slug)
            . '/media/' . rawurlencode($this->imagen);
    }

    public function has(string $version): bool
    {
        return isset($this->versions[$version]);
    }

    public function defaultVersion(): string
    {
        foreach (['corregido', 'original', 'limpia'] as $version) {
            if ($this->has($version)) {
                return $version;
            }
        }

        return 'corregido';
    }

    /**
     * @return list<string>
     */
    public function availableVersions(): array
    {
        $found = [];

        foreach (self::VERSIONS as $version) {
            if ($this->has($version)) {
                $found[] = $version;
            }
        }

        return $found;
    }
}
