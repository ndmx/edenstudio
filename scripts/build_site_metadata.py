"""Refresh canonical URLs and document metadata without inventing review dates."""
from datetime import datetime
from html import unescape
from pathlib import Path
import json
import re
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://edentv.us"
HUB = ORIGIN + "/pages/developer-docs"


def canonical(path):
    relative = path.relative_to(ROOT).as_posix()
    return ORIGIN + ("/" if relative == "index.html" else "/" + relative.removesuffix(".html"))


def plain(value):
    return unescape(re.sub(r"<[^>]+>", "", value)).strip()


def refresh(path):
    html = path.read_text()
    html = re.sub(r"Developer [Dd]ocs", "Documents &amp; Support", html)
    html = re.sub(r'(class="nav-link[^"]*"[^>]*>)Documents &amp; Support', r'\1Documents', html)
    html = re.sub(r'styles\.css\?v=[^"\s]+', 'styles.css?v=20260905', html)
    html = re.sub(r'<link\b[^>]*rel="canonical"[^>]*>\s*', '', html)
    html = re.sub(r'\s*<!-- generated site metadata -->.*?<!-- /generated site metadata -->', '', html, flags=re.S)
    url = canonical(path)
    metadata = '<link rel="canonical" href="' + url + '">'
    if path.parent.name in {"docs", "legal"} or path.name == "developer-docs.html":
        title = plain(re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.S)[1])
        description = re.search(r'<meta name="description" content="([^"]*)"', html)
        page = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title,
                "inLanguage": "en", "publisher": {"@type": "Organization", "name": "EdenTV", "url": ORIGIN + "/"}}
        if description:
            page["description"] = unescape(description[1])
        reviewed = re.search(r'Last reviewed:\s*(?:<time[^>]*>)?([A-Za-z]+ \d{1,2}, \d{4})', html)
        if reviewed:
            date = datetime.strptime(reviewed[1], "%B %d, %Y").date().isoformat()
            page["lastReviewed"] = date
            html = re.sub(r'(Last reviewed:\s*)([A-Za-z]+ \d{1,2}, \d{4})',
                          lambda m: m[1] + f'<time datetime="{date}">{m[2]}</time>', html)
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"}]
        if url != HUB:
            crumbs.append({"@type": "ListItem", "position": 2, "name": "Documents & Support", "item": HUB})
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": title, "item": url})
        graph = {"@context": "https://schema.org", "@graph": [page, {"@type": "BreadcrumbList", "itemListElement": crumbs}]}
        metadata += '\n<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False).replace("<", "\\u003c") + '</script>'
        html = html.replace('<nav class="breadcrumb-nav">', '<nav class="breadcrumb-nav" aria-label="Breadcrumb">')
        # Existing product breadcrumb destinations all used the same generic anchor.
        if path.parent.name == "docs":
            product = "pulsetrackr" if path.stem.startswith("pulsetrackr") else "jxl" if path.stem.startswith("jxl") else "parkmemory"
            html = html.replace('developer-docs.html#app-docs', f'developer-docs.html#{product}-docs')
    html = re.sub(r'\s*</head>', lambda _: '\n<!-- generated site metadata -->\n' + metadata + '\n<!-- /generated site metadata -->\n</head>', html)
    path.write_text(html)
    return url


def main():
    paths = [ROOT / "index.html"] + sorted(p for folder in ("pages", "docs", "legal") for p in (ROOT / folder).glob("*.html"))
    urls = [refresh(path) for path in paths]
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    sitemap = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    for url in urls:
        entry = ET.SubElement(sitemap, 'url')
        ET.SubElement(entry, 'loc').text = url
    ET.indent(sitemap)
    ET.ElementTree(sitemap).write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    print(f'Refreshed metadata for {len(urls)} pages and sitemap.xml')


if __name__ == '__main__':
    main()
