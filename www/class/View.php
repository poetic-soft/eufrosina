<?php

declare(strict_types=1);

namespace Eufrosina;

final class View
{
    public function __construct(
        private readonly Request $request,
        private readonly string $viewsPath,
        private readonly string $layout = 'layout.php',
        private readonly string $cssHref = '/assets/css/main.css',
    ) {
    }

    /**
     * @param array<string, mixed> $data
     */
    public function render(string $view, array $data = []): void
    {
        $viewPath = $this->resolve($view);
        $section = (string) ($data['section'] ?? '');
        $title = (string) ($data['title'] ?? 'Eufrosina');
        $cssHref = $this->cssHref;

        extract($data, EXTR_SKIP);

        ob_start();
        include $viewPath;
        $content = ob_get_clean();

        header('Vary: HX-Request, HX-Target');

        if ($this->request->isHtmx() && !$this->wrapsPage()) {
            echo $content;
            return;
        }

        $isHtmx = $this->request->isHtmx();

        ob_start();
        include $this->viewsPath . '/partials/page.php';
        $content = ob_get_clean();

        if ($this->request->isHtmx()) {
            echo $content;
            return;
        }

        include $this->viewsPath . '/' . $this->layout;
    }

    private function wrapsPage(): bool
    {
        $target = $this->request->hxTarget();

        if ($target === null || $target === '') {
            return true;
        }

        // htmx envía HX-Target con el id del elemento ("page"), no el selector ("#page").
        return ltrim($target, '#') === 'page';
    }

    /**
     * Render a partial without layout wrapping (even on full page requests).
     *
     * @param array<string, mixed> $data
     */
    public function partial(string $view, array $data = []): string
    {
        $viewPath = $this->resolve($view);
        extract($data, EXTR_SKIP);

        ob_start();
        include $viewPath;

        return (string) ob_get_clean();
    }

    private function resolve(string $view): string
    {
        if (str_ends_with($view, '.php')) {
            $path = $view;
        } else {
            $path = $this->viewsPath . '/' . ltrim($view, '/') . '.php';
        }

        if (!is_file($path)) {
            throw new \RuntimeException("View not found: {$path}");
        }

        return $path;
    }
}
