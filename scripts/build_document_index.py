#!/usr/bin/env python3
"""Build a lightweight search index from product documents in docs/.

Reads the 11 product HTML files, extracts real section anchors with
html.parser, and writes assets/document-index.json for the documents hub.
Excludes legal routing indexes and page chrome (nav, footer, TOC, quick
links, sidebar). Does not invent anchors that are absent from the HTML.
"""

from __future__ import annotations

import calendar
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
LEGAL_DIR = ROOT / "legal"
OUTPUT_PATH = ROOT / "assets" / "document-index.json"

DOCUMENT_TYPES = ("privacy", "terms", "support", "compliance")
PRODUCT_NAMES = {
    "parkmemory": "ParkMemory Hub",
    "jxl-scheduler": "JxL Scheduler",
    "pulsetrackr": "PulseTrackr",
}
LEGAL_INDEXES = {
    "privacy-policy.html",
    "terms-of-service.html",
    "app-store-compliance.html",
    "support.html",
}

SKIP_TAGS = frozenset({"nav", "footer", "script", "style", "noscript", "template"})
SKIP_CLASSES = frozenset(
    {
        "breadcrumb",
        "breadcrumb-nav",
        "toc-section",
        "toc-container",
        "toc",
        "quick-support",
        "support-actions",
        "quick-links",
        "quick-nav",
        "sidebar",
        "doc-sidebar",
        "site-sidebar",
        "navbar",
        "site-header",
        "site-footer",
    }
)
VOID_TAGS = frozenset(
    {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
)
HEADING_TAGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
BLOCK_TAGS = frozenset({"p", "div", "section", "li", "ul", "ol", "table", "tr", "td", "th", "blockquote"}) | HEADING_TAGS
WHITESPACE_RE = re.compile(r"\s+")
NUMBERED_HEADING_RE = re.compile(r"^\d+\.\s+")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REVIEWED_RE = re.compile(
    r"Last reviewed:\s*([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})",
    re.IGNORECASE,
)
MONTH_NUMBERS = {
    name.lower(): index
    for index, name in enumerate(calendar.month_name)
    if name
}


def normalize_space(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def heading_title(text: str) -> str:
    return NUMBERED_HEADING_RE.sub("", normalize_space(text))


def parse_reviewed(text: str) -> str | None:
    match = REVIEWED_RE.search(normalize_space(text))
    if not match:
        return None
    month = MONTH_NUMBERS.get(match.group(1).lower())
    if not month:
        return None
    day = int(match.group(2))
    year = int(match.group(3))
    return f"{year:04d}-{month:02d}-{day:02d}"


def classify_filename(filename: str) -> tuple[str, str, str] | None:
    name = Path(filename).name
    if name in LEGAL_INDEXES:
        return None
    stem = Path(name).stem
    for doc_type in DOCUMENT_TYPES:
        suffix = f"-{doc_type}"
        if stem.endswith(suffix):
            product_slug = stem[: -len(suffix)]
            product = PRODUCT_NAMES.get(product_slug)
            if not product:
                return None
            return stem, product, doc_type
    return None


def _class_set(attrs: dict[str, str]) -> set[str]:
    return set((attrs.get("class") or "").split())


class DocumentParser(HTMLParser):
    """Extract document title, reviewed date, and id'd doc-section bodies."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.reviewed = None
        self.sections: list[dict[str, str]] = []
        self.seen_ids: list[str] = []
        self._skip = 0
        self._depth = 0
        self._capture_title = False
        self._capture_reviewed = False
        self._capture_heading = False
        self._title_parts: list[str] = []
        self._reviewed_parts: list[str] = []
        self._heading_parts: list[str] = []
        self._text_parts: list[str] = []
        self._section_anchor: str | None = None
        self._section_depth: int | None = None
        self._reviewed_depth: int | None = None
        self._seen_anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: (value or "") for key, value in attrs}
        element_id = attr_map.get("id")
        if element_id:
            self.seen_ids.append(element_id)

        if not self._skip and self._section_anchor and (tag in BLOCK_TAGS or tag == "br"):
            self._text_parts.append(" ")
        if tag in VOID_TAGS:
            return

        classes = _class_set(attr_map)
        starts_skip = tag in SKIP_TAGS or bool(classes & SKIP_CLASSES)
        if self._skip or starts_skip:
            self._skip += 1
            return

        self._depth += 1

        if not self.title and tag == "h1":
            self._capture_title = True
            self._title_parts = []

        if self.reviewed is None and "last-updated" in classes:
            self._capture_reviewed = True
            self._reviewed_depth = self._depth
            self._reviewed_parts = []

        if self._capture_reviewed and tag == "time":
            datetime_attr = (attr_map.get("datetime") or "").strip()
            if ISO_DATE_RE.match(datetime_attr):
                self.reviewed = datetime_attr

        if (
            self._section_anchor is None
            and "doc-section" in classes
            and element_id
            and element_id not in self._seen_anchors
        ):
            self._section_anchor = element_id
            self._section_depth = self._depth
            self._heading_parts = []
            self._text_parts = []
            self._capture_heading = False

        if self._section_anchor and not self._heading_parts and tag in HEADING_TAGS:
            self._capture_heading = True

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_TAGS:
            return

        if self._skip:
            self._skip -= 1
            return

        if self._capture_title and tag == "h1":
            self.title = normalize_space("".join(self._title_parts))
            self._capture_title = False

        if self._capture_reviewed and self._depth == self._reviewed_depth:
            if self.reviewed is None:
                self.reviewed = parse_reviewed("".join(self._reviewed_parts))
            self._capture_reviewed = False
            self._reviewed_depth = None

        if self._capture_heading and tag in HEADING_TAGS:
            self._capture_heading = False

        if self._section_anchor and tag in BLOCK_TAGS:
            self._text_parts.append(" ")

        if (
            self._section_anchor is not None
            and tag == "section"
            and self._depth == self._section_depth
        ):
            self._finish_section()

        self._depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        if self._capture_title:
            self._title_parts.append(data)
        if self._capture_reviewed:
            self._reviewed_parts.append(data)
        if self._section_anchor is None:
            return
        if self._capture_heading:
            self._heading_parts.append(data)
            return
        if self._heading_parts:
            self._text_parts.append(data)

    def close(self) -> None:
        super().close()
        if self._section_anchor is not None:
            self._finish_section()

    def _finish_section(self) -> None:
        anchor = self._section_anchor or ""
        title = heading_title("".join(self._heading_parts))
        text = normalize_space("".join(self._text_parts))
        self._section_anchor = None
        self._section_depth = None
        self._capture_heading = False
        self._heading_parts = []
        self._text_parts = []
        if not anchor or anchor in self._seen_anchors:
            return
        if not title and not text:
            return
        self._seen_anchors.add(anchor)
        self.sections.append({"title": title, "anchor": anchor, "text": text})


def parse_document(html: str, filename: str) -> dict | None:
    classified = classify_filename(filename)
    if classified is None:
        return None

    doc_id, product, doc_type = classified
    parser = DocumentParser()
    parser.feed(html)
    parser.close()
    if not parser.title or not parser.reviewed or not parser.sections:
        return None

    return {
        "id": doc_id,
        "product": product,
        "type": doc_type,
        "title": parser.title,
        "url": f"../docs/{Path(filename).name}",
        "reviewed": parser.reviewed,
        "sections": parser.sections,
    }


def existing_ids(html: str) -> set[str]:
    parser = DocumentParser()
    parser.feed(html)
    parser.close()
    return set(parser.seen_ids)


def iter_product_docs(docs_dir: Path) -> list[Path]:
    files = []
    for path in sorted(docs_dir.glob("*.html")):
        if classify_filename(path.name):
            files.append(path)
    return files


def build_index(docs_dir: Path) -> list[dict]:
    documents = []
    for path in iter_product_docs(docs_dir):
        document = parse_document(path.read_text(encoding="utf-8"), path.name)
        if not document:
            raise ValueError(f"Cannot index {path.name}: title, reviewed date, and anchored document sections are required")
        documents.append(document)
    type_rank = {name: index for index, name in enumerate(DOCUMENT_TYPES)}
    product_rank = {name: index for index, name in enumerate(PRODUCT_NAMES.values())}
    documents.sort(key=lambda item: (product_rank.get(item["product"], 99), type_rank.get(item["type"], 99), item["id"]))
    return documents


def write_index(path: Path, documents: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"documents": documents}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    documents = build_index(DOCS_DIR)
    write_index(OUTPUT_PATH, documents)
    print(f"Wrote {len(documents)} documents ({sum(len(doc['sections']) for doc in documents)} sections) to {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
