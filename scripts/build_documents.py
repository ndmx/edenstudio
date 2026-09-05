"""Rebuild document routing pages, metadata, and the public search index."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
for script in ('build_document_hubs.py', 'build_site_metadata.py', 'build_document_index.py'):
    subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], cwd=ROOT, check=True)
