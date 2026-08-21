<?php
/** @var array<string, mixed> $diagnostics */

$bool = static function (mixed $value): string {
    return $value ? '<span class="ok">sí</span>' : '<span class="ko">no</span>';
};

$rows = [
    'PHP' => (string) ($diagnostics['php_version'] ?? ''),
    'Probe escritura' => $bool($diagnostics['probe_write_ok'] ?? false),
    'Probe lectura' => $bool($diagnostics['probe_read_ok'] ?? false),
    'Ruta cache' => '<code>' . htmlspecialchars((string) ($diagnostics['file_cache_path'] ?? ''), ENT_QUOTES, 'UTF-8') . '</code>',
    'Directorio escribible' => $bool($diagnostics['file_cache_writable'] ?? false),
];

$ok = ($diagnostics['probe_write_ok'] ?? false)
    && ($diagnostics['probe_read_ok'] ?? false)
    && ($diagnostics['file_cache_writable'] ?? false);
?>
<div class="panel">
    <table>
        <thead>
            <tr>
                <th>Comprobación</th>
                <th>Resultado</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($rows as $label => $value): ?>
                <tr>
                    <td><?= htmlspecialchars($label, ENT_QUOTES, 'UTF-8') ?></td>
                    <td><?= $value ?></td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>

    <?php if ($ok): ?>
        <p class="ok">Conclusión: cache en disco operativa.</p>
    <?php else: ?>
        <p class="ko">Conclusión: revisa permisos de <code>storage/cache</code>.</p>
    <?php endif; ?>
</div>
