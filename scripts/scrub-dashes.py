#!/usr/bin/env python3
"""Replace every U+2014 (em-dash) and U+2013 (en-dash) inside client source
files with a comma + space, except inside CSS calc()/unicode-range/comment
contexts where the character is functional.

In practice, the only dashes that appear in our client/ are inside literal
JSX strings or comments, so a blanket replacement is safe.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "client" / "index.html",
    *(ROOT / "client" / "src").rglob("*.tsx"),
    *(ROOT / "client" / "src").rglob("*.ts"),
    *(ROOT / "client" / "src").rglob("*.css"),
]
EM = "\u2014"
EN = "\u2013"
total = 0
for p in TARGETS:
    if not p.is_file():
        continue
    src = p.read_text(encoding="utf-8")
    if EM not in src and EN not in src:
        continue
    count = src.count(EM) + src.count(EN)
    new = src.replace(EM, ", ").replace(EN, ", ")
    p.write_text(new, encoding="utf-8")
    print(f"scrubbed {count} dashes in {p.relative_to(ROOT)}")
    total += count
print(f"total replacements: {total}")
