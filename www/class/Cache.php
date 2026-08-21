<?php

declare(strict_types=1);

namespace Eufrosina;

final class Cache
{
    public function __construct(
        private readonly string $directory,
    ) {
        if (!is_dir($this->directory) && !mkdir($this->directory, 0750, true) && !is_dir($this->directory)) {
            throw new \RuntimeException("Unable to create cache directory: {$this->directory}");
        }
    }

    public function remember(string $key, int $ttl, callable $callback): mixed
    {
        $cached = $this->get($key);
        if ($cached !== null) {
            return $cached;
        }

        $value = $callback();
        $this->set($key, $value, $ttl);

        return $value;
    }

    public function forget(string $key): bool
    {
        return $this->delete($key);
    }

    public function directory(): string
    {
        return $this->directory;
    }

    /**
     * @return array<string, mixed>
     */
    public function diagnostics(): array
    {
        $probeKey = 'eufrosina_probe_' . bin2hex(random_bytes(4));
        $probeValue = 'ok-' . time();
        $writeOk = $this->set($probeKey, $probeValue, 30);
        $readOk = $this->get($probeKey) === $probeValue;
        $this->delete($probeKey);

        return [
            'php_version' => PHP_VERSION,
            'probe_write_ok' => $writeOk,
            'probe_read_ok' => $readOk,
            'file_cache_path' => $this->directory,
            'file_cache_writable' => is_dir($this->directory) && is_writable($this->directory),
        ];
    }

    private function get(string $key): mixed
    {
        $path = $this->path($key);

        if (!is_file($path)) {
            return null;
        }

        $raw = file_get_contents($path);
        if ($raw === false) {
            return null;
        }

        $payload = unserialize($raw, ['allowed_classes' => false]);
        if (!is_array($payload) || !isset($payload['expires'], $payload['value'])) {
            @unlink($path);
            return null;
        }

        if ($payload['expires'] !== 0 && $payload['expires'] < time()) {
            @unlink($path);
            return null;
        }

        return $payload['value'];
    }

    private function set(string $key, mixed $value, int $ttl): bool
    {
        $payload = serialize([
            'expires' => $ttl > 0 ? time() + $ttl : 0,
            'value' => $value,
        ]);

        return file_put_contents($this->path($key), $payload, LOCK_EX) !== false;
    }

    private function delete(string $key): bool
    {
        $path = $this->path($key);

        if (!is_file($path)) {
            return true;
        }

        return @unlink($path);
    }

    private function path(string $key): string
    {
        return $this->directory . '/' . md5($key) . '.cache';
    }
}
