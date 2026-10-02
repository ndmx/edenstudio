"""Contract checks for cards, consistent iOS documents, and static routing."""
import sys
import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from app_documents import APPS, TYPES

class Cards(HTMLParser):
    def __init__(self):
        super().__init__(); self.cards=[]; self.current=None
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='article': self.current=[]
        if tag=='a' and self.current is not None:self.current.append(attrs.get('href'))
    def handle_endtag(self,tag):
        if tag=='article':self.cards.append(self.current);self.current=None

class AppNavigationTests(unittest.TestCase):
    def test_every_card_has_an_action(self):
        p=Cards();p.feed((ROOT/'pages/apps.html').read_text())
        self.assertEqual(len(p.cards),20)
        self.assertTrue(all(p.cards))
    def test_ios_cards_and_overviews_link_all_documents(self):
        cards=(ROOT/'pages/apps.html').read_text()
        hub=(ROOT/'pages/developer-docs.html').read_text()
        for slug,(_,anchor,_) in APPS.items():
            overview=(ROOT/'pages'/f'{slug}.html').read_text()
            self.assertIn(f'href="/pages/{slug}"',cards)
            self.assertIn(f'id="{anchor}"',hub)
            for kind in TYPES:
                self.assertTrue((ROOT/'docs'/f'{slug}-{kind}.html').is_file())
                for text in [cards,hub,overview]: self.assertIn(f'/docs/{slug}-{kind}',text)
    def test_explicit_routes_and_404(self):
        self.assertIn('noindex',(ROOT/'404.html').read_text())
        routes=(ROOT/'_redirects').read_text().splitlines()
        self.assertIn('/apps /pages/apps 301',routes)
        for row in routes:
            source,target,status=row.split()
            self.assertEqual(status,'301')
            self.assertNotEqual(source,target)
            self.assertTrue((ROOT/(target.lstrip('/')+'.html')).is_file())
