<?php

declare(strict_types=1);

namespace Eufrosina;

final class Namesake
{
    public function __construct(
        public readonly string $slug,
        public readonly int $orden,
        public readonly string $title,
        public readonly string $epoca,
        public readonly string $excerpt,
        public readonly string $path,
        public readonly ?string $imagen,
        public readonly string $directory,
    ) {
    }

    public function url(): string
    {
        return '/eufrosinas/' . rawurlencode($this->slug);
    }

    public function imageUrl(): ?string
    {
        if ($this->imagen === null) {
            return null;
        }

        return '/eufrosinas/' . rawurlencode($this->slug)
            . '/media/' . rawurlencode($this->imagen);
    }
}
