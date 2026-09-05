# -*- coding: utf-8 -*-
"""Busca miniaturas de Wikipedia/Wikimedia para cada Eufrosina."""
from __future__ import annotations

import json
import urllib.parse
import urllib.request

FIGURES = [
    ("eufrosine", [("en", "Euphrosyne"), ("es", "Eufrósine")]),
    ("eufrosina-de-alejandria", [("en", "Euphrosyne of Alexandria"), ("es", "Eufrosina de Alejandría")]),
    ("eufrosina-emperatriz-bizantina", [("en", "Euphrosyne (9th century)"), ("ca", "Eufrosina (esposa de Miquel II)"), ("en", "Euphrosyne Doukaina Kamatera")]),
    ("eufrosina-de-polatsk", [("en", "Euphrosyne of Polotsk"), ("es", "Eufrosina de Pólatsk")]),
    ("eufrosina-de-kiev", [("en", "Euphrosyne of Kiev"), ("es", "Eufrosina de Kiev")]),
    ("eufrosina-ducena-camatera", [("en", "Euphrosyne Doukaina Kamatera"), ("es", "Eufrosina Ducena Camatera")]),
    ("eufrosyne-of-masovia", [("en", "Euphrosyne of Masovia")]),
    ("eufrosine-de-bulgaria", [("en", "Irene of Bulgaria, Empress of Byzantium"), ("en", "Euphrosyne of Bulgaria")]),
    ("eufrosina-de-moscu", [("en", "Eudoxia of Moscow"), ("ru", "Евдокия Дмитриевна"), ("es", "Eufrosina de Moscú")]),
    ("euphrosyne-parepa-rosa", [("en", "Euphrosyne Parepa-Rosa")]),
    ("euphrosyne-doxiadis", [("en", "Euphrosyne Doxiadis")]),
    ("eufrosina-cruz-mendoza", [("es", "Eufrosina Cruz Mendoza"), ("en", "Eufrosina Cruz")]),
]

UA = "EufrosinaBlog/1.0 (personal memorial site; contact via local project)"


def get_summary(lang: str, title: str) -> dict:
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.load(r)
    except Exception as e:
        return {"error": str(e)}


def commons_search(query: str) -> str | None:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,
            "gsrlimit": 5,
            "prop": "imageinfo",
            "iiprop": "url|mime|size",
            "iiurlwidth": 1200,
        }
    )
    url = f"https://commons.wikimedia.org/w/api.php?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.load(r)
    except Exception:
        return None
    pages = (data.get("query") or {}).get("pages") or {}
    for page in pages.values():
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        mime = info.get("mime", "")
        if not mime.startswith("image/") or mime == "image/svg+xml":
            continue
        return info.get("thumburl") or info.get("url")
    return None


def main() -> None:
    for slug, candidates in FIGURES:
        found = None
        source = None
        for lang, title in candidates:
            data = get_summary(lang, title)
            if data.get("error"):
                continue
            thumb = (data.get("originalimage") or {}).get("source") or (data.get("thumbnail") or {}).get("source")
            if thumb:
                found = thumb
                source = f"{lang}:{data.get('title')}"
                break
        if not found:
            found = commons_search(candidates[0][1])
            source = f"commons:{candidates[0][1]}" if found else None
        print(f"{slug}\t{found or 'NO_IMAGE'}\t{source or ''}")


if __name__ == "__main__":
    main()
