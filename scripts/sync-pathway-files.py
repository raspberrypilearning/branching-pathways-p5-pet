#!/usr/bin/env python3
"""Synchronise project-format copies from the named Markdown pages."""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / 'en'
check = argparse.ArgumentParser()
check.add_argument('--check', action='store_true')
args = check.parse_args()
files = re.findall(r'^        file: (.+)$', (EN / 'pathways.yml').read_text(), re.M)
copies = [(EN / filename, EN / f'step_{index}.md') for index, filename in enumerate(files, 1)]
copies += [(ROOT / 'starters/pet.py', EN / dest) for dest in ['resources/pet.py', 'code/p5-pet-starter/main.py']]
copies += [(ROOT / 'assets/pet-maker.svg', EN / 'images/banner.svg')]
for source, destination in copies:
    if args.check:
        assert destination.read_bytes() == source.read_bytes(), f'Out of sync: {destination.name}'
    else:
        destination.write_bytes(source.read_bytes())
print(f'{"Checked" if args.check else "Synced"} {len(copies)} project files')
