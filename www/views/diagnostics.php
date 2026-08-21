<?php
/** @var string $title */
/** @var array<string, mixed> $diagnostics */
?>
<h1>Diagnóstico de cache</h1>
<p>Estado de la cache en disco (<code>storage/cache</code>).</p>

<div id="cache-status">
    <?php include __DIR__ . '/partials/cache-status.php'; ?>
</div>

<button
    hx-get="/diagnostics/probe"
    hx-target="#cache-status"
    hx-swap="innerHTML">
    Reprobar cache (htmx)
</button>
