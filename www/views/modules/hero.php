<?php
/**
 * @var string $archivo Archivo en /assets/images/hero/
 * @var list<array{src: string, filename: string, width: int, height: int, alt: string}> $images
 */

$archivo = (string) ($archivo ?? '');
$images = $images ?? [];
$image = null;

if ($archivo !== '') {
    foreach ($images as $candidate) {
        if ($candidate['filename'] === $archivo) {
            $image = $candidate;
            break;
        }
    }
}
?>
<header class="hero<?= $image === null ? ' hero--plain' : '' ?>">
    <?php if ($image !== null): ?>
        <img
            class="hero__bg"
            src="<?= htmlspecialchars($image['src'], ENT_QUOTES, 'UTF-8') ?>"
            alt="<?= htmlspecialchars($image['alt'], ENT_QUOTES, 'UTF-8') ?>"
            <?php if ($image['width'] > 0 && $image['height'] > 0): ?>
                width="<?= (int) $image['width'] ?>"
                height="<?= (int) $image['height'] ?>"
            <?php endif; ?>
            fetchpriority="high"
            decoding="async"
        >
    <?php endif; ?>

    <div class="hero__copy">
        <h1>Eufrosina Pérez Tera</h1>
        <p class="lede">Noventa y cinco años. Valladolid y Torrelobatón.</p>
    </div>
</header>
