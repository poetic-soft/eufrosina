<?php
/** @var string $title */
/** @var string $section */
/** @var string $content */
/** @var bool $isHtmx */
?>
<?php if (!empty($isHtmx)): ?>
<title><?= htmlspecialchars($title ?? 'Eufrosina', ENT_QUOTES, 'UTF-8') ?></title>
<?php endif; ?>
<div class="frame">
    <nav class="site-nav">
        <a class="brand" href="/">Eufrosina</a>
        <div class="nav-links">
            <a href="/" <?= ($section ?? '') === 'home' ? 'aria-current="page"' : '' ?>>Inicio</a>
            <a href="/escritos" <?= ($section ?? '') === 'escritos' ? 'aria-current="page"' : '' ?>>Escritos</a>
            <a href="/diario" <?= ($section ?? '') === 'diario' ? 'aria-current="page"' : '' ?>>Diario</a>
        </div>
    </nav>
    <main id="main-content">
        <?= $content ?>
    </main>
    <p class="site-foot">Papeles recogidos para ser leídos.</p>
</div>
