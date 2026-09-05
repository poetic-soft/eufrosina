<?php

declare(strict_types=1);

require __DIR__ . '/../www/vendor/autoload.php';

$cache = new Eufrosina\Cache(__DIR__ . '/../www/storage/cache');
$namesakes = new Eufrosina\Namesakes(__DIR__ . '/../www/eufrosinas', $cache);

echo 'count=' . $namesakes->count() . PHP_EOL;
foreach ($namesakes->list() as $item) {
    echo $item->orden . "\t" . $item->slug . "\t" . ($item->imagen ?? '-') . PHP_EOL;
}

$first = $namesakes->list()[0] ?? null;
if ($first !== null) {
    $html = $namesakes->html($first);
    echo 'first_title_ok=' . (str_contains($html, '<h1>') ? 'yes' : 'no') . PHP_EOL;
    echo 'links_ok=' . (str_contains($html, '<a href="http') ? 'yes' : 'no') . PHP_EOL;
}

echo 'intro_len=' . strlen($namesakes->introHtml()) . PHP_EOL;
