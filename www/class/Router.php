<?php

declare(strict_types=1);

namespace Eufrosina;

final class Router
{
    /** @var list<array{method: string, pattern: string, handler: callable}> */
    private array $routes = [];

    public function __construct(
        private readonly Request $request,
        private readonly View $view,
    ) {
    }

    public function get(string $path, callable $handler): void
    {
        $this->add('GET', $path, $handler);
    }

    public function post(string $path, callable $handler): void
    {
        $this->add('POST', $path, $handler);
    }

    public function delete(string $path, callable $handler): void
    {
        $this->add('DELETE', $path, $handler);
    }

    private function add(string $method, string $path, callable $handler): void
    {
        $pattern = preg_replace('/\{([a-zA-Z0-9_]+)\}/', '(?P<$1>[^/]+)', $path);
        $this->routes[] = [
            'method' => $method,
            'pattern' => '#^' . $pattern . '$#',
            'handler' => $handler,
        ];
    }

    public function dispatch(): void
    {
        $method = $this->request->method();
        $uri = $this->request->path();

        foreach ($this->routes as $route) {
            if ($route['method'] !== $method) {
                continue;
            }

            if (!preg_match($route['pattern'], $uri, $matches)) {
                continue;
            }

            $params = array_filter($matches, 'is_string', ARRAY_FILTER_USE_KEY);
            $result = call_user_func(
                $route['handler'],
                $params,
                $this->request->isHtmx()
            );

            if (is_array($result)) {
                [$viewPath, $data] = $result;
                $this->view->render($viewPath, $data ?? []);
            }

            return;
        }

        http_response_code(404);
        $this->view->render('404', [
            'title' => 'No encontrada · Eufrosina',
            'section' => '',
        ]);
    }
}
