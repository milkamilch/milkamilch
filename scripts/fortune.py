"""Renders today's fortune as a small terminal SVG.

Usage: python3 scripts/fortune.py <out.svg> [YYYY-MM-DD]
Fortunes live in fortunes.txt next to this script, separated by lines with a single "%".
"""

import datetime
import os
import random
import sys
import textwrap
from xml.sax.saxutils import escape

BG = "#0d1117"
FG = "#e6fce6"
ACCENT = "#39ff14"
DIM = "#7d8590"

WIDTH = 860
WRAP = 92


def pick(day):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fortunes.txt")
    with open(path, encoding="utf-8") as f:
        fortunes = [s.strip() for s in f.read().split("\n%\n") if s.strip()]
    # Fixed shuffle, then one per day: no repeats until the list is through.
    random.Random(42).shuffle(fortunes)
    return fortunes[day.toordinal() % len(fortunes)]


def render(day):
    lines = textwrap.wrap(pick(day), WRAP)
    line_h = 20
    height = 56 + len(lines) * line_h + 10
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" '
        f'font-family="\'JetBrains Mono\', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" '
        f'style="font-variant-ligatures: none; font-feature-settings: \'liga\' 0, \'calt\' 0">',
        f"<title>fortune of the day ({day})</title>",
        f'<rect width="100%" height="100%" rx="10" fill="{BG}" stroke="#30363d"/>',
        f'<text x="24" y="34" fill="{ACCENT}">lars@dortmund<tspan fill="{DIM}">:~$ </tspan><tspan fill="{FG}">fortune</tspan></text>',
    ]
    for i, line in enumerate(lines):
        out.append(f'<text x="24" y="{62 + i * line_h}" fill="{FG}" xml:space="preserve">{escape(line)}</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    out_path = sys.argv[1]
    day = datetime.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else datetime.datetime.now(datetime.timezone.utc).date()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render(day))


if __name__ == "__main__":
    main()
