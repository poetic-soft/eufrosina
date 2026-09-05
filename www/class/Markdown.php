<?php

declare(strict_types=1);

namespace Eufrosina;

final class Markdown
{
    /**
     * @return array{meta: array<string, string>, body: string}
     */
    public static function split(string $raw): array
    {
        $raw = self::normalize($raw);

        if (!str_starts_with($raw, "---\n")) {
            return ['meta' => [], 'body' => $raw];
        }

        $end = strpos($raw, "\n---", 4);
        if ($end === false) {
            return ['meta' => [], 'body' => $raw];
        }

        $yaml = substr($raw, 4, $end - 4);
        $body = ltrim(substr($raw, $end + 4), "\r\n");

        return [
            'meta' => self::parseFrontMatter($yaml),
            'body' => $body,
        ];
    }

    /**
     * @return array<string, string>
     */
    private static function parseFrontMatter(string $yaml): array
    {
        $meta = [];

        foreach (explode("\n", $yaml) as $line) {
            $line = trim($line);
            if ($line === '' || !str_contains($line, ':')) {
                continue;
            }

            [$key, $value] = explode(':', $line, 2);
            $key = trim($key);
            $value = trim($value);

            if ($key !== '') {
                $meta[$key] = $value;
            }
        }

        return $meta;
    }

    public static function titleFromBody(string $body): ?string
    {
        if (preg_match('/^#\s+(.+)$/m', $body, $matches) === 1) {
            return trim($matches[1]);
        }

        foreach (explode("\n", $body) as $line) {
            $line = trim($line);
            if ($line !== '') {
                return $line;
            }
        }

        return null;
    }

    public static function excerpt(string $body, int $limit = 220): string
    {
        $plain = preg_replace('/^#\s+.+$/m', '', $body, 1) ?? $body;
        $plain = preg_replace('/^#+\s+/m', '', $plain) ?? $plain;
        $plain = preg_replace('/\*\*(.+?)\*\*/s', '$1', $plain) ?? $plain;
        $plain = preg_replace('/\s+/', ' ', $plain) ?? $plain;
        $plain = trim($plain);

        if ($plain === '') {
            return '';
        }

        if (mb_strlen($plain) <= $limit) {
            return $plain;
        }

        $cut = mb_substr($plain, 0, $limit);
        $space = mb_strrpos($cut, ' ');

        if ($space !== false && $space > 80) {
            $cut = mb_substr($cut, 0, $space);
        }

        return rtrim($cut, '.,;: ') . '…';
    }

    public static function toHtml(string $body): string
    {
        $body = self::normalize($body);
        $escaped = htmlspecialchars($body, ENT_QUOTES, 'UTF-8');

        $escaped = preg_replace('/^###\s+(.+)$/m', '<h3>$1</h3>', $escaped) ?? $escaped;
        $escaped = preg_replace('/^##\s+(.+)$/m', '<h2>$1</h2>', $escaped) ?? $escaped;
        $escaped = preg_replace('/^#\s+(.+)$/m', '<h1>$1</h1>', $escaped) ?? $escaped;
        $escaped = preg_replace('/\*\*(.+?)\*\*/s', '<strong>$1</strong>', $escaped) ?? $escaped;
        $escaped = preg_replace(
            '/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/',
            '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>',
            $escaped
        ) ?? $escaped;

        $blocks = preg_split('/\n{2,}/', trim($escaped)) ?: [];
        $html = '';

        foreach ($blocks as $block) {
            $block = trim($block);
            if ($block === '') {
                continue;
            }

            if (preg_match('/^<h[1-3]>/', $block) === 1) {
                if (preg_match('/^(<h[1-3]>.*<\/h[1-3]>)(?:\n([\s\S]+))?$/', $block, $parts) === 1) {
                    $html .= $parts[1];
                    if (!empty($parts[2])) {
                        $html .= '<p>' . nl2br(trim($parts[2]), false) . '</p>';
                    }
                    continue;
                }

                $html .= $block;
                continue;
            }

            $html .= '<p>' . nl2br($block, false) . '</p>';
        }

        return $html;
    }

    private static function normalize(string $text): string
    {
        $text = str_replace(["\r\n", "\r"], "\n", $text);

        return $text;
    }
}
