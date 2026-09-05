<?php
/** @var int $nEscritos */
/** @var int $nDiario */
/** @var int $nEufrosinas */
/** @var list<array{src: string, filename: string, width: int, height: int, alt: string}> $heroImages */
/** @var list<array{slug: string, titulo: string, images: list<array{src: string, filename: string, width: int, height: int, alt: string}>}> $galleries */
/** @var Eufrosina\View $this */

$heroImages = $heroImages ?? [];
$galleries = $galleries ?? [];
$nEufrosinas = $nEufrosinas ?? 0;
?>
<?= $this->partial('modules/hero', [
    'images' => $heroImages,
    'archivo' => 'c.png',
    'caption' => 'Eufrosina y su familia en el año 1969',
]) ?>

<nav class="home-doors" aria-label="Cajas de papeles">
    <a class="door" href="/escritos">
        <strong>Escritos</strong>
        <span class="count"><?= (int) $nEscritos ?> piezas</span>
        <span>De Aranda a Lanjarón, de la clase al 8 de marzo.</span>
    </a>
    <a class="door" href="/diario">
        <strong>Diario</strong>
        <span class="count"><?= (int) $nDiario ?> piezas</span>
        <span>Torrelobatón y Valladolid, el tiempo y el pueblo.</span>
    </a>
    <a class="door" href="/eufrosinas">
        <strong>Eufrosinas</strong>
        <span class="count"><?= (int) $nEufrosinas ?> nombres</span>
        <span>El nombre y las mujeres que lo llevaron en la historia.</span>
    </a>
</nav>

<div class="home-intro">
    <p>Esta web reúne la voz de una mujer que <strong>aprendió a leer y escribir de adulta</strong>, que <strong>viajó</strong>, que <strong>se rió en los balnearios</strong>, que <strong>hizo bolillos en el patio de Torre</strong> y que <strong>apuntó el calor, la lluvia y las fiestas del pueblo</strong>.</p>
    <p>Hay cajas de papeles: los <strong>escritos</strong>, el <strong>diario</strong>, y una sala de <strong>Eufrosinas</strong> —el eco del nombre, desde las Gracias griegas hasta hoy.</p>
</div>

<?= $this->partial('modules/gallery', [
    'series' => $galleries,
    'galeria' => 'a',
    'text' => 'Momentos familiares'
]) ?>
