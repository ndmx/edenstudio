"""Integrity checks for public documents, deep links, and discovery metadata."""
from html.parser import HTMLParser
from pathlib import Path
import json
import unittest
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.links = []
        self.canonicals = []
        self.h1s = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs['href'])
        if tag == 'h1':
            self.h1s += 1


class DocumentSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = sorted((ROOT / 'docs').glob('*.html')) + sorted((ROOT / 'legal').glob('*.html')) + [ROOT / 'pages/developer-docs.html']
        cls.pages = {p: Page(p) for p in cls.paths}

    def test_unique_ids_and_single_heading(self):
        for path, page in self.pages.items():
            with self.subTest(page=path.name):
                self.assertEqual(len(page.ids), len(set(page.ids)))
                self.assertEqual(page.h1s, 1)

    def test_local_destinations_and_fragments_exist(self):
        for path, page in self.pages.items():
            for href in page.links:
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                target = (ROOT / url.path.lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path)).resolve() if url.path else path
                if target.is_dir():
                    target /= 'index.html'
                with self.subTest(page=path.name, href=href):
                    self.assertTrue(target.is_file(), str(target))
                    if url.fragment and target.is_file() and target.suffix == '.html':
                        self.assertIn(unquote(url.fragment), Page(target).ids)

    def test_canonical_urls_match_sitemap(self):
        tree = ET.parse(ROOT / 'sitemap.xml')
        urls = [node.text for node in tree.findall('.//{*}loc')]
        self.assertEqual(len(urls), len(set(urls)))
        for path, page in self.pages.items():
            with self.subTest(page=path.name):
                self.assertEqual(len(page.canonicals), 1)
                self.assertIn(page.canonicals[0], urls)
                self.assertFalse(page.canonicals[0].endswith('.html'))

    def test_reviewed_dates_and_jsonld(self):
        import re
        for path in self.paths:
            text = path.read_text()
            blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
            self.assertEqual(len(blocks), 1, path.name)
            graph = json.loads(blocks[0])['@graph']
            if path.parent.name == 'docs':
                self.assertEqual(graph[0]['lastReviewed'], '2026-08-23')
                self.assertIn('<time datetime="2026-08-23">August 23, 2026</time>', text)
            self.assertNotIn('dateModified', graph[0])

    def test_search_preserves_block_boundaries_and_inline_words(self):
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        from build_document_index import parse_document
        html = '<h1>PulseTrackr Support</h1><span class="last-updated">Last reviewed: August 23, 2026</span><section id="help" class="doc-section"><h2>Help</h2><p>First paragraph.</p><p>Second con<strong>tact</strong>.</p><p>Line<br>break.</p></section>'
        doc = parse_document(html, 'pulsetrackr-support.html')
        self.assertEqual(doc['sections'][0]['text'], 'First paragraph. Second contact. Line break.')

    def test_malformed_product_document_fails_the_build(self):
        import sys
        import tempfile
        sys.path.insert(0, str(ROOT / 'scripts'))
        from build_document_index import build_index
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'pulsetrackr-support.html').write_text('<h1>Missing content</h1>')
            with self.assertRaisesRegex(ValueError, 'pulsetrackr-support.html'):
                build_index(Path(directory))


if __name__ == '__main__':
    unittest.main()
