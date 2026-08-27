<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="light dark">
    <meta name="theme-color" content="#e4e7e1" media="(prefers-color-scheme: light)">
    <meta name="theme-color" content="#1b201c" media="(prefers-color-scheme: dark)">
    <title><?= htmlspecialchars($title ?? 'Eufrosina', ENT_QUOTES, 'UTF-8') ?></title>
    <link rel="stylesheet" href="<?= htmlspecialchars($cssHref ?? '/assets/css/main.css', ENT_QUOTES, 'UTF-8') ?>">
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="<?= htmlspecialchars($jsHref ?? '/assets/js/gallery.js', ENT_QUOTES, 'UTF-8') ?>" defer></script>
</head>
<body
    hx-boost="true"
    hx-target="#page"
    hx-swap="innerHTML"
    hx-push-url="true">
    <a class="skip-link" href="#main-content">Saltar al contenido</a>
    <div id="page">
        <?= $content ?>
    </div>
</body>
</html>
