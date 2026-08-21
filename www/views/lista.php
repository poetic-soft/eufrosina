<?php
/** @var string $heading */
/** @var string $lede */
/** @var string $coleccion */
/** @var list<Eufrosina\Piece> $piezas */
?>
<h1><?= htmlspecialchars($heading, ENT_QUOTES, 'UTF-8') ?></h1>
<p class="lede"><?= htmlspecialchars($lede, ENT_QUOTES, 'UTF-8') ?></p>

<?php if ($piezas === []): ?>
    <p class="muted">Todavía no hay piezas en esta caja.</p>
<?php else: ?>
    <ul class="piece-list">
        <?php foreach ($piezas as $pieza): ?>
            <li>
                <a href="<?= htmlspecialchars($pieza->url(), ENT_QUOTES, 'UTF-8') ?>">
                    <h2><?= htmlspecialchars($pieza->title, ENT_QUOTES, 'UTF-8') ?></h2>
                    <?php if ($pieza->excerpt !== ''): ?>
                        <p><?= htmlspecialchars($pieza->excerpt, ENT_QUOTES, 'UTF-8') ?></p>
                    <?php endif; ?>
                </a>
            </li>
        <?php endforeach; ?>
    </ul>
<?php endif; ?>
