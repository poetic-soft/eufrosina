<?php
/** @var int $nEscritos */
/** @var int $nDiario */
/** @var list<array{src: string, filename: string, width: int, height: int, alt: string}> $heroImages */
/** @var list<array{slug: string, titulo: string, images: list<array{src: string, filename: string, width: int, height: int, alt: string}>}> $galleries */
/** @var Eufrosina\View $this */

$heroImages = $heroImages ?? [];
$galleries = $galleries ?? [];
?>
<?= $this->partial('modules/hero', [
    'images' => $heroImages,
    'archivo' => 'c.png',
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
        <span>Torrelobatón y Valladolid, 2022.</span>
    </a>
</nav>

<div class="home-intro">
    <p>Esta web reúne la voz de una mujer que <strong>aprendió a leer y escribir de adulta</strong>, que <strong>viajó</strong>, que <strong>se rió en los balnearios</strong>, que <strong>hizo bolillos en el patio de Torre</strong> y que <strong>apuntó el calor, la lluvia y las fiestas del pueblo</strong>.</p>
    <p>Hay dos cajas de papeles. Los <strong>escritos</strong> (viajes, clase, asociaciones de mujeres, cartas a la pandilla del boli) y el <strong>diario</strong> de 2022, cuando el verano fue de fuego y ella esperaba la lluvia para quedarse un mes más en el pueblo.</p>
</div>

<?= $this->partial('modules/gallery', [
    'series' => $galleries,
    'galeria' => 'a',
    'text' => 'Momentos familiares'
]) ?>
