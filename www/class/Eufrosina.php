<?php

declare(strict_types=1);

namespace Eufrosina;

final class Eufrosina
{
    private Request $request;
    private Cache $cache;
    private View $view;
    private Router $router;
    private Archive $archive;
    private Namesakes $namesakes;
    private Media $media;
    private string $basePath;

    private function __construct(string $basePath)
    {
        $this->basePath = $basePath;
        $this->request = new Request();
        $this->cache = new Cache($basePath . '/storage/cache');
        $this->archive = new Archive($basePath . '/piezas', $this->cache);
        $this->namesakes = new Namesakes($basePath . '/eufrosinas', $this->cache);
        $this->media = new Media($basePath . '/assets');
        $this->view = new View(
            $this->request,
            $basePath . '/views',
            cssHref: self::assetHref($basePath, '/assets/css/main.css'),
            jsHref: self::assetHref($basePath, '/assets/js/gallery.js'),
        );
        $this->router = new Router($this->request, $this->view);
        $this->registerRoutes();
    }

    public static function boot(?string $basePath = null): self
    {
        return new self($basePath ?? dirname(__DIR__));
    }

    public function run(): void
    {
        $this->router->dispatch();
    }

    public function cache(): Cache
    {
        return $this->cache;
    }

    public function request(): Request
    {
        return $this->request;
    }

    private static function assetHref(string $basePath, string $href): string
    {
        $file = $basePath . $href;

        if (is_file($file)) {
            $href .= '?v=' . filemtime($file);
        }

        return $href;
    }

    private function registerRoutes(): void
    {
        $this->router->get('/', function () {
            return ['home', [
                'title' => 'Eufrosina',
                'section' => 'home',
                'nEscritos' => $this->archive->count('escritos'),
                'nDiario' => $this->archive->count('diario'),
                'nEufrosinas' => $this->namesakes->count(),
                'heroImages' => $this->media->hero(),
                'galleries' => $this->media->galleries(),
            ]];
        });

        $this->router->get('/escritos', function () {
            return $this->lista(
                'escritos',
                'Escritos',
                'Viajes, clase, asociaciones de mujeres y cartas: los papeles que Eufrosina fue dejando a lo largo de los años.'
            );
        });

        $this->router->get('/diario', function () {
            return $this->lista(
                'diario',
                'Diario',
                'Notas de Torrelobatón y Valladolid: el calor, la lluvia, el patio y los días del pueblo.'
            );
        });

        $this->router->get('/eufrosinas', function () {
            return ['eufrosinas', [
                'title' => 'Eufrosinas · Eufrosina',
                'section' => 'eufrosinas',
                'introHtml' => $this->namesakes->introHtml(),
                'nombres' => $this->namesakes->list(),
            ]];
        });

        $this->router->get('/escritos/{slug}', function (array $params) {
            return $this->pieza('escritos', $params['slug']);
        });

        $this->router->get('/escritos/{slug}/media/{file}', function (array $params) {
            $this->serveImage('escritos', $params['slug'], $params['file']);
        });

        $this->router->get('/escritos/{slug}/{version}', function (array $params) {
            return $this->pieza('escritos', $params['slug'], $params['version']);
        });

        $this->router->get('/diario/{slug}', function (array $params) {
            return $this->pieza('diario', $params['slug']);
        });

        $this->router->get('/diario/{slug}/media/{file}', function (array $params) {
            $this->serveImage('diario', $params['slug'], $params['file']);
        });

        $this->router->get('/diario/{slug}/{version}', function (array $params) {
            return $this->pieza('diario', $params['slug'], $params['version']);
        });

        $this->router->get('/eufrosinas/{slug}/media/{file}', function (array $params) {
            $this->serveNamesakeImage($params['slug'], $params['file']);
        });

        $this->router->get('/eufrosinas/{slug}', function (array $params) {
            return $this->namesake($params['slug']);
        });

        $this->router->get('/diagnostics', function () {
            return ['diagnostics', [
                'title' => 'Diagnóstico de cache',
                'section' => '',
                'diagnostics' => $this->cache->diagnostics(),
            ]];
        });

        $this->router->get('/diagnostics/probe', function () {
            return ['partials/cache-status', [
                'title' => 'Diagnóstico de cache',
                'section' => '',
                'diagnostics' => $this->cache->diagnostics(),
            ]];
        });
    }

    /**
     * @return array{0: string, 1: array<string, mixed>}
     */
    private function lista(string $coleccion, string $heading, string $lede): array
    {
        return ['lista', [
            'title' => $heading . ' · Eufrosina',
            'section' => $coleccion,
            'coleccion' => $coleccion,
            'heading' => $heading,
            'lede' => $lede,
            'piezas' => $this->archive->list($coleccion),
        ]];
    }

    /**
     * @return array{0: string, 1: array<string, mixed>}
     */
    private function pieza(string $coleccion, string $slug, ?string $version = null): array
    {
        $piece = $this->archive->get($coleccion, $slug);

        if ($piece === null) {
            http_response_code(404);

            return ['404', [
                'title' => 'No encontrada · Eufrosina',
                'section' => $coleccion,
            ]];
        }

        $version = $version ?? $piece->defaultVersion();

        if (!in_array($version, Piece::VERSIONS, true) || !$piece->has($version)) {
            http_response_code(404);

            return ['404', [
                'title' => 'No encontrada · Eufrosina',
                'section' => $coleccion,
            ]];
        }

        return ['pieza', [
            'title' => $piece->title . ' · Eufrosina',
            'section' => $coleccion,
            'pieza' => $piece,
            'version' => $version,
            'cuerpo' => $this->archive->html($piece, $version),
        ]];
    }

    /**
     * @return array{0: string, 1: array<string, mixed>}
     */
    private function namesake(string $slug): array
    {
        $item = $this->namesakes->get($slug);

        if ($item === null) {
            http_response_code(404);

            return ['404', [
                'title' => 'No encontrada · Eufrosina',
                'section' => 'eufrosinas',
            ]];
        }

        return ['eufrosina', [
            'title' => $item->title . ' · Eufrosinas',
            'section' => 'eufrosinas',
            'nombre' => $item,
            'cuerpo' => $this->namesakes->html($item),
        ]];
    }

    private function serveImage(string $coleccion, string $slug, string $file): void
    {
        if (!$this->archive->isSafeImageName($file)) {
            http_response_code(404);
            return;
        }

        $piece = $this->archive->get($coleccion, $slug);
        if ($piece === null) {
            http_response_code(404);
            return;
        }

        $this->sendFile($piece->directory, $file);
    }

    private function serveNamesakeImage(string $slug, string $file): void
    {
        if (!$this->namesakes->isSafeImageName($file)) {
            http_response_code(404);
            return;
        }

        $item = $this->namesakes->get($slug);
        if ($item === null) {
            http_response_code(404);
            return;
        }

        $this->sendFile($item->directory, $file);
    }

    private function sendFile(string $directory, string $file): void
    {
        $root = realpath($directory);
        $path = realpath($directory . DIRECTORY_SEPARATOR . $file);

        if ($root === false || $path === false || !str_starts_with($path, $root . DIRECTORY_SEPARATOR) || !is_file($path)) {
            http_response_code(404);
            return;
        }

        $mime = match (strtolower(pathinfo($file, PATHINFO_EXTENSION))) {
            'jpg', 'jpeg' => 'image/jpeg',
            'png' => 'image/png',
            'webp' => 'image/webp',
            'gif' => 'image/gif',
            default => 'application/octet-stream',
        };

        $mtime = filemtime($path) ?: time();
        header('Content-Type: ' . $mime);
        header('Content-Length: ' . (string) filesize($path));
        header('Last-Modified: ' . gmdate('D, d M Y H:i:s', $mtime) . ' GMT');
        header('Cache-Control: public, max-age=86400');
        readfile($path);
    }
}
