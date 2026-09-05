<?php
/** @var string $introHtml */
/** @var list<Eufrosina\Namesake> $nombres */
?>
<section class="literary literary--index">
    <header class="literary-mast">
        <p class="literary-kicker">El nombre</p>
        <div class="literary-title-row">
            <h1>Eufrosinas</h1>
            <p class="literary-aside">Historia</p>
        </div>
        <p class="literary-lede">El eco del nombre, y las mujeres que lo llevaron.</p>
    </header>

    <article class="literary-rule-block namesakes-intro">
        <?= $introHtml ?>
    </article>

    <section class="literary-roster" aria-labelledby="namesakes-list-title">
        <h2 id="namesakes-list-title" class="literary-section-title">En la historia</h2>
        <?php if ($nombres === []): ?>
            <p class="muted">Todavía no hay entradas.</p>
        <?php else: ?>
            <ol class="literary-index">
                <?php foreach ($nombres as $i => $nombre): ?>
                    <li>
                        <a href="<?= htmlspecialchars($nombre->url(), ENT_QUOTES, 'UTF-8') ?>">
                            <span class="literary-index-num" aria-hidden="true"><?= str_pad((string) ($i + 1), 2, '0', STR_PAD_LEFT) ?></span>
                            <?php if ($nombre->imageUrl() !== null): ?>
                                <span class="literary-index-thumb">
                                    <img
                                        src="<?= htmlspecialchars($nombre->imageUrl(), ENT_QUOTES, 'UTF-8') ?>"
                                        alt=""
                                        width="96"
                                        height="120"
                                        loading="lazy"
                                        decoding="async"
                                    >
                                </span>
                            <?php endif; ?>
                            <span class="literary-index-copy">
                                <span class="literary-index-title"><?= htmlspecialchars($nombre->title, ENT_QUOTES, 'UTF-8') ?></span>
                                <?php if ($nombre->epoca !== ''): ?>
                                    <span class="literary-index-meta"><?= htmlspecialchars($nombre->epoca, ENT_QUOTES, 'UTF-8') ?></span>
                                <?php endif; ?>
                            </span>
                        </a>
                    </li>
                <?php endforeach; ?>
            </ol>
        <?php endif; ?>
    </section>
</section>
