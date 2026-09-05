# -*- coding: utf-8 -*-
"""Descarga imágenes Wikimedia/Wikipedia para www/eufrosinas."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "eufrosinas"
DEST = ROOT / "www" / "eufrosinas"
UA = "EufrosinaBlog/1.0 (personal memorial site)"

# slug, title, época, excerpt corto, archivo fuente, búsquedas Wikipedia (lang, title)
ENTRIES = [
    {
        "slug": "eufrosine",
        "title": "Eufrósine",
        "epoca": "Siglo VIII a. C.",
        "orden": 1,
        "source": "Eufrósine.md",
        "wiki": [("es", "Eufrósine"), ("en", "Euphrosyne"), ("en", "Charites")],
        "commons": ["The Three Graces Euphrosyne", "Charites Raphael", "Three Graces Canova"],
    },
    {
        "slug": "eufrosina-de-alejandria",
        "title": "Santa Eufrosina de Alejandría",
        "epoca": "Siglo V",
        "orden": 2,
        "source": "Eufrosina de Alejandría.md",
        "wiki": [("es", "Eufrosina de Alejandría"), ("en", "Euphrosyne of Alexandria")],
        "commons": ["Euphrosyne of Alexandria", "Saint Euphrosyne"],
    },
    {
        "slug": "eufrosina-emperatriz-bizantina",
        "title": "Eufrosina, emperatriz bizantina",
        "epoca": "Siglo IX",
        "orden": 3,
        "source": "Eufrosina (esposa de Miquel II).md",
        "wiki": [("ca", "Eufrosina (esposa de Miquel II)"), ("en", "Euphrosyne (9th century)")],
        "commons": ["Byzantine empress mosaic", "Constantine VI"],
    },
    {
        "slug": "eufrosina-de-polatsk",
        "title": "Santa Eufrosina de Pólatsk",
        "epoca": "Siglo XII",
        "orden": 4,
        "source": "Eufrosina de Pólatsk.md",
        "wiki": [("es", "Eufrosina de Pólatsk"), ("en", "Euphrosyne of Polotsk"), ("be", "Еўфрасіння Полацкая")],
        "commons": ["Euphrosyne of Polotsk", "Efrosinia Polotskaya"],
    },
    {
        "slug": "eufrosina-de-kiev",
        "title": "Eufrosina de Kiev",
        "epoca": "Siglo XII",
        "orden": 5,
        "source": "Eufrosina de Kiev.md",
        "wiki": [("es", "Eufrosina de Kiev"), ("en", "Euphrosyne of Kiev")],
        "commons": ["Euphrosyne of Kiev", "Géza II"],
    },
    {
        "slug": "eufrosina-ducena-camatera",
        "title": "Eufrosina Ducena Camatera",
        "epoca": "Siglo XII",
        "orden": 6,
        "source": "Eufrosina Ducena Camatera.md",
        "wiki": [("es", "Eufrosina Ducena Camatera"), ("en", "Euphrosyne Doukaina Kamatera")],
        "commons": ["Alexios III Angelos", "Byzantine empress"],
    },
    {
        "slug": "eufrosyne-of-masovia",
        "title": "Eufrosina de Mazovia",
        "epoca": "Siglo XIII",
        "orden": 7,
        "source": "Euphrosyne of Masovia.md",
        "wiki": [("en", "Euphrosyne of Masovia"), ("pl", "Eufrozyna mazowiecka")],
        "commons": ["Piast dynasty", "Masovia princess"],
    },
    {
        "slug": "eufrosine-de-bulgaria",
        "title": "Eufrósine de Bulgaria",
        "epoca": "Siglo XIII",
        "orden": 8,
        "source": "Eufrósine de Bulgaria.md",
        "wiki": [("en", "Euphrosyne of Bulgaria"), ("bg", "Ефросина")],
        "commons": ["Theodore Svetoslav", "Second Bulgarian Empire"],
    },
    {
        "slug": "eufrosina-de-moscu",
        "title": "Santa Eufrosina de Moscú",
        "epoca": "Siglo XIV",
        "orden": 9,
        "source": "Eufrosina de Moscú.md",
        "wiki": [("en", "Eudoxia of Moscow"), ("ru", "Евдокия Дмитриевна"), ("es", "Eudoxia de Moscú")],
        "commons": ["Eudoxia of Moscow", "Evdokia Dmitrievna", "Saint Eudoxia Moscow"],
    },
    {
        "slug": "euphrosyne-parepa-rosa",
        "title": "Euphrosyne Parepa-Rosa",
        "epoca": "Siglo XIX",
        "orden": 10,
        "source": "Euphrosyne Parepa-Rosa.md",
        "wiki": [("en", "Euphrosyne Parepa-Rosa")],
        "commons": ["Euphrosyne Parepa-Rosa"],
    },
    {
        "slug": "euphrosyne-doxiadis",
        "title": "Euphrosyne Doxiadis",
        "epoca": "Siglo XX",
        "orden": 11,
        "source": "Euphrosyne Doxiadis.md",
        "wiki": [("en", "Euphrosyne Doxiadis"), ("en", "Fayum mummy portraits")],
        "commons": ["Fayum mummy portrait", "Fayum portrait woman"],
    },
    {
        "slug": "eufrosina-cruz-mendoza",
        "title": "Eufrosina Cruz Mendoza",
        "epoca": "Siglo XX",
        "orden": 12,
        "source": "Eufrosina Cruz Mendoza.md",
        "wiki": [("es", "Eufrosina Cruz Mendoza"), ("en", "Eufrosina Cruz")],
        "commons": ["Eufrosina Cruz"],
    },
]


def curl_json(url: str) -> dict | list | None:
    try:
        out = subprocess.check_output(
            ["curl.exe", "-sL", "-A", UA, url],
            timeout=40,
        )
        return json.loads(out.decode("utf-8"))
    except Exception:
        return None


def curl_download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.check_call(
            ["curl.exe", "-sL", "-A", UA, "-o", str(dest), url],
            timeout=60,
        )
        return dest.is_file() and dest.stat().st_size > 1000
    except Exception:
        return False


def wiki_image(lang: str, title: str) -> str | None:
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    data = curl_json(url)
    if not isinstance(data, dict):
        return None
    if data.get("type") == "disambiguation":
        return None
    for key in ("originalimage", "thumbnail"):
        src = (data.get(key) or {}).get("source")
        if src:
            return clean_url(src)
    return None


def clean_url(url: str) -> str:
    url = re.sub(r"\?utm_.*$", "", url)
    # Prefer larger commons thumbs when possible
    url = re.sub(r"/\d+px-", "/1200px-", url)
    return url


def commons_image(query: str) -> str | None:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,
            "gsrlimit": 8,
            "prop": "imageinfo",
            "iiprop": "url|mime|size",
            "iiurlwidth": 1200,
        }
    )
    data = curl_json(f"https://commons.wikimedia.org/w/api.php?{params}")
    if not isinstance(data, dict):
        return None
    pages = (data.get("query") or {}).get("pages") or {}
    best = None
    best_score = -1
    for page in pages.values():
        title = (page.get("title") or "").lower()
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        mime = info.get("mime", "")
        if not mime.startswith("image/") or "svg" in mime:
            continue
        url = info.get("thumburl") or info.get("url")
        if not url:
            continue
        score = info.get("size") or 0
        # Prefer portrait-ish filenames matching person terms
        if any(w in title for w in ("euphros", "eufros", "eudox", "evdoki", "parepa", "cruz")):
            score += 5_000_000
        if score > best_score:
            best_score = score
            best = clean_url(url)
    return best


def find_image(entry: dict) -> str | None:
    for lang, title in entry["wiki"]:
        url = wiki_image(lang, title)
        if url:
            return url
    for q in entry.get("commons", []):
        url = commons_image(q)
        if url:
            return url
    return None


def find_source_file(name: str) -> Path | None:
    direct = SRC / "lista" / name
    if direct.is_file():
        return direct
    # Fuzzy match for encoding issues
    target = name.casefold()
    for p in (SRC / "lista").glob("*.md"):
        if p.name.casefold() == target:
            return p
        # compare without accents roughly
        a = re.sub(r"[^a-z0-9]+", "", p.stem.casefold())
        b = re.sub(r"[^a-z0-9]+", "", Path(name).stem.casefold())
        if a == b:
            return p
    return None


def write_front(path: Path, meta: dict, body: str) -> None:
    lines = ["---"]
    for k, v in meta.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append(body.rstrip() + "\n")
    path.write_text("\n".join(lines), encoding="utf-8")


def strip_existing_h1(body: str) -> str:
    body = body.lstrip()
    if body.startswith("# "):
        first, _, rest = body.partition("\n")
        return rest.lstrip()
    return body


def main() -> None:
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)

    # Protect raw markdown
    (DEST / ".htaccess").write_text(
        "Options -Indexes\n\n"
        "<FilesMatch \"\\.(md|php|html?)$\">\n"
        "    Deny from all\n"
        "</FilesMatch>\n",
        encoding="utf-8",
    )

    nombre = (SRC / "nombre.md").read_text(encoding="utf-8")
    write_front(
        DEST / "nombre.md",
        {"coleccion": "eufrosinas"},
        "# El nombre\n\n" + nombre.strip() + "\n",
    )

    indice_lines = [
        "# Las Eufrosinas",
        "",
        "Mujeres históricas y figuras llamadas Eufrosina, ordenadas desde la Antigüedad hasta hoy.",
        "",
    ]

    for entry in ENTRIES:
        folder = DEST / "lista" / entry["slug"]
        folder.mkdir(parents=True)

        src = find_source_file(entry["source"])
        if src is None:
            raise SystemExit(f"No encuentro fuente: {entry['source']}")
        raw = src.read_text(encoding="utf-8")
        body = strip_existing_h1(raw)

        meta = {
            "coleccion": "eufrosinas",
            "titulo": entry["title"],
            "epoca": entry["epoca"],
            "orden": entry["orden"],
            "imagen": "imagen.jpg",
        }
        write_front(folder / "entrada.md", meta, f"# {entry['title']}\n\n{body}")

        img_url = find_image(entry)
        ok = False
        if img_url:
            ok = curl_download(img_url, folder / "imagen.jpg")
            # fallback without forcing 1200px
            if not ok and "1200px-" in img_url:
                ok = curl_download(img_url.replace("/1200px-", "/800px-"), folder / "imagen.jpg")
        if not ok:
            print(f"WARN sin imagen: {entry['slug']} ({img_url})")
            meta.pop("imagen", None)
            write_front(folder / "entrada.md", meta, f"# {entry['title']}\n\n{body}")
        else:
            print(f"OK {entry['slug']} <- {img_url}")

        excerpt = entry["epoca"]
        indice_lines.append(f"- [{entry['title']}](/eufrosinas/{entry['slug']}) — {excerpt}")

    (DEST / "indice.md").write_text("\n".join(indice_lines) + "\n", encoding="utf-8")
    print("Listo:", DEST)


if __name__ == "__main__":
    main()
