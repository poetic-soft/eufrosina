<?php
/** @var Eufrosina\Namesake $nombre */
/** @var string $cuerpo */

$backHref = '/eufrosinas';
$showFoto = $nombre->imageUrl() !== null;
?>
<section class="literary literary--entry">
    <a class="back literary-back" href="<?= $backHref ?>">Eufrosinas</a>

    <header class="literary-mast">
        <div class="literary-title-row">
            <h1><?= htmlspecialchars($nombre->title, ENT_QUOTES, 'UTF-8') ?></h1>
            <?php if ($nombre->epoca !== ''): ?>
                <p class="literary-aside"><?= htmlspecialchars($nombre->epoca, ENT_QUOTES, 'UTF-8') ?></p>
            <?php endif; ?>
        </div>
    </header>

    <div class="literary-spread<?= $showFoto ? '' : ' literary-spread--text' ?>">
        <?php if ($showFoto): ?>
            <figure class="literary-plate">
                <a
                    href="<?= htmlspecialchars($nombre->imageUrl(), ENT_QUOTES, 'UTF-8') ?>"
                    target="_blank"
                    rel="noopener noreferrer"
                    hx-boost="false"
                    title="Abrir a tamaño completo"
                >
                    <img
                        src="<?= htmlspecialchars($nombre->imageUrl(), ENT_QUOTES, 'UTF-8') ?>"
                        alt="Imagen de <?= htmlspecialchars($nombre->title, ENT_QUOTES, 'UTF-8') ?>"
                        width="374"
                        height="512"
                        decoding="async"
                    >
                </a>
            </figure>
        <?php endif; ?>

        <article class="cuerpo literary-body">
            <?= $cuerpo ?>
        </article>
    </div>

    <a class="back literary-back literary-back--foot" href="<?= $backHref ?>">Eufrosinas</a>
</section>
