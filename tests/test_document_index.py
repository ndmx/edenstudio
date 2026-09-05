#!/usr/bin/env python3
"""Tests for product-document index extraction, anchors, and exclusions."""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_document_index as bdi  # noqa: E402

FIXTURE = """<!DOCTYPE html>
<html lang="en">
<body class="page-docs">
    <nav class="navbar site-header" id="primary-navigation">
        <a href="../index.html">Home</a>
        <a href="../pages/developer-docs.html">Developer Docs</a>
    </nav>
    <section class="breadcrumb">
        <nav class="breadcrumb-nav">
            <a href="../pages/developer-docs.html">Developer Docs</a>
            <span class="current">Privacy Policy</span>
        </nav>
    </section>
    <section class="doc-header">
        <h1>ParkMemory Hub Privacy Policy</h1>
        <p class="doc-subtitle">How the app stores memories.</p>
        <span class="last-updated">Last reviewed: <time datetime="2026-01-05">January 5, 2026</time></span>
    </section>
    <section class="toc-section">
        <div class="toc-container">
            <h2>Table of Contents</h2>
            <nav class="toc">
                <ol>
                    <li><a href="#overview" class="toc-link">Overview</a></li>
                    <li><a href="#contact" class="toc-link">Contact</a></li>
                </ol>
            </nav>
        </div>
    </section>
    <section class="quick-support">
        <h2>Quick Support</h2>
        <div class="support-actions">
            <a href="#overview">Allow location, set a watch radius, and review nearby reports.</a>
        </div>
    </section>
    <aside class="sidebar doc-sidebar">
        <a href="#overview">Sidebar jump</a>
    </aside>
    <section class="doc-content">
        <div class="doc-body">
            <section id="overview" class="doc-section">
                <h2>1. Overview</h2>
                <p>ParkMemory Hub helps families collect trip memories &amp; plans.</p>
                <p>Sharing is limited to   the circle you create.</p>
            </section>
            <section class="doc-section">
                <h2>Unanchored notes</h2>
                <p>This block has no id and must not receive a generated anchor.</p>
            </section>
            <section id="contact" class="doc-section">
                <h2>2. Contact</h2>
                <p>Email support@edentv.us for help.</p>
            </section>
        </div>
    </section>
    <footer class="footer site-footer">
        <p>Creating tomorrow's digital experiences today.</p>
        <p>&copy; 2026 EdenTV. All rights reserved.</p>
        <a href="parkmemory-privacy.html">Privacy Policy</a>
    </footer>
</body>
</html>
"""

ID_RE = re.compile(r'\sid="([^"]+)"', re.IGNORECASE)


def source_ids(html: str) -> set[str]:
    return set(ID_RE.findall(html))


class FilenameAndDateTests(unittest.TestCase):
    def test_classifies_product_docs(self):
        self.assertEqual(
            bdi.classify_filename("parkmemory-privacy.html"),
            ("parkmemory-privacy", "ParkMemory Hub", "privacy"),
        )
        self.assertEqual(
            bdi.classify_filename("jxl-scheduler-support.html"),
            ("jxl-scheduler-support", "JxL Scheduler", "support"),
        )
        self.assertEqual(
            bdi.classify_filename("pulsetrackr-compliance.html"),
            ("pulsetrackr-compliance", "PulseTrackr", "compliance"),
        )

    def test_excludes_legal_routing_indexes(self):
        for name in bdi.LEGAL_INDEXES:
            self.assertIsNone(bdi.classify_filename(name))
            self.assertIsNone(bdi.parse_document("<h1>Index</h1>", name))

    def test_reviewed_iso_from_english_date(self):
        self.assertEqual(bdi.parse_reviewed("Last reviewed: August 23, 2026"), "2026-08-23")
        self.assertEqual(bdi.parse_reviewed("  Last reviewed: January 5, 2026 "), "2026-01-05")
        self.assertIsNone(bdi.parse_reviewed("Updated yesterday"))

    def test_heading_number_stripped(self):
        self.assertEqual(bdi.heading_title("1. Overview"), "Overview")
        self.assertEqual(bdi.heading_title("10. Contact"), "Contact")
        self.assertEqual(bdi.heading_title("App Store URLs"), "App Store URLs")


class FixtureParserTests(unittest.TestCase):
    def setUp(self):
        self.doc = bdi.parse_document(FIXTURE, "parkmemory-privacy.html")

    def test_core_fields(self):
        self.assertIsNotNone(self.doc)
        self.assertEqual(self.doc["id"], "parkmemory-privacy")
        self.assertEqual(self.doc["product"], "ParkMemory Hub")
        self.assertEqual(self.doc["type"], "privacy")
        self.assertEqual(self.doc["title"], "ParkMemory Hub Privacy Policy")
        self.assertEqual(self.doc["url"], "../docs/parkmemory-privacy.html")
        self.assertEqual(self.doc["reviewed"], "2026-01-05")

    def test_indexes_real_sections_only(self):
        anchors = [section["anchor"] for section in self.doc["sections"]]
        titles = [section["title"] for section in self.doc["sections"]]
        self.assertEqual(anchors, ["overview", "contact"])
        self.assertEqual(titles, ["Overview", "Contact"])

    def test_does_not_invent_anchors(self):
        emitted = {section["anchor"] for section in self.doc["sections"]}
        self.assertTrue(emitted <= source_ids(FIXTURE))
        self.assertNotIn("unanchored-notes", emitted)
        self.assertFalse(any(section["anchor"].startswith("generated") for section in self.doc["sections"]))

    def test_excludes_navigation_toc_quick_links_sidebar_footer(self):
        blob = " ".join(section["title"] + " " + section["text"] for section in self.doc["sections"])
        self.assertNotIn("Table of Contents", blob)
        self.assertNotIn("Quick Support", blob)
        self.assertNotIn("watch radius", blob)
        self.assertNotIn("Sidebar jump", blob)
        self.assertNotIn("All rights reserved", blob)
        self.assertNotIn("digital experiences today", blob)
        self.assertNotIn("Unanchored notes", blob)
        self.assertNotEqual(self.doc["title"], "Home")

    def test_normalizes_entities_and_whitespace(self):
        overview = self.doc["sections"][0]
        self.assertIn("memories & plans", overview["text"])
        self.assertNotIn("&amp;", overview["text"])
        self.assertNotIn("  ", overview["text"])
        self.assertTrue(overview["text"].startswith("ParkMemory Hub helps"))


class ProductDocsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = bdi.iter_product_docs(bdi.DOCS_DIR)
        cls.html_by_name = {path.name: path.read_text(encoding="utf-8") for path in cls.paths}
        cls.documents = bdi.build_index(bdi.DOCS_DIR)
        cls.by_id = {doc["id"]: doc for doc in cls.documents}

    def test_indexes_eleven_product_documents(self):
        self.assertEqual(len(self.paths), 11)
        self.assertEqual(len(self.documents), 11)
        self.assertEqual(
            {path.name for path in self.paths},
            {
                "jxl-scheduler-compliance.html",
                "jxl-scheduler-privacy.html",
                "jxl-scheduler-support.html",
                "parkmemory-compliance.html",
                "parkmemory-privacy.html",
                "parkmemory-support.html",
                "parkmemory-terms.html",
                "pulsetrackr-compliance.html",
                "pulsetrackr-privacy.html",
                "pulsetrackr-support.html",
                "pulsetrackr-terms.html",
            },
        )

    def test_does_not_index_legal_routing_files(self):
        legal_names = {path.name for path in bdi.LEGAL_DIR.glob("*.html")}
        self.assertTrue(bdi.LEGAL_INDEXES <= legal_names)
        indexed_urls = {doc["url"] for doc in self.documents}
        for name in bdi.LEGAL_INDEXES:
            self.assertNotIn(f"../legal/{name}", indexed_urls)
            self.assertNotIn(f"../docs/{name}", indexed_urls)

    def test_required_fields_and_types(self):
        for doc in self.documents:
            self.assertEqual(set(doc), {"id", "product", "type", "title", "url", "reviewed", "sections"})
            self.assertIn(doc["product"], set(bdi.PRODUCT_NAMES.values()))
            self.assertIn(doc["type"], bdi.DOCUMENT_TYPES)
            self.assertTrue(doc["title"])
            self.assertEqual(doc["url"], f"../docs/{doc['id']}.html")
            self.assertRegex(doc["reviewed"], r"^20\d{2}-\d{2}-\d{2}$")
            self.assertTrue(doc["sections"])
            for section in doc["sections"]:
                self.assertEqual(set(section), {"title", "anchor", "text"})
                self.assertTrue(section["title"])
                self.assertTrue(section["anchor"])
                self.assertTrue(section["text"])
                self.assertNotIn(" ", section["anchor"])

    def test_anchors_exist_in_source_and_are_unique(self):
        for doc in self.documents:
            html = self.html_by_name[f"{doc['id']}.html"]
            ids = source_ids(html)
            anchors = [section["anchor"] for section in doc["sections"]]
            self.assertEqual(len(anchors), len(set(anchors)), doc["id"])
            for anchor in anchors:
                self.assertIn(anchor, ids, f"{doc['id']} missing id={anchor}")
                self.assertNotEqual(anchor, "primary-navigation")

    def test_real_docs_exclude_chrome_copy(self):
        for doc in self.documents:
            blob = " ".join(section["title"] + " " + section["text"] for section in doc["sections"])
            self.assertNotIn("Table of Contents", blob)
            self.assertNotIn("Quick Support", blob)
            self.assertNotIn("All rights reserved", blob)
            self.assertNotIn("Creating tomorrow's digital experiences today", blob)
            self.assertNotIn("Allow location, set a watch radius, and review nearby reports.", blob)

    def test_reviewed_date_matches_source(self):
        for doc in self.documents:
            html = self.html_by_name[f"{doc['id']}.html"]
            iso = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})">', html)
            visible = re.search(
                r"Last reviewed:\s*(?:<time[^>]*>)?([A-Za-z]+ \d{1,2}, \d{4})",
                html,
            )
            self.assertTrue(iso or visible, doc["id"])
            if iso:
                self.assertEqual(doc["reviewed"], iso.group(1))
            if visible:
                self.assertEqual(doc["reviewed"], bdi.parse_reviewed("Last reviewed: " + visible.group(1)))

    def test_known_section_content(self):
        privacy = self.by_id["parkmemory-privacy"]
        overview = next(section for section in privacy["sections"] if section["anchor"] == "overview")
        self.assertEqual(overview["title"], "Overview")
        self.assertIn("on-device storage", overview["text"])
        self.assertIn("no Firebase dependency", overview["text"])

        pulse = self.by_id["pulsetrackr-privacy"]
        sos = next(section for section in pulse["sections"] if section["anchor"] == "sos")
        self.assertEqual(sos["title"], "SOS and Trusted Contacts")
        self.assertIn("Keychain", sos["text"])

        urls = next(
            section
            for section in self.by_id["pulsetrackr-compliance"]["sections"]
            if section["anchor"] == "urls"
        )
        self.assertEqual(urls["title"], "App Store URLs")
        self.assertIn("https://edentv.us/docs/pulsetrackr-privacy.html#choices", urls["text"])

    def test_written_index_round_trip(self):
        built = bdi.build_index(bdi.DOCS_DIR)
        if bdi.OUTPUT_PATH.exists():
            payload = json.loads(bdi.OUTPUT_PATH.read_text(encoding="utf-8"))
            self.assertEqual(payload["documents"], built)


if __name__ == "__main__":
    unittest.main()
