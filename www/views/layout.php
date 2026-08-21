<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($title ?? 'Eufrosina', ENT_QUOTES, 'UTF-8') ?></title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Alegreya:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="<?= htmlspecialchars($cssHref ?? '/assets/css/main.css', ENT_QUOTES, 'UTF-8') ?>">
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
</head>
<body
    hx-boost="true"
    hx-target="#page"
    hx-swap="innerHTML"
    hx-push-url="true">
    <div id="page">
        <?= $content ?>
    </div>
</body>
</html>
