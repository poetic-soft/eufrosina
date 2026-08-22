<?php
/** @var int $nEscritos */
/** @var int $nDiario */
?>
<header class="home-hero">
    <h1>Eufrosina Pérez Tera</h1>
    <p class="lede">Noventa y cinco años. Valladolid y Torrelobatón.</p>

    <div class="home-doors">
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
    </div>
</header>

<div class="home-intro">
    <p>Esta web reúne la voz de una mujer que <strong>aprendió a leer y escribir de adulta</strong>, que <strong>viajó</strong>, que <strong>se rió en los balnearios</strong>, que <strong>hizo bolillos en el patio de Torre</strong> y que <strong>apuntó el calor, la lluvia y las fiestas del pueblo</strong>.</p>
    <p>Hay dos cajas de papeles. Los <strong>escritos</strong> (viajes, clase, asociaciones de mujeres, cartas a la pandilla del boli) y el <strong>diario</strong> de 2022, cuando el verano fue de fuego y ella esperaba la lluvia para quedarse un mes más en el pueblo.</p>
    <p class="muted">No es una biografía oficial. Es su letra, recogida y ordenada para que se pueda leer.</p>
</div>
