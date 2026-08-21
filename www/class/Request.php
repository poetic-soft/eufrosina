<?php

declare(strict_types=1);

namespace Eufrosina;

final class Request
{
    public function method(): string
    {
        return strtoupper($_SERVER['REQUEST_METHOD'] ?? 'GET');
    }

    public function path(): string
    {
        $uri = $_SERVER['REQUEST_URI'] ?? '/';
        $path = parse_url($uri, PHP_URL_PATH);

        if (!is_string($path) || $path === '') {
            return '/';
        }

        return rtrim($path, '/') ?: '/';
    }

    public function isHtmx(): bool
    {
        return isset($_SERVER['HTTP_HX_REQUEST'])
            && $_SERVER['HTTP_HX_REQUEST'] === 'true';
    }

    public function hxTarget(): ?string
    {
        return $this->header('HX-Target');
    }

    public function header(string $name, ?string $default = null): ?string
    {
        $key = 'HTTP_' . strtoupper(str_replace('-', '_', $name));

        return isset($_SERVER[$key]) ? (string) $_SERVER[$key] : $default;
    }
}
