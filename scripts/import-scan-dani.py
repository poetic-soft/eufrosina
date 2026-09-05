# -*- coding: utf-8 -*-
"""Importa páginas de scan/dani a www/piezas/diario."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "scan" / "dani"
PIEZAS = ROOT / "www" / "piezas" / "diario"


def src(name: str) -> Path:
    return SCAN / name


def write_md(path: Path, meta: dict, body: str) -> None:
    lines = ["---"]
    for k, v in meta.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append(body.rstrip() + "\n")
    path.write_text("\n".join(lines), encoding="utf-8")


def copy_image(dest: Path, image: Path, crop: tuple[float, float, float, float] | None = None) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if crop is None:
        shutil.copy2(image, dest)
        return
    im = Image.open(image)
    w, h = im.size
    l, t, r, b = crop
    box = (int(w * l), int(h * t), int(w * r), int(h * b))
    im.crop(box).convert("RGB").save(dest, "JPEG", quality=90)


def update_orden(slug: str, orden: int) -> None:
    folder = PIEZAS / slug
    for name in ("original.md", "corregido.md"):
        path = folder / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"(?m)^orden:\s*\d+\s*$", f"orden: {orden}", text, count=1)
        path.write_text(text, encoding="utf-8")


# Actualizar orden de piezas ya existentes (cronológico YYYYMMDD)
EXISTING_ORDEN = {
    "01-torrelobaton-16-julio-2022": 20220716,
    "02-torrelobaton-25-julio-2022": 20220725,
    "03-torrelobaton-27-julio-2022": 20220727,
    "04-torrelobaton-8-agosto-2022": 20220808,
    "05-torrelobaton-10-agosto-2022": 20220810,
    "06-torrelobaton-15-septiembre-2022": 20220915,
    "07-torrelobaton-18-octubre-2022": 20221018,
    "08-torrelobaton-octubre-noviembre-2022": 20221106,
    "09-valladolid-21-noviembre-2022": 20221121,
}

# Nuevas piezas: slug, orden, imagen, crop opcional, original, corregido
PIECES: list[dict] = [
    {
        "slug": "10-verano-2016",
        "orden": 20160701,
        "image": "WhatsApp Image 2026-09-03 at 13.30.34 (6).jpeg",
        "original": """Verano del 2016

Meses de julio, agosto y

Parte de septiembre,

con un calor de 38ºC.

y parte antes en junio

y sin caer una gota

de agua.""",
        "corregido": """# Verano de 2016

Meses de julio, agosto y parte de septiembre, con un calor de 38 grados, y parte antes en junio, y sin caer una gota de agua.""",
    },
    {
        "slug": "11-marzo-2017",
        "orden": 20170311,
        "image": "WhatsApp Image 2026-09-03 at 13.30.34 (5).jpeg",
        "crop": (0.0, 0.0, 1.0, 0.55),
        "original": """marzo, 2017

Primera semana hasta

el 11-12-) días soleados

y de calor, con temperatu-

ras de- 17-18 Gds""",
        "corregido": """# Marzo de 2017

Primera semana hasta el 11-12: días soleados y de calor, con temperaturas de 17-18 grados.""",
    },
    {
        "slug": "12-torrelobaton-semana-santa-2017",
        "orden": 20170416,
        "image": "WhatsApp Image 2026-09-03 at 13.30.34 (4).jpeg",
        "crop": (0.0, 0.0, 1.0, 0.48),
        "original": """Semana Santa

de abril, 10 - al 16 - una

semana de verano, muy

seca, con la falta que hace

el agua, 16-4-2017

Torrelobatón""",
        "corregido": """# Torrelobatón, Semana Santa de 2017

Del 10 al 16 de abril: una semana de verano, muy seca, con la falta que hace el agua.

16 de abril de 2017""",
    },
    {
        "slug": "13-abril-2017-calor",
        "orden": 20170423,
        "image": "WhatsApp Image 2026-09-03 at 13.30.34 (5).jpeg",
        "crop": (0.0, 0.45, 1.0, 1.0),
        "original": """23-4-2017

unas semanas de un

calor de verano 24-28 Gds""",
        "corregido": """# 23 de abril de 2017

Unas semanas de un calor de verano: 24-28 grados.""",
    },
    {
        "slug": "14-moncayo-1-mayo-2017",
        "orden": 20170501,
        "image": "WhatsApp Image 2026-09-03 at 13.30.34 (4).jpeg",
        "crop": (0.0, 0.42, 1.0, 1.0),
        "original": """1-5-2017,

un fin de semana en

familia, en el entorno

del Moncayo,

Santa Cruz del

Moncayo, con Daniela

con cinco años la

abuela con 85, ha estado

bien, no pensaba yo

que iba aguantar el

camino y la marcha

Eufrosina""",
        "corregido": """# Santa Cruz del Moncayo, 1 de mayo de 2017

Un fin de semana en familia, en el entorno del Moncayo, Santa Cruz del Moncayo, con Daniela —con cinco años—; la abuela, con 85, ha estado bien. No pensaba yo que iba a aguantar el camino y la marcha.

Eufrosina""",
    },
    {
        "slug": "15-12-octubre-2017",
        "orden": 20171012,
        "image": "WhatsApp Image 2026-09-03 at 13.30.34 (3).jpeg",
        "crop": (0.0, 0.0, 1.0, 0.52),
        "original": """12 - Octubre, 2017

llevamos un verano de lo

más caluroso y sin

llover hoy dia del Pilar

sigue haciendo mucho

calor.""",
        "corregido": """# 12 de octubre de 2017

Llevamos un verano de lo más caluroso y sin llover. Hoy, día del Pilar, sigue haciendo mucho calor.""",
    },
    {
        "slug": "16-7-enero-2018-nieve",
        "orden": 20180107,
        "image": "WhatsApp Image 2026-09-03 at 13.30.34 (3).jpeg",
        "crop": (0.0, 0.48, 1.0, 1.0),
        "original": """dia, 7 - Enero. 2018 -

una mañana bonita

de nieve, despues de tanta

sequia, llega el agua

que dure mucho.""",
        "corregido": """# 7 de enero de 2018

Una mañana bonita de nieve. Después de tanta sequía, llega el agua: que dure mucho.""",
    },
    {
        "slug": "17-14-noviembre-2018",
        "orden": 20181114,
        "image": "WhatsApp Image 2026-09-03 at 13.30.34 (1).jpeg",
        "crop": (0.48, 0.0, 1.0, 0.72),
        "original": """dia-14-11-2018

un día espléndido de

calor vengo de darme un

paseo por la carretera

Madrid y estoy sudando

hoy me he paseado

mucho, así me duele

el famoso pie

Eufrosina""",
        "corregido": """# 14 de noviembre de 2018

Un día espléndido de calor. Vengo de darme un paseo por la carretera de Madrid y estoy sudando: hoy me he paseado mucho, así me duele el famoso pie.

Eufrosina""",
    },
    {
        "slug": "18-31-diciembre-2018",
        "orden": 20181231,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (4).jpeg",
        "crop": (0.48, 0.0, 1.0, 1.0),
        "original": """dia - 31-12-2018

una mañana muy solea-

da Pero con una helada

mayuscula, En estos

momento estoy pensando

en salir ha comprar para

la cena y no se qué,

espero que cuando

vea en el mercado me

inspire.

Eufrosina""",
        "corregido": """# 31 de diciembre de 2018

Una mañana muy soleada, pero con una helada mayúscula. En estos momentos estoy pensando en salir a comprar para la cena y no sé qué; espero que, cuando vea en el mercado, me inspire.

Eufrosina""",
    },
    {
        "slug": "19-18-enero-2019-nieve",
        "orden": 20190118,
        "image": "WhatsApp Image 2026-09-03 at 13.30.35.jpeg",
        "crop": (0.0, 0.28, 1.0, 0.72),
        "original": """18-1-2019- H 1- del

mediodia, en estos momen-

tos, esta nevando copiosa-

mente que bonito espero

que siga.""",
        "corregido": """# 18 de enero de 2019

A la una del mediodía, en estos momentos, está nevando copiosamente. Qué bonito: espero que siga.""",
    },
    {
        "slug": "20-30-abril-2019",
        "orden": 20190430,
        "image": "WhatsApp Image 2026-09-03 at 13.30.35.jpeg",
        "crop": (0.0, 0.68, 1.0, 1.0),
        "original": """30-4-2019

un dia muy caluroso

con una temperatura

de 25 G""",
        "corregido": """# 30 de abril de 2019

Un día muy caluroso, con una temperatura de 25 grados.""",
    },
    {
        "slug": "21-23-noviembre-2019",
        "orden": 20191123,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (6).jpeg",
        "crop": (0.48, 0.0, 1.0, 0.58),
        "original": """dia. 23.11.2019 - Hora 9.30

En estos momentos vengo

de darme un paseo de

una hora y vengo así

como rota, joder como

me duelen tanto mis

huesos, parezco un

cacharro roto.

Eufrosina""",
        "corregido": """# 23 de noviembre de 2019

A las 9:30. En estos momentos vengo de darme un paseo de una hora y vengo así como rota. Joder, cómo me duelen tanto mis huesos: parezco un cacharro roto.

Eufrosina""",
    },
    {
        "slug": "22-27-noviembre-2019",
        "orden": 20191127,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (6).jpeg",
        "crop": (0.48, 0.52, 1.0, 1.0),
        "original": """27-11-2019

Porque me duelen tanto

los hombros los estoy

imbalida de brazos y pies!""",
        "corregido": """# 27 de noviembre de 2019

¿Por qué me duelen tanto los hombros? Los estoy inválida de brazos y pies.""",
    },
    {
        "slug": "23-29-noviembre-2019",
        "orden": 20191129,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (3).jpeg",
        "crop": (0.0, 0.0, 1.0, 0.42),
        "original": """día, 29-11-2019

Como se puede seguir

viviendo con tantos

dolores y sentirse tan

inútil..

Eufrosina""",
        "corregido": """# 29 de noviembre de 2019

Cómo se puede seguir viviendo con tantos dolores y sentirse tan inútil…

Eufrosina""",
    },
    {
        "slug": "24-11-marzo-2020",
        "orden": 20200311,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (2).jpeg",
        "crop": (0.0, 0.0, 1.0, 0.48),
        "original": """miércoles, 11-3-2020

llevamos unos días

de marzo muy soleados

con temperaturas por la

mañana fresquitas 6 Gds

y la tarde con unos

18 G-""",
        "corregido": """# Miércoles, 11 de marzo de 2020

Llevamos unos días de marzo muy soleados, con temperaturas por la mañana fresquitas —6 grados— y la tarde con unos 18 grados.""",
    },
    {
        "slug": "25-16-marzo-2020",
        "orden": 20200316,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (1).jpeg",
        "original": """Lunes, 16-3-2020

Ha amanecido lloviendo

y a las 16,30 tenemos

3 G de temperatura, en

estos momentos esta que-

riendo como nevar

esta cayendo como sal

Tambien es el segundo

dia de estar sin salir

de casa por el vichito

ese que anda por ahi

esperemos poder con el

Yo no he conocido otra

peste igual en toda mi

vida y mira que

han pasado pestes. —

Eufrosina""",
        "corregido": """# Lunes, 16 de marzo de 2020

Ha amanecido lloviendo y a las 16:30 tenemos 3 grados de temperatura; en estos momentos está queriendo como nevar: está cayendo como sal.

También es el segundo día de estar sin salir de casa por el bichito ese que anda por ahí. Esperemos poder con él.

Yo no he conocido otra peste igual en toda mi vida, y mira que han pasado pestes.

Eufrosina""",
    },
    {
        "slug": "26-torrelobaton-17-marzo-2020",
        "orden": 20200317,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32 (2).jpeg",
        "original": """Torrelobatón

día 17- martes, sigo en

Torre a consecuencia de la

Peste esta (Coronavirus) me

veo en Valladolid mas encerra-

da en este momento son

las 12 de mediodía y se

ve una niebla que esta la

calle como si hubiera humo

espero que salga el Sol antes

de las dos para salir a dar-

me el Paseo de la mañana

la temperatura es muy agra-

dable

Eufrosina""",
        "corregido": """# Torrelobatón, martes 17 de marzo de 2020

Sigo en Torre a consecuencia de esta peste (coronavirus); me veo en Valladolid más encerrada. En este momento son las 12 del mediodía y se ve una niebla que está la calle como si hubiera humo. Espero que salga el sol antes de las dos para salir a darme el paseo de la mañana; la temperatura es muy agradable.

Eufrosina""",
    },
    {
        "slug": "27-semana-santa-2020",
        "orden": 20200405,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33.jpeg",
        "original": """Domingo, 5-4-2020

Domingo de Ramos, una

Semana Santa un poco rara

pues a causa del Coronavirus

ese vicho que nos tiene

encerrados a todos no abra

Procesiones y creo que

tampoco la hubiera habido

pues llevamos unos días

con chaparrones.

Domingo de Resurección

esto esta desierto no se

ve a nadie por la calle

estos dias han caído unos

buenos chaparrones así

como abril las aguas mil

Pero nunca han parado el

mundo como está que

vichito abran tirado para

que sea tan potente y

tenerle tanto miedo.

esperemos haber en que

termina la cosa porque

sino moriremos de pena

moriremos por estar

encerrados y los niños

sin salir de casa pobres.

Coronavirus este es el

vicho que nos quiere matar""",
        "corregido": """# Domingo de Ramos, 5 de abril de 2020

Una Semana Santa un poco rara, pues a causa del coronavirus —ese bicho que nos tiene encerrados a todos— no habrá procesiones, y creo que tampoco las hubiera habido, pues llevamos unos días con chaparrones.

## Domingo de Resurrección

Esto está desierto: no se ve a nadie por la calle. Estos días han caído unos buenos chaparrones; así como «abril, aguas mil».

Pero nunca han parado el mundo como está: qué bichito habrán tirado para que sea tan potente y tenerle tanto miedo. Esperemos a ver en qué termina la cosa, porque si no, moriremos de pena, moriremos por estar encerrados, y los niños sin salir de casa, pobres.

Coronavirus: este es el bicho que nos quiere matar.""",
    },
    {
        "slug": "28-23-abril-2020",
        "orden": 20200423,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32 (7).jpeg",
        "original": """día 23, Abril, 2020

fiesta de la Comunidad

con el bicho este que nos

tiene en casa sin salir

Ya llevamos cuarenta

días encerrados en casa

y sin esperanzas de Poder

salir mientras no tengan

un medicamento que

lo pueda matar

coronavirus este es el

nombre del Bicho que qui-

ere matarnos a todos.

Este mes de abril se ve que

como no tenemos conta-

minación esta lloviendo

bastante, para el campo

buenísimo esta precioso

lo que se ve en la tele

lástima que no vamos

a poder disfrutarlo,

suponiendo que cuando

salga de casa pueda

andar bien.

Eufrosina""",
        "corregido": """# 23 de abril de 2020

Fiesta de la Comunidad, con este bicho que nos tiene en casa sin salir. Ya llevamos cuarenta días encerrados en casa y sin esperanzas de poder salir mientras no tengan un medicamento que lo pueda matar.

Coronavirus: este es el nombre del bicho que quiere matarnos a todos.

Este mes de abril se ve que, como no tenemos contaminación, está lloviendo bastante; para el campo, buenísimo: está precioso lo que se ve en la tele. Lástima que no vamos a poder disfrutarlo, suponiendo que, cuando salga de casa, pueda andar bien.

Eufrosina""",
    },
    {
        "slug": "29-27-abril-2020",
        "orden": 20200427,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32 (6).jpeg",
        "crop": (0.0, 0.28, 0.52, 1.0),
        "original": """27- abril 2020, lunes

sigue con ganas de

llover por la tarde llovera

y yo en casa sin salir

este bicho nos tiene cas-

tigados a todo el mundo

han dado permiso para

que salgan los niños

pero no se ven apenas niños

los padres tienen miedo

salir pienso que algun dia

saldremos

Eufrosina""",
        "corregido": """# Lunes, 27 de abril de 2020

Sigue con ganas de llover; por la tarde lloverá, y yo en casa sin salir. Este bicho nos tiene castigados a todo el mundo. Han dado permiso para que salgan los niños, pero no se ven apenas niños: los padres tienen miedo de salir. Pienso que algún día saldremos.

Eufrosina""",
    },
    {
        "slug": "30-8-junio-2020",
        "orden": 20200608,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32 (6).jpeg",
        "crop": (0.48, 0.0, 1.0, 1.0),
        "original": """Junio, 8-6-2020

despues de unos dias de

calor de verano ha llega-

do el frío el reflon no

falla hasta el cuarenta

de mayo no te quites el

sayo.

Seguimos con el bicho,

este que no nos va a dejar

en mucho tiempo

haber quien aguanta mas

esta haciendo una

buena limpieza.

Eufrosina

entre tanto Viejo al que

pille descuidado plus nos

cojera.""",
        "corregido": """# 8 de junio de 2020

Después de unos días de calor de verano ha llegado el frío: el reflón no falla; «hasta el cuarenta de mayo no te quites el sayo».

Seguimos con el bicho, este que no nos va a dejar en mucho tiempo. A ver quién aguanta más: está haciendo una buena limpieza. Entre tanto viejo al que pille descuidado, plus nos cogerá.

Eufrosina""",
    },
    {
        "slug": "31-22-junio-2020",
        "orden": 20200622,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32 (5).jpeg",
        "original": """22-6-2020, lunes

Despues de tres meses de estar

encerrados,, ya podemos

salir y viajar por el

mundo ya veremos como

termina esto, si matamos

al bicho o el bicho, nos

mata el Coronavirus

tiene mucha potencia

y todavia no han des

cubierto nada para ma

tarlo.

Espero que con este calor

que tenemos se achichu

rre son 38 G-

Eufrosina""",
        "corregido": """# Lunes, 22 de junio de 2020

Después de tres meses de estar encerrados, ya podemos salir y viajar por el mundo. Ya veremos cómo termina esto: si matamos al bicho o el bicho nos mata. El coronavirus tiene mucha potencia y todavía no han descubierto nada para matarlo.

Espero que con este calor que tenemos se achicharre: son 38 grados.

Eufrosina""",
    },
    {
        "slug": "32-24-junio-2020-san-juan",
        "orden": 20200624,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32 (4).jpeg",
        "crop": (0.0, 0.0, 0.52, 1.0),
        "original": """24-6-2020, dia de San Juan

esta noche ha sido de

tormentas y la mañana

esta nublado asi como

siempre en el dia de San

Juan, es estropea meriendas.

algunos años nos estropeaba

el ir a comer la merienda

a la fuente mas proxima,

se preparaba la tormenta

y se acabo.

Eufrosina""",
        "corregido": """# Día de San Juan, 24 de junio de 2020

Esta noche ha sido de tormentas y la mañana está nublada, así como siempre en el día de San Juan: se estropean meriendas. Algunos años nos estropeaba el ir a comer la merienda a la fuente más próxima: se preparaba la tormenta y se acabó.

Eufrosina""",
    },
    {
        "slug": "33-torrelobaton-3-agosto-2020",
        "orden": 20200803,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (5).jpeg",
        "crop": (0.48, 0.0, 1.0, 0.72),
        "original": """Torrelobaton dia, 3-8-2020

Despues de unos dias de

mucho calor, se ha cambia-

do para mas fresquito

creo que tenemos unos

30 G, Por la mañana y

la noche hace fresquito

Eufrosina""",
        "corregido": """# Torrelobatón, 3 de agosto de 2020

Después de unos días de mucho calor, se ha cambiado para más fresquito. Creo que tenemos unos 30 grados; por la mañana y la noche hace fresquito.

Eufrosina""",
    },
    {
        "slug": "34-torrelobaton-6-agosto-2020",
        "orden": 20200806,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32 (4).jpeg",
        "crop": (0.48, 0.0, 1.0, 1.0),
        "original": """dia 6-8-2020 Torrelobatón

Vaya dia de calor en el

patio a los 2 - se frien

los pajaros tengo dos

pichones en el arbol no

se si no se quemaran

por lo menos hay 45 G,

menos mal que por la

noche refresca mucho

Eufrosina""",
        "corregido": """# Torrelobatón, 6 de agosto de 2020

Vaya día de calor: en el patio, a las 2, se fríen los pájaros. Tengo dos pichones en el árbol; no sé si no se quemarán. Por lo menos hay 45 grados; menos mal que por la noche refresca mucho.

Eufrosina""",
    },
    {
        "slug": "35-1-noviembre-2020",
        "orden": 20201101,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32 (3).jpeg",
        "original": """Día - 1 - 11 - 2020

Domingo día de Todos los

Santos

Una mañana con mucha

niebla a partir de las dos

ha salido el Sol y esta

esplendido con una gran

temperatura, en esta casa

se esta muy bien con el

Sol Portodas Partes en el

Patio se esta muy bien

Eufrosina

aquí parece que no hay

Bicho contagioso.""",
        "corregido": """# Domingo, 1 de noviembre de 2020

Día de Todos los Santos. Una mañana con mucha niebla; a partir de las dos ha salido el sol y está espléndido, con una gran temperatura. En esta casa se está muy bien con el sol por todas partes; en el patio se está muy bien.

Aquí parece que no hay bicho contagioso.

Eufrosina""",
    },
    {
        "slug": "36-17-abril-2021",
        "orden": 20210417,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32 (1).jpeg",
        "crop": (0.0, 0.35, 1.0, 1.0),
        "original": """Sabado, 17-4-2021

Tengo una mañana perra

esta pata esta chunga y

mi cadera, ayer la di

un paseo regular y se

ve que estan cansados

creo que llegara el dia que

no van a querer andar

Eufrosina""",
        "corregido": """# Sábado, 17 de abril de 2021

Tengo una mañana perra: esta pata está chunga y mi cadera. Ayer le di un paseo regular y se ve que están cansados. Creo que llegará el día que no van a querer andar.

Eufrosina""",
    },
    {
        "slug": "37-24-julio-2021-dentista",
        "orden": 20210724,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (4).jpeg",
        "crop": (0.0, 0.0, 0.52, 1.0),
        "original": """Julio, 24-7-2021

Voy al dentista a

revisión de mis

clavos que me pusieron

ayer, Tengo ganas

de terminar con es-

te asunto de la boca

Para comer un

cacho de Pan agusto

Eufrosina""",
        "corregido": """# 24 de julio de 2021

Voy al dentista a revisión de mis clavos que me pusieron ayer. Tengo ganas de terminar con este asunto de la boca, para comer un cacho de pan a gusto.

Eufrosina""",
    },
    {
        "slug": "38-valladolid-24-noviembre-2021",
        "orden": 20211124,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (2).jpeg",
        "crop": (0.0, 0.45, 1.0, 1.0),
        "original": """miercoles 24-11-2021

en estos momentos que

son las 10 de la mañana

esta cayendo una precio-

sa nevada aber lo que

dura porque esta raro

ver nevar en Valladolid

así con esos copos tan

hermosos

Eufrosina""",
        "corregido": """# Miércoles, 24 de noviembre de 2021

En estos momentos, que son las 10 de la mañana, está cayendo una preciosa nevada. A ver lo que dura, porque está raro ver nevar en Valladolid así, con esos copos tan hermosos.

Eufrosina""",
    },
    {
        "slug": "39-18-enero-2022-bolillos",
        "orden": 20220118,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32.jpeg",
        "crop": (0.0, 0.0, 0.52, 1.0),
        "original": """dia 18-1-2022 martes

Hoy he empezado una la-

bor de bolillos que sera

para mi nieta Daniela

espero que tenga salud

para terminarla pues

es una labor vastante

complicada espero que si

termine.

Eufrosina""",
        "corregido": """# Martes, 18 de enero de 2022

Hoy he empezado una labor de bolillos que será para mi nieta Daniela. Espero que tenga salud para terminarla, pues es una labor bastante complicada. Espero que sí termine.

Eufrosina""",
    },
    {
        "slug": "40-valladolid-28-enero-2022",
        "orden": 20220128,
        "image": "WhatsApp Image 2026-09-03 at 13.30.32.jpeg",
        "crop": (0.48, 0.0, 1.0, 1.0),
        "original": """Valladolid, 28-1-2022

Un mes de lo mas sobado

con unas temperaturas por

la noche heladoras y

luego de dia mucho sol asi

todo el mes sin caer una

gota de agua, vendra

Febrero mas suave

esperemos.

Eufrosina""",
        "corregido": """# Valladolid, 28 de enero de 2022

Un mes de lo más sobado, con unas temperaturas por la noche heladoras y luego de día mucho sol; así todo el mes sin caer una gota de agua. Vendrá febrero más suave, esperemos.

Eufrosina""",
    },
    {
        "slug": "41-7-abril-2022",
        "orden": 20220407,
        "image": "WhatsApp Image 2026-09-03 at 13.30.31 (6).jpeg",
        "original": """7-4-2022

Jueves, Despues de tres

meses sin llover, ha llegado

abril y esta haciendo de todo

a llovido y a nevado por

esos montes y despues de

tenerlo todo florido llegaron

unas heladas que lo ha

matado todo.

No hay abril que no

sea Ruin

creo que estamos pasando

unos años de prueba porque

tenemos de todo pestes, volcanes,

guerras, sequia y heladas,

solo queda la langosta.

Eufrosina""",
        "corregido": """# Jueves, 7 de abril de 2022

Después de tres meses sin llover, ha llegado abril y está haciendo de todo: ha llovido y ha nevado por esos montes, y después de tenerlo todo florido llegaron unas heladas que lo han matado todo.

No hay abril que no sea ruin. Creo que estamos pasando unos años de prueba, porque tenemos de todo: pestes, volcanes, guerras, sequía y heladas; solo queda la langosta.

Eufrosina""",
    },
    {
        "slug": "42-valladolid-22-abril-2022",
        "orden": 20220422,
        "image": "WhatsApp Image 2026-09-03 at 13.30.31 (5).jpeg",
        "original": """Valladolid- 22-4-2022

llevamos unos dias de lluvia

y nieve este mes de abril se

esta portando con heladas

agua nieve y sol.

Hoy ha amanecido lloviendo

todo el día.

Esta tarde despues de dos

años he estado en un con-

cierto de guitarras en el

centro cívico, que emoción

despues de tanto tiempo que

emoción, se han juntado

el grupo de Vivar y un

grupo de Santander fabuloso

haber si ya arrancamos

en hacer una vida normal

Eufrosina""",
        "corregido": """# Valladolid, 22 de abril de 2022

Llevamos unos días de lluvia y nieve: este mes de abril se está portando, con heladas, agua, nieve y sol. Hoy ha amanecido lloviendo todo el día.

Esta tarde, después de dos años, he estado en un concierto de guitarras en el centro cívico. Qué emoción, después de tanto tiempo: qué emoción. Se han juntado el grupo de Vivar y un grupo de Santander; fabuloso. A ver si ya arrancamos en hacer una vida normal.

Eufrosina""",
    },
    {
        "slug": "43-torrelobaton-12-septiembre-2022",
        "orden": 20220912,
        "image": "WhatsApp Image 2026-09-03 at 13.30.31 (1).jpeg",
        "crop": (0.0, 0.48, 0.55, 1.0),
        "original": """Septiembre, 12 - Torre

Por fin parece que va ha

llover, despues de tantos

meses sin caer una

gota esta muy nublo

y ha bajado la temperatura

Eufrosina""",
        "corregido": """# Torre, 12 de septiembre de 2022

Por fin parece que va a llover, después de tantos meses sin caer una gota. Está muy nublado y ha bajado la temperatura.

Eufrosina""",
    },
    {
        "slug": "44-31-agosto-humo",
        "orden": 20220831,
        "image": "WhatsApp Image 2026-09-03 at 13.30.07.jpeg",
        "crop": (0.0, 0.0, 1.0, 0.78),
        "original": """31. de Agosto

el día a amanecido

muy nublo y fresquito

ya podría llover para que

se limpie un poco el

aire que esta muy

cargado con tantos

fuegos estamos respiran-

do el humo a si como

si nada nos va mi-

nando nuestros

cuerpo.

Eufrosina""",
        "corregido": """# 31 de agosto

El día ha amanecido muy nublado y fresquito. Ya podría llover para que se limpie un poco el aire, que está muy cargado con tantos fuegos: estamos respirando el humo así como si nada; nos va minando nuestros cuerpos.

Eufrosina""",
    },
    {
        "slug": "45-valladolid-29-noviembre-2022",
        "orden": 20221129,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (5).jpeg",
        "crop": (0.0, 0.0, 0.52, 1.0),
        "original": """V, 29-11-2022 martes

Vengo del medico de

cabecero pues con esta

peste llebaba estos años

sin ver una persona solo

maquinas que te hablan

menos mal que lo que

me an puesto parece per-

sona se ha portado

bien aber si me dura

La mañana estaba

como en estas fechas es

Valladolid con niebla

y frío uno bajocero

normal como tiene que

hacer

Eufrosina""",
        "corregido": """# Valladolid, martes 29 de noviembre de 2022

Vengo del médico de cabecera, pues con esta peste llevaba estos años sin ver una persona: solo máquinas que te hablan. Menos mal que lo que me han puesto parece persona; se ha portado bien. A ver si me dura.

La mañana estaba, como en estas fechas es Valladolid, con niebla y frío: uno bajo cero, normal, como tiene que hacer.

Eufrosina""",
    },
    {
        "slug": "46-1-diciembre-2022-caja",
        "orden": 20221201,
        "image": "WhatsApp Image 2026-09-03 at 13.30.33 (6).jpeg",
        "crop": (0.0, 0.0, 0.52, 1.0),
        "original": """Jueves, 1-12-2022

Vengo de sacar dinero de

la caja de ahorros y de

verdad en que país estamos

y en que siglo pues me

parecía que estábamos otra

vez en mi infancia con las

colas para todo y se acababa

y nos íbamos a casa sin nada

pues ahora llegan las 11.30

y cierran la taquilla y no

puedes decir nada para mi

esta sociedad de tonta

maquina es una Mierda

y una Bergüenza""",
        "corregido": """# Jueves, 1 de diciembre de 2022

Vengo de sacar dinero de la caja de ahorros y, de verdad, ¿en qué país estamos y en qué siglo? Pues me parecía que estábamos otra vez en mi infancia, con las colas para todo, y se acababa y nos íbamos a casa sin nada. Pues ahora llegan las 11:30 y cierran la taquilla y no puedes decir nada. Para mí esta sociedad de tonta máquina es una mierda y una vergüenza.""",
    },
    {
        "slug": "47-valladolid-12-diciembre-2022",
        "orden": 20221212,
        "image": "WhatsApp Image 2026-09-03 at 13.30.30 (4).jpeg",
        "crop": (0.48, 0.0, 1.0, 1.0),
        "original": """Valladolid, 12-12-2022

Parece que este año esta cogi-

endo tempero el agua pues

desde que he venido de Torre

no habido día claro entre

niebla y chirimiri poco

a poco creo que los embalses

se iran llenando y las

fuentes cogiendo tempero

para que no nos sigan

dando la lata y las

electras sigan tirando el

agua y cobrandola a

Precio de oro.

Eufrosina""",
        "corregido": """# Valladolid, 12 de diciembre de 2022

Parece que este año está cogiendo tempero el agua, pues desde que he venido de Torre no ha habido día claro: entre niebla y chirimiri. Poco a poco creo que los embalses se irán llenando y las fuentes cogiendo tempero, para que no nos sigan dando la lata y las eléctricas sigan tirando el agua y cobrándola a precio de oro.

Eufrosina""",
    },
    {
        "slug": "48-valladolid-13-diciembre-2022",
        "orden": 20221213,
        "image": "WhatsApp Image 2026-09-03 at 13.30.30 (3).jpeg",
        "crop": (0.0, 0.0, 0.55, 1.0),
        "original": """dia 13-12-2022

en Valladolid

Tenemos una temperatura

de 13,6. Y es las 13 Horas

una mañana de lluvia lenta

como chiriviri mañana de

Paraguas. Ya se quejan los

labradores porque no pueden

sembrar y a los de la remolacha

no pueden sacar la remolacha.

Quien lo diria hace un mes

llorando porque no llovía

parecia que ya no lloveria

nunca como es el ser humano

que frágil.

Eufrosina""",
        "corregido": """# Valladolid, 13 de diciembre de 2022

Tenemos una temperatura de 13,6, y son las 13 horas: una mañana de lluvia lenta como chirimiri, mañana de paraguas. Ya se quejan los labradores porque no pueden sembrar, y los de la remolacha no pueden sacar la remolacha. Quién lo diría: hace un mes llorando porque no llovía, parecía que ya no llovería nunca. Cómo es el ser humano, qué frágil.

Eufrosina""",
    },
    {
        "slug": "49-valladolid-23-febrero-2023",
        "orden": 20230223,
        "image": "WhatsApp Image 2026-09-03 at 13.30.30 (2).jpeg",
        "crop": (0.45, 0.0, 1.0, 1.0),
        "original": """Febrero, Jueves, 23, 2-2023

(11 horas) Esta nevando en

estos momentos en

Valladolid despues de un

mes de Heladas y Sol

Todo el mes ha llegado

el imbierno.

que bonito se ve nevar

desde la bentana no

creo que cuaje seria fan-

tastico verlo blanco!

12,30 sigue nevando con unos

copos grandes

Eufrosina

3, H

Sigue con copos Grandes pero

no cuaja.""",
        "corregido": """# Valladolid, jueves 23 de febrero de 2023

A las 11 horas está nevando en estos momentos en Valladolid, después de un mes de heladas y sol. Todo el mes ha llegado el invierno. Qué bonito se ve nevar desde la ventana; no creo que cuaje: sería fantástico verlo blanco.

A las 12:30 sigue nevando con unos copos grandes.

A las 15:00 sigue con copos grandes, pero no cuaja.

Eufrosina""",
    },
    {
        "slug": "50-20-abril-2023",
        "orden": 20230420,
        "image": "WhatsApp Image 2026-09-03 at 13.30.30 (1).jpeg",
        "crop": (0.0, 0.0, 0.55, 0.58),
        "original": """Jueves, 20-4-2023

Seguimos con mucho Sol,

desde febrero que dejó de

llover no ha vuelto a caer

una gota solo Heladas de

noche y mucho Sol en el

dia, con unas temperaturas

altisimas para el mes que

estamos, como siga asi

este verano nos freímos

Eufrosina""",
        "corregido": """# Jueves, 20 de abril de 2023

Seguimos con mucho sol: desde febrero que dejó de llover no ha vuelto a caer una gota, solo heladas de noche y mucho sol en el día, con unas temperaturas altísimas para el mes que estamos. Como siga así, este verano nos freímos.

Eufrosina""",
    },
    {
        "slug": "51-torrelobaton-25-julio-2023",
        "orden": 20230725,
        "image": "WhatsApp Image 2026-09-03 at 13.30.30.jpeg",
        "original": """Torrelobatón, 25-7-2023

día de Santiago hoy es

fiesta segun los políticos

pues se ve que segun quien

mande el Santo es mas o

menos importante, muchos

años antes era fiesta luego

solo era en la Parte de

Santiago, y ahora otra

vez toca en castilla esto

es como el tiempo cuando

quiere hace frio o calor co-

mo este año que este mes

esta siendo fresquito por

las noche y las mañanas

esta Castilla es así de dura

cuando se trillaba decían a

trillar con manta y a carrear

con abrigo

Eufrosina

25, 7 - 2023

no me puedo creer que

en el mes de julio en el

pueblo tenga que dormir

con manta porque tengo

frío en la cama

25-7-2023 Torre

Son las 2 de la tarde

y se agradece estar en el

patio a la sombra de la

sombrilla pues la no-

che a sido fría y la ma-

ñana, quien diria que

podría estar a estas

horas sentada al sol y

sombra en este patio

y es Julio.""",
        "corregido": """# Torrelobatón, 25 de julio de 2023

Día de Santiago. Hoy es fiesta según los políticos, pues se ve que según quién mande el santo es más o menos importante. Muchos años antes era fiesta; luego solo era en la parte de Santiago, y ahora otra vez toca en Castilla. Esto es como el tiempo: cuando quiere hace frío o calor, como este año, que este mes está siendo fresquito por las noches y las mañanas. Esta Castilla es así de dura: cuando se trillaba decían «a trillar con manta y a carrear con abrigo».

No me puedo creer que en el mes de julio, en el pueblo, tenga que dormir con manta porque tengo frío en la cama.

Son las 2 de la tarde y se agradece estar en el patio a la sombra de la sombrilla, pues la noche ha sido fría y la mañana… Quién diría que podría estar a estas horas sentada al sol y sombra en este patio, y es julio.

Eufrosina""",
    },
    {
        "slug": "52-torre-3-septiembre-2023",
        "orden": 20230903,
        "image": "WhatsApp Image 2026-09-03 at 13.30.10 (2).jpeg",
        "original": """Septiembre, 3-2023, Torre

Ya llego el agua, una

mañana con bajada de

temperaturas, y nublado has-

ta sobre las tres, empezo a una

llovizna suave a continua-

ción unos truenos y el

chaparrón muy bueno

pero moderado. se ve que

la dana había descargado

por Toledo y en Madrid

con furia por aquí un

chaparrón como tiene que

ser pues la tiera esta tan

seca que asi es como se

aprovecha el agua con este

chaparrón comeré Higos de las

Higueras de la era

Eufrosina""",
        "corregido": """# Torre, 3 de septiembre de 2023

Ya llegó el agua: una mañana con bajada de temperaturas, y nublado hasta sobre las tres; empezó una llovizna suave, a continuación unos truenos y el chaparrón, muy bueno pero moderado. Se ve que la DANA había descargado por Toledo y en Madrid con furia; por aquí, un chaparrón como tiene que ser, pues la tierra está tan seca que así es como se aprovecha el agua. Con este chaparrón comeré higos de las higueras de la era.

Eufrosina""",
    },
    {
        "slug": "53-5-noviembre-2023",
        "orden": 20231105,
        "image": "WhatsApp Image 2026-09-03 at 13.30.10 (1).jpeg",
        "original": """Noviembre . 5-11-2023

Domingo: día que vine de

Torre despues de cinco meses

y al entrar en casa tenía

la casa llena de mierda

por un atronque que

se había preparado por

las dichosas toallitas me

dieron ganas de cerrar

la puerta y volverme

al pueblo, con lo agusto

que estaba ¿Porqué

no me quedo alli para

siempre?""",
        "corregido": """# Domingo, 5 de noviembre de 2023

Día que vine de Torre después de cinco meses, y al entrar en casa tenía la casa llena de mierda por un atranco que se había preparado por las dichosas toallitas. Me dieron ganas de cerrar la puerta y volverme al pueblo, con lo a gusto que estaba. ¿Por qué no me quedo allí para siempre?""",
    },
    {
        "slug": "54-28-diciembre-2023",
        "orden": 20231228,
        "image": "WhatsApp Image 2026-09-03 at 13.30.10.jpeg",
        "original": """dia. 28-12-2023

dia de concierto de

mayores en Miguel de Libes

a la Salida en la escalera

de subir tuve un

accidente muy apara-

toso terminé llena de

cardenales de pies a

cabeza pero no se

me Rompio ningun

Hueso

Eufrosina""",
        "corregido": """# 28 de diciembre de 2023

Día de concierto de mayores en Miguel Delibes. A la salida, en la escalera de subir, tuve un accidente muy aparatoso: terminé llena de cardenales de pies a cabeza, pero no se me rompió ningún hueso.

Eufrosina""",
    },
    {
        "slug": "55-30-octubre-2024",
        "orden": 20241030,
        "image": "WhatsApp Image 2026-09-03 at 13.30.03.jpeg",
        "original": """Lunes 30 Octubre, 2024

Primer dia de mis

ejercicios con mi

brazo roto.

Con todos mis dolores

aguante todos los

movimientos y como

me duele.

menos mal que los

que me atendían

eran fenomenales

Urra por ellos""",
        "corregido": """# Lunes, 30 de octubre de 2024

Primer día de mis ejercicios con mi brazo roto. Con todos mis dolores aguanté todos los movimientos, y cómo me duele. Menos mal que los que me atendían eran fenomenales. ¡Hurra por ellos!""",
    },
    {
        "slug": "56-21-enero-2025",
        "orden": 20250121,
        "image": "WhatsApp Image 2026-09-03 at 13.30.09.jpeg",
        "original": """21-1-2025, martes

Cuando son las 2.30 de

la tarde Parece de noche

pues esta lloviendo muy

bien, lo único que es un

aburrimiento no poder

salir de paseo y creo que

tampoco podré ir a la

clase de lectura porque en

mi situación que me estoy

quedándo un poco minus

valida este brazo me esta

machacando. Me gustaría

hacer cosas pero no puedo

por que me sigue doliendo

mucho sobre todo cuando

cojo la fregona ese movimiento

Eufrosina""",
        "corregido": """# Martes, 21 de enero de 2025

Cuando son las 2:30 de la tarde parece de noche, pues está lloviendo muy bien. Lo único es que es un aburrimiento no poder salir de paseo, y creo que tampoco podré ir a la clase de lectura porque, en mi situación —que me estoy quedando un poco minusválida—, este brazo me está machacando. Me gustaría hacer cosas, pero no puedo porque me sigue doliendo mucho, sobre todo cuando cojo la fregona: ese movimiento.

Eufrosina""",
    },
    {
        "slug": "57-25-febrero-2025",
        "orden": 20250225,
        "image": "WhatsApp Image 2026-09-03 at 13.30.07 (1).jpeg",
        "original": """25.2-2025

día en el que me dieron

el alta de mi rotura del

brazo despues de cinco

meses segun el medico

fenomeno con la aberia

que tenia y que maneje

el brazo casi bien tengo

un pequeño atranque

pero pienso que con el

tiempo se ira arreglan-

do espero por lo menos

meduele menos

Eufrosina""",
        "corregido": """# 25 de febrero de 2025

Día en el que me dieron el alta de mi rotura del brazo, después de cinco meses. Según el médico, fenómeno con la avería que tenía, y que maneje el brazo casi bien. Tengo un pequeño atranco, pero pienso que con el tiempo se irá arreglando; espero, por lo menos, me duele menos.

Eufrosina""",
    },
    {
        "slug": "58-17-enero-2026-san-anton",
        "orden": 20260117,
        "image": "WhatsApp Image 2026-09-03 at 13.30.02.jpeg",
        "original": """Sabado, 17-1-2026

Día de San Antón

Un dia amanecio

muy nublo y con mu-

cho frio despues templo

y en el rato del medio

dia empezó a nevar

un poquito daba gusto

ver caer los copos pero

como estaba el suelo

muy humedo segun

caia la nieve se desha-

cia solo en los coches

se vio un poco, y sigue

lloviendo el chirimiri

porque no llueve a chaparron

seguimos asi todo el mes

Eufrosina""",
        "corregido": """# Sábado, 17 de enero de 2026

Día de San Antón. Un día amaneció muy nublado y con mucho frío; después templó, y en el rato del mediodía empezó a nevar un poquito. Daba gusto ver caer los copos, pero como estaba el suelo muy húmedo, según caía la nieve se deshacía; solo en los coches se vio un poco. Y sigue lloviendo el chirimiri, porque no llueve a chaparrón. Seguimos así todo el mes.

Eufrosina""",
    },
    {
        "slug": "59-23-enero-2026",
        "orden": 20260123,
        "image": "WhatsApp Image 2026-09-03 at 13.30.02 (1).jpeg",
        "original": """día 23-1 2026 Viernes

seguimos con el tiempo

muy Borrascoso hoy

en las horas del mediodía

a nevado un poco unos

buenos copos pero segun

caian desaparecian.

Eufrosina""",
        "corregido": """# Viernes, 23 de enero de 2026

Seguimos con el tiempo muy borrascoso. Hoy, en las horas del mediodía, ha nevado un poco: unos buenos copos, pero según caían desaparecían.

Eufrosina""",
    },
]


def main() -> None:
    for slug, orden in EXISTING_ORDEN.items():
        update_orden(slug, orden)
        print(f"orden {orden}: {slug}")

    for piece in PIECES:
        folder = PIEZAS / piece["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        meta = {
            "coleccion": "diario",
            "fuente": "scan/dani",
            "imagen": "imagen.jpg",
            "orden": piece["orden"],
        }
        write_md(folder / "original.md", meta, piece["original"])
        write_md(folder / "corregido.md", meta, piece["corregido"])
        image_path = src(piece["image"])
        if not image_path.is_file():
            raise SystemExit(f"Falta imagen: {image_path}")
        copy_image(folder / "imagen.jpg", image_path, piece.get("crop"))
        print(f"ok {piece['slug']}")

    print(f"Total nuevas: {len(PIECES)}")


if __name__ == "__main__":
    main()
