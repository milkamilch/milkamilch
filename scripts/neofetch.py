"""Renders a neofetch-style SVG card from live GitHub data.

Usage: python3 scripts/neofetch.py <out.svg>
Reads GITHUB_TOKEN if set (higher rate limit); works without it.
"""

import datetime
import json
import os
import sys
import urllib.request
from xml.sax.saxutils import escape

USER = "milkamilch"

# Languages that only say "there was a web page" — not what the projects are built in.
IGNORED_LANGUAGES = {"HTML", "CSS", "Dockerfile", "Shell", "PowerShell", "Batchfile", "Procfile", "Makefile",
                     "Cython", "C", "GoTemplate"}

# The profile repo, and a team hackathon repo that is not mostly mine.
IGNORED_REPOS = {USER, "LLMhackatron"}

STATIC_LINES = [
    ("OS", "Arch Linux (btw) · Hyprland"),
    ("Host", "Zolitron — Backend Dev"),
    ("Kernel", "M.Sc. Wirtschaftsinformatik (compiling…)"),
    ("Shell", "Java 25 · Spring Boot · Python"),
    ("Solver", "OR-Tools, routing garbage trucks"),
    ("Bugs", "fixed: many · introduced: also many"),
]

BG = "#0d1117"
FG = "#e6fce6"
ACCENT = "#39ff14"
DIM = "#7d8590"

ARCH_LOGO = r"""
                  -`
                 .o+`
                `ooo/
               `+oooo:
              `+oooooo:
              -+oooooo+:
            `/:-:++oooo+:
           `/++++/+++++++:
          `/++++++++++++++:
         `/+++ooooooooooooo/`
        ./ooosssso++osssssso+`
       .oossssso-````/ossssss+`
      -osssssso.      :ssssssso.
     :osssssss/        osssso+++.
    /ossssssss/        +ssssooo/-
  `/ossssso+/:-        -:/+osssso+-
 `+sso+:-`                 `.-/+oso:
`++:.                           `-/+/
""".strip("\n").split("\n")


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": USER})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def collect():
    user = get(f"https://api.github.com/users/{USER}")
    repos = [r for r in get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in repos)
    languages = {}
    for r in repos:
        if r["name"] in IGNORED_REPOS:
            continue
        # Every repo weighs the same, so a committed virtualenv cannot drown out the rest.
        sizes = {k: v for k, v in get(r["languages_url"]).items() if k not in IGNORED_LANGUAGES}
        repo_total = sum(sizes.values())
        for lang, size in sizes.items():
            languages[lang] = languages.get(lang, 0) + size / repo_total
    commits = get(f"https://api.github.com/search/commits?q=author:{USER}")["total_count"]
    created = datetime.datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
    return {
        "repos": len([r for r in repos if r["name"] != USER]),
        "stars": stars,
        "followers": user["followers"],
        "commits": commits,
        "created": created,
        "languages": sorted(languages.items(), key=lambda kv: -kv[1])[:5],
    }


def uptime(created, now):
    days = (now - created).days
    years, days = divmod(days, 365)
    return f"{years} years, {days} days" if years else f"{days} days"


def render(data, now):
    rows = [("", f"{USER}@github", ACCENT), ("", "─" * 38, DIM)]
    rows += [(k, v, FG) for k, v in STATIC_LINES]
    rows += [
        ("Uptime", uptime(data["created"], now), FG),
        ("Packages", f"{data['repos']} public repos · {data['stars']} ★", FG),
        ("Commits", f"{data['commits']:,} (public, all time)", FG),
        ("Followers", f"{data['followers']} (hi mom)", FG),
    ]

    line_h = 20
    top = 40
    left_x = 28
    right_x = 360
    width = 860
    height = top + max(len(ARCH_LOGO), len(rows) + 4) * line_h + 20

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'font-family="\'JetBrains Mono\', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" '
        f'style="font-variant-ligatures: none; font-feature-settings: \'liga\' 0, \'calt\' 0">',
        f'<title>neofetch for {USER}</title>',
        f'<rect width="100%" height="100%" rx="10" fill="{BG}" stroke="#30363d"/>',
    ]

    for i, line in enumerate(ARCH_LOGO):
        y = top + i * line_h
        out.append(f'<text x="{left_x}" y="{y}" fill="{ACCENT}" xml:space="preserve">{escape(line)}</text>')

    for i, (key, value, color) in enumerate(rows):
        y = top + i * line_h
        if key:
            out.append(
                f'<text x="{right_x}" y="{y}" xml:space="preserve">'
                f'<tspan fill="{ACCENT}" font-weight="bold">{escape(key)}</tspan>'
                f'<tspan fill="{DIM}">: </tspan><tspan fill="{color}">{escape(value)}</tspan></text>'
            )
        else:
            out.append(f'<text x="{right_x}" y="{y}" fill="{color}" font-weight="bold">{escape(value)}</text>')

    # Language bar
    y = top + (len(rows) + 1) * line_h
    total = sum(size for _, size in data["languages"]) or 1
    bar_w = width - right_x - 40
    x = right_x
    palette = [ACCENT, "#2ea043", "#a5d6a7", "#56d364", "#1b4721"]
    out.append(f'<text x="{right_x}" y="{y - 6}" fill="{ACCENT}" font-weight="bold">Languages<tspan fill="{DIM}"> (share per repo):</tspan></text>')
    for (lang, size), color in zip(data["languages"], palette):
        w = bar_w * size / total
        out.append(f'<rect x="{x:.1f}" y="{y + 2}" width="{w:.1f}" height="8" fill="{color}"/>')
        x += w
    legend_y = y + 30
    x = right_x
    for (lang, size), color in zip(data["languages"], palette):
        label = f"{lang} {100 * size / total:.0f}%"
        label_w = 14 + len(label) * 7.5 + 14
        if x + label_w > width - 20:
            x = right_x
            legend_y += line_h
        out.append(f'<rect x="{x}" y="{legend_y - 9}" width="9" height="9" rx="2" fill="{color}"/>')
        out.append(f'<text x="{x + 14}" y="{legend_y}" fill="{FG}" font-size="12">{escape(label)}</text>')
        x += label_w

    # Terminal color blocks, like the real thing
    y = legend_y + 22
    for i, color in enumerate(["#0d1117", "#ff7b72", ACCENT, "#e3b341", "#79c0ff", "#d2a8ff", "#56d4dd", FG]):
        out.append(f'<rect x="{right_x + i * 26}" y="{y}" width="24" height="12" fill="{color}" stroke="#30363d"/>')

    out.append(
        f'<text x="{width - 20}" y="{height - 12}" fill="{DIM}" font-size="10" text-anchor="end">'
        f'refreshed {now:%Y-%m-%d} by a GitHub Action</text>'
    )
    out.append("</svg>")
    return "\n".join(out)


def main():
    out_path = sys.argv[1]
    now = datetime.datetime.now(datetime.timezone.utc)
    svg = render(collect(), now)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
