<?php
/**
 * @var string $galeria Carpeta en /assets/images/galleries/
 * @var list<array{slug: string, titulo: string, images: list<array{src: string, filename: string, width: int, height: int, alt: string}>}> $series
 */

$galeria = (string) ($galeria ?? '');
$series = $series ?? [];
$chosen = null;

if ($galeria !== '') {
    foreach ($series as $candidate) {
        if ($candidate['slug'] === $galeria) {
            $chosen = $candidate;
            break;
        }
    }
}

if ($chosen === null) {
    return;
}

$total = count($chosen['images']);
$trackId = 'gallery-' . $chosen['slug'];
$label = $chosen['titulo'] !== '' ? $chosen['titulo'] : 'Fotos';
?>
<section class="gallery" data-gallery aria-label="<?= htmlspecialchars($label, ENT_QUOTES, 'UTF-8') ?>">
    <?php if ($chosen['titulo'] !== ''): ?>
        <h2 class="gallery__title"><?= htmlspecialchars($chosen['titulo'], ENT_QUOTES, 'UTF-8') ?></h2>
    <?php endif; ?>

    <div class="gallery-frame">
        <div
            id="<?= htmlspecialchars($trackId, ENT_QUOTES, 'UTF-8') ?>"
            class="gallery-viewport"
            tabindex="0"
            data-gallery-viewport
        >
        <ul class="gallery-track">
            <?php foreach ($chosen['images'] as $index => $image): ?>
                <?php
                $nro = $index + 1;
                $slideLabel = $image['alt'] !== ''
                    ? $image['alt']
                    : 'Fotografía ' . $nro . ' de ' . $total . '. Abrir original';
                ?>
                <li class="gallery-slide">
                    <a
                        class="gallery-item"
                        href="<?= htmlspecialchars($image['src'], ENT_QUOTES, 'UTF-8') ?>"
                        hx-boost="false"
                        target="_blank"
                        rel="noopener noreferrer"
                        aria-label="<?= htmlspecialchars($slideLabel, ENT_QUOTES, 'UTF-8') ?>"
                    >
                        <img
                            src="<?= htmlspecialchars($image['src'], ENT_QUOTES, 'UTF-8') ?>"
                            alt=""
                            <?php if ($image['width'] > 0 && $image['height'] > 0): ?>
                                width="<?= (int) $image['width'] ?>"
                                height="<?= (int) $image['height'] ?>"
                            <?php endif; ?>
                            loading="<?= $index === 0 ? 'eager' : 'lazy' ?>"
                            decoding="async"
                        >
                    </a>
                </li>
            <?php endforeach; ?>
        </ul>
        </div>

        <?php if ($total > 1): ?>
            <button
                type="button"
                class="gallery-arrow gallery-arrow--prev"
                data-gallery-prev
                aria-controls="<?= htmlspecialchars($trackId, ENT_QUOTES, 'UTF-8') ?>"
                aria-label="Anterior"
            >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true" width="22" height="22">
                    <path d="M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z"/>
                </svg>
            </button>
            <button
                type="button"
                class="gallery-arrow gallery-arrow--next"
                data-gallery-next
                aria-controls="<?= htmlspecialchars($trackId, ENT_QUOTES, 'UTF-8') ?>"
                aria-label="Siguiente"
            >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true" width="22" height="22">
                    <path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"/>
                </svg>
            </button>
        <?php endif; ?>
    </div>
</section>
