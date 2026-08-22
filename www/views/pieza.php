<?php
/** @var Eufrosina\Piece $pieza */
/** @var string $version */
/** @var string $cuerpo */

$coleccionLabel = $pieza->coleccion === 'diario' ? 'Diario' : 'Escritos';
$backHref = '/' . htmlspecialchars($pieza->coleccion, ENT_QUOTES, 'UTF-8');
$backLabel = htmlspecialchars($coleccionLabel, ENT_QUOTES, 'UTF-8');
$showFoto = $version === 'original' && $pieza->imageUrl() !== null;
?>
<a class="back" href="<?= $backHref ?>">← <?= $backLabel ?></a>

<nav class="versions" aria-label="Versiones del texto">
    <?php foreach ($pieza->availableVersions() as $disponible): ?>
        <a
            href="<?= htmlspecialchars($pieza->url($disponible), ENT_QUOTES, 'UTF-8') ?>"
            <?php if ($disponible === $version): ?>aria-current="page"<?php endif; ?>
        ><?= htmlspecialchars(Eufrosina\Piece::VERSION_LABELS[$disponible], ENT_QUOTES, 'UTF-8') ?></a>
    <?php endforeach; ?>
</nav>

<?php if ($showFoto): ?>
<div class="pieza-layout">
<figure class="pieza-foto">
    <a
        href="<?= htmlspecialchars($pieza->imageUrl(), ENT_QUOTES, 'UTF-8') ?>"
        target="_blank"
        rel="noopener noreferrer"
        hx-boost="false"
        title="Abrir a tamaño completo"
    >
        <img
            src="<?= htmlspecialchars($pieza->imageUrl(), ENT_QUOTES, 'UTF-8') ?>"
            alt="Facsímil de <?= htmlspecialchars($pieza->title, ENT_QUOTES, 'UTF-8') ?>"
            width="374"
            height="512"
            decoding="async"
        >
    </a>
</figure>
<?php endif; ?>

<article class="cuerpo version-<?= htmlspecialchars($version, ENT_QUOTES, 'UTF-8') ?>">
    <?= $cuerpo ?>
</article>

<?php if ($showFoto): ?>
</div>
<?php endif; ?>

<a class="back" href="<?= $backHref ?>">← <?= $backLabel ?></a>
