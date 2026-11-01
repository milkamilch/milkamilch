"""Renders today's garbage-truck tour as an animated SVG.

Usage: python3 scripts/route.py <out.svg> [YYYY-MM-DD]
The date seeds the instance, so every day gets a new map and the same day always the same one.
"""

import datetime
import math
import random
import sys
import time

BG = "#0d1117"
FG = "#e6fce6"
ACCENT = "#39ff14"
DIM = "#7d8590"
GRID = "#1c2430"

WIDTH = 860
MAP_TOP = 70
MAP_H = 300
MAP_X0, MAP_X1 = 40, WIDTH - 40
STOPS = 16
KM_PER_PX = 0.05
LOOP_S = 14  # one full tour incl. the pause at the depot
DRIVE_SHARE = 0.85


def instance(rng):
    depot = (MAP_X0 + 30, MAP_TOP + MAP_H / 2)
    stops = []
    while len(stops) < STOPS:
        p = (rng.uniform(MAP_X0 + 90, MAP_X1 - 10), rng.uniform(MAP_TOP + 15, MAP_TOP + MAP_H - 15))
        if all(math.dist(p, q) > 45 for q in stops):
            stops.append(p)
    return depot, stops


def tour_length(points, order):
    return sum(math.dist(points[a], points[b]) for a, b in zip(order, order[1:]))


def nearest_neighbour(points):
    order, left = [0], set(range(1, len(points)))
    while left:
        nxt = min(left, key=lambda i: math.dist(points[order[-1]], points[i]))
        order.append(nxt)
        left.remove(nxt)
    return order + [0]


def two_opt(points, order):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(order) - 2):
            for j in range(i + 1, len(order) - 1):
                a, b, c, d = points[order[i - 1]], points[order[i]], points[order[j]], points[order[j + 1]]
                if math.dist(a, c) + math.dist(b, d) < math.dist(a, b) + math.dist(c, d) - 1e-9:
                    order[i:j + 1] = reversed(order[i:j + 1])
                    improved = True
    return order


def render(day):
    rng = random.Random(day.isoformat())
    depot, stops = instance(rng)
    points = [depot] + stops

    start = time.perf_counter()
    nn = nearest_neighbour(points)
    nn_km = tour_length(points, nn) * KM_PER_PX
    best = two_opt(points, list(nn))
    solve_ms = (time.perf_counter() - start) * 1000
    best_km = tour_length(points, best) * KM_PER_PX

    # Where along the tour (0..1 of the loop) the truck reaches each stop.
    total = tour_length(points, best)
    arrival, run = {}, 0.0
    for a, b in zip(best, best[1:]):
        run += math.dist(points[a], points[b])
        arrival.setdefault(b, run / total * DRIVE_SHARE)

    path = "M " + " L ".join(f"{points[i][0]:.1f},{points[i][1]:.1f}" for i in best)
    height = MAP_TOP + MAP_H + 70
    saved = 100 * (nn_km - best_km) / nn_km if nn_km else 0
    verdict = f"2-opt saves {saved:.0f}%" if saved >= 0.5 else "2-opt found nothing to improve"

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" '
        f'font-family="\'JetBrains Mono\', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" '
        f'style="font-variant-ligatures: none; font-feature-settings: \'liga\' 0, \'calt\' 0">',
        f"<title>Today's garbage truck tour ({day})</title>",
        f'<rect width="100%" height="100%" rx="10" fill="{BG}" stroke="#30363d"/>',
        f'<text x="24" y="36" fill="{ACCENT}">lars@dortmund<tspan fill="{DIM}">:~$ </tspan>'
        f'<tspan fill="{FG}">./route --stops {STOPS} --seed {day}</tspan></text>',
    ]

    # City blocks
    for x in range(MAP_X0, MAP_X1 + 1, 30):
        for y in range(MAP_TOP, MAP_TOP + MAP_H + 1, 30):
            out.append(f'<circle cx="{x}" cy="{y}" r="1" fill="{GRID}"/>')

    loop = f'dur="{LOOP_S}s" repeatCount="indefinite"'
    out += [
        f'<path id="tour" d="{path}" fill="none" stroke="{DIM}" stroke-width="1" stroke-dasharray="3 5" opacity="0.6"/>',
        f'<path d="{path}" fill="none" stroke="{ACCENT}" stroke-width="2.5" stroke-linejoin="round" '
        f'pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1">'
        f'<animate attributeName="stroke-dashoffset" values="1;0;0" keyTimes="0;{DRIVE_SHARE};1" {loop}/></path>',
    ]

    for i, (x, y) in enumerate(stops, start=1):
        t = arrival[i]
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{BG}" stroke="{DIM}" stroke-width="1.5">'
            f'<animate attributeName="fill" values="{BG};{ACCENT};{ACCENT}" keyTimes="0;{t:.4f};1" calcMode="discrete" {loop}/>'
            f'<animate attributeName="stroke" values="{DIM};{ACCENT};{ACCENT}" keyTimes="0;{t:.4f};1" calcMode="discrete" {loop}/>'
            f"</circle>"
        )

    dx, dy = depot
    out += [
        f'<rect x="{dx - 11}" y="{dy - 11}" width="22" height="22" rx="4" fill="{BG}" stroke="{ACCENT}" stroke-width="2"/>',
        f'<text x="{dx}" y="{dy + 30}" fill="{DIM}" font-size="11" text-anchor="middle">depot</text>',
        f'<text font-size="22" text-anchor="middle" dominant-baseline="central">🚛'
        f'<animateMotion keyPoints="0;1;1" keyTimes="0;{DRIVE_SHARE};1" calcMode="linear" {loop}>'
        f'<mpath href="#tour"/></animateMotion></text>',
    ]

    y = MAP_TOP + MAP_H + 32
    out.append(
        f'<text x="24" y="{y}" fill="{FG}"><tspan fill="{ACCENT}">✔ </tspan>'
        f'{STOPS} stops · <tspan fill="{ACCENT}" font-weight="bold">{best_km:.1f} km</tspan> · '
        f'nearest neighbour {nn_km:.1f} km → {verdict} · solved in {solve_ms:.1f} ms</text>'
    )
    out.append(
        f'<text x="24" y="{y + 22}" fill="{DIM}" font-size="11">'
        f"new city every day · the real ones at work use OR-Tools and a lot more constraints</text>"
    )
    out.append("</svg>")
    return "\n".join(out)


def main():
    out_path = sys.argv[1]
    day = datetime.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else datetime.datetime.now(datetime.timezone.utc).date()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render(day))


if __name__ == "__main__":
    main()
