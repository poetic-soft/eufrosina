Quiero montar una web basada en htmx en front y puro PHP en server

Combinar htmx y PHP puro es una arquitectura ligera y eficiente: htmx reemplaza la complejidad de JS en el cliente haciendo peticiones AJAX mediante atributos HTML, mientras que PHP se encarga de procesar la lógica y devolver únicamente los fragmentos de HTML que deben actualizarse en el DOM.

1. Detección de Peticiones htmx

Cuando htmx hace un intercambio, incluye la cabecera HTTP HX-Request: true. Puedes crear un helper básico para saber si debes renderizar el layout completo o solo un componente HTML:

PHP
function is_htmx(): bool {
    return isset($_SERVER['HTTP_HX_REQUEST']) && $_SERVER['HTTP_HX_REQUEST'] === 'true';
}
2. Flujo de Renderizado (Layout vs. Fragmento)

El patrón fundamental consiste en bifurcar la respuesta del servidor según el tipo de petición:

PHP
// index.php
$route = strtok($_SERVER['REQUEST_URI'], '?');

if ($route === '/items') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $item = $_POST['item_name'] ?? '';
        
        // Guardar en BD...

        // Si la petición viene de htmx, devolvemos solo el fragmento
        if (is_htmx()) {
            include __DIR__ . '/partials/item-row.php';
            exit;
        }
    }
}

// Petición normal de navegador: carga la página completa
include __DIR__ . '/views/full-page.php';
3. Ejemplo Práctico: Inserción Dinámica sin JS Adicional

Página Completa (views/full-page.php):

HTML
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PHP + htmx</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
</head>
<body>
    <h1>Lista de Elementos</h1>

    <!-- Intercepta el submit, hace POST vía AJAX e inyecta la respuesta al final del <ul> -->
    <form hx-post="/items" hx-target="#item-list" hx-swap="beforeend">
        <input type="text" name="item_name" required>
        <button type="submit">Añadir</button>
    </form>

    <ul id="item-list">
        <!-- Los elementos se irán insertando aquí -->
    </ul>
</body>
</html>
Fragmento Reutilizable (partials/item-row.php):

PHP
<li>
    <?= htmlspecialchars($item) ?>
    <button 
        hx-delete="/items/<?= $id ?>" 
        hx-target="closest li" 
        hx-swap="outerHTML">
        Eliminar
    </button>
</li>
4. Patrones y Cabeceras Útiles en PHP

Enviar Eventos al Frontend: Usa la cabecera HX-Trigger para que htmx dispare eventos JS personalizados en el cliente sin devolver código JS:

PHP
header('HX-Trigger: itemAdded');
Redirección desde Servidor: Para redirigir la página completa desde una respuesta htmx:

PHP
header('HX-Redirect: /dashboard');
exit;
Protección CSRF Global: Adjunta el token CSRF en el <body> para que htmx lo incluya automáticamente en todas las peticiones POST/PUT/DELETE:

HTML
<body hx-headers='{"X-CSRF-Token": "<?= $_SESSION['csrf_token'] ?>"}'>
¿Quieres ver un ejemplo de enrutador ligero en un solo archivo para organizar las rutas de este stack?

Sí
Y cómo se.puede implementar una cache en server para no tener que procesar el mismo fragmento en cada request

Para cachear fragmentos de HTML en PHP puro sin sobrecargar la aplicación, el método más directo utiliza Output Buffering junto a un almacenamiento en disco o en memoria (APCu).

1. Helper de Cache por Output Buffering (Archivo o APCu)

Este patrón evalúa si el fragmento existe y sigue vigente. Si expiró, ejecuta el código, captura el HTML con ob_start() y lo almacena.

PHP
function render_cache(string $key, int $ttl_seconds, callable $callback): string {
    // Opción con APCu (memoria RAM):
    if (function_exists('apcu_fetch')) {
        $cached = apcu_fetch($key);
        if ($cached !== false) return $cached;

        ob_start();
        $callback();
        $html = ob_get_clean();

        apcu_store($key, $html, $ttl_seconds);
        return $html;
    }

    // Opción de reserva en disco (sys_get_temp_dir):
    $filepath = sys_get_temp_dir() . '/frag_' . md5($key) . '.html';
    
    if (file_exists($filepath) && (time() - filemtime($filepath)) < $ttl_seconds) {
        return file_get_contents($filepath);
    }

    ob_start();
    $callback();
    $html = ob_get_clean();

    file_put_contents($filepath, $html, LOCK_EX);
    return $html;
}
2. Uso en el Endpoint para htmx

En lugar de consultar la base de datos y renderizar en cada petición AJAX, envuelves la generación del parcial en el helper:

PHP
// /partials/stats.php
if (is_htmx()) {
    $category = $_GET['cat'] ?? 'general';
    $cache_key = "stats_fragment_" . $category;

    // Devuelve el HTML directamente desde la cache si no ha pasado 1 hora (3600s)
    echo render_cache($cache_key, 3600, function() use ($category) {
        // Consultas pesadas a BD o cálculos extensos...
        $data = get_heavy_stats_from_db($category);
        
        include __DIR__ . '/views/stats-card.php';
    });
    exit;
}
3. Cache a Nivel de Cabeceras HTTP (ETag / 304 Not Modified)

Si el fragmento no cambia con frecuencia, puedes ahorrar ancho de banda indicándole a htmx que use su propia cache local con la cabecera ETag:

PHP
$html = render_cache($key, 3600, $render_function);
$etag = md5($html);

header("ETag: \"$etag\"");

if (isset($_SERVER['HTTP_IF_NONE_MATCH']) && trim($_SERVER['HTTP_IF_NONE_MATCH'], '"') === $etag) {
    http_response_code(304); // Not Modified
    exit;
}

echo $html;
4. Estrategias de Invalidación

Por Clave Dinámica: Incluye la versión de los datos o timestamp en la clave ("user_profile_{$user_id}_{$user_updated_at}"). Al cambiar los datos, la clave cambia automáticamente y regenera la cache.

Borrado Manual: Al ejecutar una acción mutable (POST/PUT/DELETE), elimina la clave guardada:

PHP
// Tras actualizar el elemento en BD
apcu_delete("stats_fragment_general");
// O en disco: @unlink(sys_get_temp_dir() . '/frag_' . md5("stats_fragment_general") . '.html');
¿Quieres ver cómo gestionar la invalidación de cache mediante eventos con la cabecera HX-Trigger?

Sí
Apcu

APCu (Alternative PHP User Cache) es una extensión en memoria compartida (RAM) integrada directamente dentro de los procesos de PHP. Al no requerir conexiones TCP/sockets como Redis o Memcached, es la opción de mayor rendimiento para cachear arrays, objetos o fragmentos HTML renderizados localmente en un solo servidor.

Configuración recomendada (php.ini)

Para asegurar un rendimiento óptimo sin consumir RAM en exceso:

Ini, TOML
extension=apcu.so

apc.enabled=1
apc.shm_size=64M        ; Memoria asignada (ajustar según volumen)
apc.ttl=3600            ; Tiempo de vida por defecto para claves sin TTL explícito
apc.enable_cli=0        ; Desactivar en CLI salvo que ejecutes tests/scripts
Operaciones Principales (API de APCu)

Función	Propósito	Ejemplo
apcu_store($key, $var, $ttl)	Guarda un valor en RAM. Devuelve true/false.	apcu_store('menu_html', $html, 300);
apcu_fetch($key)	Recupera el valor. Devuelve false si no existe o expiró.	$html = apcu_fetch('menu_html');
apcu_exists($key)	Comprueba la existencia sin extraer los datos.	if (apcu_exists('menu_html')) { ... }
apcu_delete($key)	Invalida/elimina una clave explícitamente.	apcu_delete('menu_html');
apcu_clear_cache()	Limpia toda la memoria cacheada.	apcu_clear_cache();
Ejemplo de Abstracción para Fragmentos HTML

PHP
function apcu_remember(string $key, int $ttl, callable $callback): string {
    $cached = apcu_fetch($key);
    if ($cached !== false) {
        return $cached;
    }

    // Captura la salida del búfer
    ob_start();
    $callback();
    $html = ob_get_clean();

    apcu_store($key, $html, $ttl);
    return $html;
}

// Uso directo en endpoint/controlador:
$html = apcu_remember("user_card_{$userId}", 600, function() use ($userId) {
    $user = db_find_user($userId);
    include __DIR__ . '/partials/user-card.php';
});
Ventajas vs. Limitaciones

Velocidad Extrema: Acceso directo a RAM sin latencia de red ni serialización compleja.

Simplicidad: Cero dependencias externas o servicios adicionales corriendo en el sistema.

Memoria Compartida por Nodo: Si usas un entorno multiseridor (vARIOS VPS tras un balanceador de carga), APCu no comparte la memoria entre servidores. Para arquitecturas distribuidas de gran escala, Redis es la alternativa adecuada.

¿Quieres ver un panel de control mínimo en PHP para inspeccionar el estado de APCu?

Sí
Mi server es compartido tendr apcu?

En un hosting compartido por defecto suele estar desactivado, pero en la mayoría de los proveedores modernos con cPanel o Plesk puedes activarlo tú mismo con un clic.

1. Cómo comprobar si está activo

Sube un archivo temporal (ej. check_apcu.php) a tu servidor para verificar la disponibilidad:

PHP
<?php
if (extension_loaded('apcu') && function_exists('apcu_enabled') && apcu_enabled()) {
    echo "APCu está disponible y activo.";
} else {
    echo "APCu NO está instalado o está desactivado.";
}
2. Cómo activarlo desde el panel de control

En cPanel (CloudLinux): Busca Seleccionar Versión de PHP (Select PHP Version) -> ve a la pestaña Extensiones (Extensions) -> marca la casilla apcu.

En Plesk: Ve a Ajustes de PHP (PHP Settings) de tu dominio -> busca la lista de módulos y activa apcu.

Atención en Hosting Compartido: Aunque actives APCu, algunos hosting compartidos aíslan la memoria RAM por usuario mediante CloudLinux/LVE y borran la cache de APCu si el proceso de PHP se reinicia por falta de uso o límite de memoria.

3. Alternativa robusta para Hosting Compartido: Cache en Disco

Si no tienes acceso a APCu o el servidor reinicia los procesos PHP constantemente, la alternativa más rápida en servidores compartidos modernos (que utilizan discos NVMe/SSD) es la cache en archivos local. Tiene un rendimiento casi idéntico para el volumen de un hosting compartido:

PHP
function file_remember(string $key, int $ttl, callable $callback): string {
    $cache_dir = __DIR__ . '/../cache_storage';
    if (!is_dir($cache_dir)) {
        mkdir($cache_dir, 0750, true);
    }

    $filepath = $cache_dir . '/' . md5($key) . '.html';

    // Si el archivo existe y no ha expirado, devolverlo
    if (file_exists($filepath) && (time() - filemtime($filepath)) < $ttl) {
        return file_get_contents($filepath);
    }

    // Si expiró o no existe, generar el fragmento
    ob_start();
    $callback();
    $html = ob_get_clean();

    // Guardar en disco de forma segura (LOCK_EX evita colisiones de escritura)
    file_put_contents($filepath, $html, LOCK_EX);

    return $html;
}
¿Quieres una función para limpiar automáticamente los archivos caducados del disco?

Sí
Muéstrame una plantilla de enrutador ligero en PHP puro optimizada para trabajar con peticiones htmx.

Este enrutador de un solo archivo utiliza expresiones regulares para capturar parámetros dinámicos (como /items/{id}) y automatiza la inserción del layout según se trate de una petición navegación estándar o una interacción por htmx.

1. El Enrutador (Router.php)

PHP
<?php

class Router {
    private array $routes = [];

    public function get(string $path, callable $handler): void {
        $this->add('GET', $path, $handler);
    }

    public function post(string $path, callable $handler): void {
        $this->add('POST', $path, $handler);
    }

    public function delete(string $path, callable $handler): void {
        $this->add('DELETE', $path, $handler);
    }

    private function add(string $method, string $path, callable $handler): void {
        // Convierte /items/{id} en regex
        $pattern = preg_replace('/\{([a-zA-Z0-9_]+)\}/', '(?P<$1>[^/]+)', $path);
        $this->routes[] = [
            'method'  => $method,
            'pattern' => "#^" . $pattern . "$#",
            'handler' => $handler
        ];
    }

    public function isHtmx(): bool {
        return isset($_SERVER['HTTP_HX_REQUEST']) && $_SERVER['HTTP_HX_REQUEST'] === 'true';
    }

    public function dispatch(): void {
        $method = $_SERVER['REQUEST_METHOD'];
        $uri    = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

        foreach ($this->routes as $route) {
            if ($route['method'] === $method && preg_match($route['pattern'], $uri, $matches)) {
                // Filtra solo los parámetros con nombre
                $params = array_filter($matches, 'is_string', ARRAY_FILTER_USE_KEY);
                
                // Ejecuta el controlador
                $result = call_user_func($route['handler'], $params, $this->isHtmx());
                
                if (is_array($result)) {
                    [$viewPath, $data] = $result;
                    $this->render($viewPath, $data ?? []);
                }
                return;
            }
        }

        // Manejo de 404
        http_response_code(404);
        echo $this->isHtmx() 
            ? '<div class="error">Recurso no encontrado</div>' 
            : '<h1>404 - Página no encontrada</h1>';
    }

    private function render(string $viewPath, array $data): void {
        extract($data);

        // Petición htmx: renderizar únicamente la vista parcial
        if ($this->isHtmx()) {
            include $viewPath;
            return;
        }

        // Petición normal de navegador: envolver la vista dentro del layout global
        ob_start();
        include $viewPath;
        $content = ob_get_clean();

        include __DIR__ . '/views/layout.php';
    }
}
2. Punto de Entrada (index.php)

PHP
<?php

require_once __DIR__ . '/Router.php';

$router = new Router();

// Ruta de página principal
$router->get('/', function() {
    return [__DIR__ . '/views/home.php', ['title' => 'Inicio']];
});

// Endpoint para htmx: devuelve únicamente la fila generada
$router->post('/items', function($params, $isHtmx) {
    $newItem = $_POST['name'] ?? 'Elemento sin nombre';
    
    // Guardar en base de datos...
    
    return [__DIR__ . '/views/partials/item-row.php', ['item' => $newItem]];
});

// Ruta con parámetros URL
$router->delete('/items/{id}', function($params, $isHtmx) {
    $id = $params['id'];
    
    // Borrar de base de datos...

    // Si htmx espera eliminar el elemento del DOM (hx-swap="outerHTML"), devolvemos cadena vacía
    if ($isHtmx) {
        echo "";
        return;
    }
    
    header('Location: /');
});

$router->dispatch();
3. La Estructura del Layout (views/layout.php)

PHP
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title><?= $title ?? 'Mi App htmx' ?></title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
</head>
<body>
    <nav>
        <a href="/">Inicio</a>
    </nav>

    <main id="main-content">
        <!-- Inyección automática del contenido de la vista en peticiones no-htmx -->
        <?= $content ?>
    </main>
</body>
</html>