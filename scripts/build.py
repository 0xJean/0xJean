#!/usr/bin/env python3
"""Generate the profile's SVG assets (light + dark) into ../assets.

GitHub renders README images as plain <img>, so everything here is
self-contained SVG: system fonts, inline CSS, CSS keyframe animation.
Run:  python3 scripts/build.py
"""

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
W = 1000

THEMES = {
    "light": dict(bg="#ECE9E2", card="#F5F3EE", ink="#141412", muted="#6B6861", line="#D3D0C9", signal="#FF4A1C", onink="#ECE9E2"),
    "dark": dict(bg="#0E0E0D", card="#161615", ink="#EDEAE3", muted="#8F8C84", line="#2A2A28", signal="#FF4A1C", onink="#0E0E0D"),
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
SERIF = "'Iowan Old Style', 'Palatino Linotype', Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(width, height, body, t, extra_css="", label=""):
    css = f"""
    .sans {{ font-family: {SANS}; }}
    .serif {{ font-family: {SERIF}; }}
    .mono {{ font-family: {MONO}; }}
    .ink {{ fill: {t['ink']}; }}
    .muted {{ fill: {t['muted']}; }}
    .signal {{ fill: {t['signal']}; }}
    {extra_css}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(label)}">'
        f"<style>{css}</style>{body}</svg>"
    )


def text(x, y, s, cls, size, weight=400, anchor="start", spacing=0, style=""):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    st = f' font-style="{style}"' if style else ""
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{ls}{st}>{esc(s)}</text>'


# ── Hero: name + live order book ───────────────────────────
def hero(t):
    H = 440
    rnd = random.Random(2017)
    mid_x, base_y, half = 800, 352, 165
    dots = []
    for _ in range(1500):
        side = rnd.choice((-1, 1))
        u = rnd.random()
        step = math.floor(u * 16) / 16
        depth = 14 + 190 * step**1.3
        x = mid_x + side * (8 + u * half)
        y = base_y - rnd.random() * depth
        r = 0.9 + rnd.random() * 1.1
        op = 0.25 + 0.55 * rnd.random()
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{t["ink"]}" opacity="{op:.2f}"/>')

    # Particles flowing toward the mid price.
    flow = []
    for i in range(36):
        side = -1 if i % 2 else 1
        y = base_y - 6 - rnd.random() * 60
        dur = 2.2 + rnd.random() * 2.4
        delay = -rnd.random() * dur
        dist = (50 + rnd.random() * 120) * side
        flow.append(
            f'<circle class="flow" style="--d:{dist:.0f}px;animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s" '
            f'cx="{mid_x}" cy="{y:.1f}" r="1.8" fill="{t["ink"]}"/>'
        )

    # Fills bursting at the mid price.
    sparks = []
    for i in range(30):
        a = rnd.uniform(-math.pi * 0.95, -math.pi * 0.05)
        m = 30 + rnd.random() * 90
        dx, dy = math.cos(a) * m * 0.8, math.sin(a) * m * 1.2
        dur = 1.4 + rnd.random() * 1.2
        delay = -rnd.random() * dur
        r = 1.6 + rnd.random() * 2.2
        sparks.append(
            f'<circle class="spark" style="--x:{dx:.0f}px;--y:{dy:.0f}px;animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s" '
            f'cx="{mid_x}" cy="{base_y - 8}" r="{r:.1f}" fill="{t["signal"]}"/>'
        )

    css = """
    .flow { animation: flow linear infinite; transform-box: fill-box; }
    @keyframes flow { 0% { transform: translateX(var(--d)); opacity: 0; } 15% { opacity: .9; } 100% { transform: translateX(0); opacity: .9; } }
    .spark { animation: spark ease-out infinite; opacity: 0; }
    @keyframes spark { 0% { transform: translate(0,0); opacity: 1; } 100% { transform: translate(var(--x), var(--y)); opacity: 0; } }
    .pulse { animation: pulse 1.6s ease-out infinite; transform-origin: center; transform-box: fill-box; }
    @keyframes pulse { 0% { transform: scale(1); opacity: .7; } 100% { transform: scale(3.2); opacity: 0; } }
    """
    body = f"""
    <rect width="{W}" height="{H}" rx="22" fill="{t['bg']}"/>
    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{t['line']}"/>
    <g>
      <circle cx="56" cy="62" r="4" fill="{t['ink']}"/><circle cx="70" cy="62" r="5" fill="{t['signal']}"/><circle cx="84" cy="62" r="4" fill="{t['ink']}"/>
      {text(100, 67, "JEAN  /  0xJean", "mono ink", 15, 500, spacing=2)}
    </g>
    {text(56, 128, "WEB3 ARCHITECT · FOUNDER · SINCE 2017", "mono muted", 15, spacing=1.2)}
    {text(52, 200, "I’m Jean.", "sans ink", 58, 600, spacing=-2)}
    {text(52, 264, "I build the engines", "sans ink", 58, 600, spacing=-2)}
    {text(54, 332, "markets run on.", "serif signal", 62, 400, style="italic")}
    {text(56, 390, "Exchanges · Perpetuals · Payments · Quant", "sans muted", 19)}
    <g>{''.join(dots)}</g>
    <line x1="{mid_x}" y1="{base_y - 236}" x2="{mid_x}" y2="{base_y + 6}" stroke="{t['signal']}" stroke-width="1" stroke-dasharray="2 5" opacity=".6"/>
    <g>{''.join(flow)}</g>
    <g>{''.join(sparks)}</g>
    <line x1="{mid_x - half - 20}" y1="{base_y + 8}" x2="{mid_x + half + 20}" y2="{base_y + 8}" stroke="{t['line']}"/>
    {text(mid_x - half, base_y + 34, "BIDS", "mono muted", 13, spacing=1.5)}
    {text(mid_x + half, base_y + 34, "ASKS", "mono muted", 13, anchor="end", spacing=1.5)}
    <circle cx="{mid_x - 22}" cy="{base_y + 30}" r="3.5" fill="{t['signal']}"/>
    <circle class="pulse" cx="{mid_x - 22}" cy="{base_y + 30}" r="3.5" fill="{t['signal']}"/>
    {text(mid_x - 12, base_y + 34, "LIVE", "mono muted", 13, spacing=1.5)}
    """
    return svg(W, H, body, t, css, "Jean — I build the engines markets run on.")


# ── Stats strip ─────────────────────────────────────────────
def stats(t):
    H = 156
    items = [("16", "years shipping software"), ("10+", "years in Web3"), ("12", "years as a founder"), ("$B+", "value through my systems")]
    col = W / 4
    parts = [f'<rect width="{W}" height="{H}" rx="22" fill="{t["card"]}"/>',
             f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{t["line"]}"/>']
    for i, (n, label) in enumerate(items):
        x = i * col + 32
        if i:
            parts.append(f'<line x1="{i*col}" y1="30" x2="{i*col}" y2="{H-30}" stroke="{t["line"]}"/>')
        parts.append(text(x, 84, n, "sans ink", 50, 600, spacing=-2))
        parts.append(text(x + 2, 116, label, "sans muted", 17))
    return svg(W, H, "".join(parts), t, label="16 years shipping software, 10+ years in Web3, 12 years as a founder, $B+ handled by systems I designed")


# ── Products ────────────────────────────────────────────────
def mini_candles(x, y, t, seed):
    rnd = random.Random(seed)
    raw, p = [], 0.0
    for _ in range(16):
        o = p
        c = o + rnd.uniform(-7, 9)
        raw.append((o, c, max(o, c) + rnd.random() * 4, min(o, c) - rnd.random() * 4))
        p = c
    lo = min(r[3] for r in raw)
    hi = max(r[2] for r in raw)
    sy = lambda v: y + 58 - (v - lo) / (hi - lo) * 56
    out = []
    for i, (o, c, h, l) in enumerate(raw):
        col = t["ink"] if c >= o else t["signal"]
        cx = x + i * 9
        top, bot = sy(max(o, c)), sy(min(o, c))
        out.append(f'<line x1="{cx+3}" x2="{cx+3}" y1="{sy(h):.1f}" y2="{sy(l):.1f}" stroke="{col}"/>')
        out.append(f'<rect x="{cx}" width="6" y="{top:.1f}" height="{max(1.5, bot - top):.1f}" fill="{col}"/>')
    return "".join(out)


def mini_line(x, y, t, seed, drift=0.3, area=True, w=144, h=60):
    rnd = random.Random(seed)
    vals, v = [], 0.0
    for _ in range(40):
        v += rnd.uniform(-1, 1) + drift
        vals.append(v)
    lo, hi = min(vals), max(vals)
    pts = [(x + i / 39 * w, y + 4 + (1 - (val - lo) / (hi - lo)) * (h - 8)) for i, val in enumerate(vals)]
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    out = ""
    if area:
        out += f'<path d="{d} L{x+w},{y+h} L{x},{y+h} Z" fill="{t["signal"]}" opacity=".12"/>'
    return out + f'<path d="{d}" fill="none" stroke="{t["ink"]}" stroke-width="1.6"/>'


def mini_pos(x, y, t):
    return (
        f'<rect x="{x+44}" y="{y-6}" width="56" height="74" rx="10" fill="{t["ink"]}"/>'
        f'<rect x="{x+50}" y="{y}" width="44" height="30" rx="5" fill="{t["card"]}"/>'
        f'<circle cx="{x+72}" cy="{y+15}" r="8" fill="{t["signal"]}"/>'
        f'<path d="M{x+68},{y+15} l3,3 l6,-6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>'
        + "".join(
            f'<rect x="{x+50 + (k % 3) * 15}" y="{y+36 + (k // 3) * 10}" width="12" height="6" rx="2" fill="{t["muted"]}" opacity=".5"/>'
            for k in range(9)
        )
    )


def products(t):
    cards = [
        ("01", "CENTRALIZED EXCHANGE", "A crypto exchange,", "from a blank page",
         ["Designed end to end: matching engine,", "data layer and multisig custody."],
         [("ms", "latency"), ("1M+", "daily users"), ("0", "assets lost")], "candles"),
        ("02", "ON-CHAIN PERPETUALS", "A perpetuals exchange", "that lives on-chain",
         ["Hundreds of in-house smart contracts,", "fully on-chain matching, multi-chain."],
         [("$10M+", "TVL"), ("200K", "users"), ("$100M+", "daily volume")], "line"),
        ("03", "RETAIL CRYPTO PAYMENTS", "Paying with crypto", "at the checkout counter",
         ["Dozens of tokens on thousands of POS", "terminals, HSM keys, settled in seconds."],
         [("1,000s", "POS terminals"), ("8-fig", "daily volume"), ("0", "incidents")], "pos"),
        ("04", "QUANTITATIVE TRADING", "A quant system with", "a public scoreboard",
         ["Multi-asset perpetual strategies with", "copy-trading, public and verifiable."],
         [("#7", "on Binance leaderboard"), ("Live", "copy-trading")], "equity"),
    ]
    cw, ch, gap = 488, 320, 24
    H = 2 * ch + gap
    parts = []
    for idx, (no, tag, n1, n2, desc, metrics, art) in enumerate(cards):
        cx = (idx % 2) * (cw + gap)
        cy = (idx // 2) * (ch + gap)
        parts.append(f'<rect x="{cx+0.5}" y="{cy+0.5}" width="{cw-1}" height="{ch-1}" rx="20" fill="{t["card"]}" stroke="{t["line"]}"/>')
        parts.append(text(cx + 30, cy + 48, no, "mono signal", 15, 500, spacing=1))
        parts.append(text(cx + 62, cy + 48, tag, "mono muted", 13, spacing=1))
        ax, ay = cx + cw - 172, cy + 28
        if art == "candles":
            parts.append(mini_candles(ax, ay, t, 7))
        elif art == "line":
            parts.append(mini_line(ax, ay, t, 11, drift=0.15))
        elif art == "pos":
            parts.append(mini_pos(ax, ay, t))
        else:
            parts.append(mini_line(ax, ay, t, 3, drift=0.45))
        parts.append(text(cx + 30, cy + 128, n1, "sans ink", 29, 600, spacing=-0.6))
        parts.append(text(cx + 30, cy + 163, n2, "sans ink", 29, 600, spacing=-0.6))
        for k, line in enumerate(desc):
            parts.append(text(cx + 30, cy + 202 + k * 24, line, "sans muted", 17))
        parts.append(f'<line x1="{cx+30}" y1="{cy+248}" x2="{cx+cw-30}" y2="{cy+248}" stroke="{t["line"]}"/>')
        mx = cx + 30
        for value, label in metrics:
            parts.append(text(mx, cy + 282, value, "mono ink", 21, 600))
            parts.append(text(mx, cy + 303, label, "sans muted", 14))
            mx += 145 if len(metrics) == 3 else 200
    return svg(W, H, "".join(parts), t, label="Four products: a crypto exchange, an on-chain perpetuals exchange, a crypto payment network and a quant trading system")


def bets(t):
    items = ["AI video × ERC-404", "GameFi economy", "Token swap DEX", "x402 payments", "NFT synthetics", "Token toolkit"]
    H = 60
    parts, x = [], 0
    for s in items:
        w = 28 + len(s) * 9.2
        parts.append(f'<rect x="{x+0.5}" y="10.5" width="{w}" height="38" rx="19" fill="{t["card"]}" stroke="{t["line"]}"/>')
        parts.append(text(x + w / 2, 35, s, "sans ink", 15, 500, anchor="middle"))
        x += w + 10
    return svg(int(x), H, "".join(parts), t, label="Also shipped: " + ", ".join(items))


# ── Stack ───────────────────────────────────────────────────
def stack(t):
    layers = [
        ("L4", "Application", "Wallets · POS payments · GameFi · AI video"),
        ("L3", "Custody & security", "HSM · Multisig custody · Wallet security · Fast settlement"),
        ("L2", "Engine", "In-memory matching · Microservices · Queues · 100M-scale data"),
        ("L1", "Protocol", "Solidity · Rust · EVM & gas · Cross-chain · ERC-404 · x402"),
    ]
    row, top = 82, 30
    H = top * 2 + row * 4
    parts = [f'<rect width="{W}" height="{H}" rx="22" fill="{t["card"]}"/>',
             f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{t["line"]}"/>']
    for i, (no, name, items) in enumerate(layers):
        y = top + i * row
        if i:
            parts.append(f'<line x1="36" y1="{y}" x2="660" y2="{y}" stroke="{t["line"]}"/>')
        parts.append(text(36, y + 47, no, "mono signal", 15, 500))
        parts.append(text(88, y + 38, name, "sans ink", 23, 600, spacing=-0.3))
        parts.append(text(88, y + 64, items, "sans muted", 16))

    # Isometric stack of four dotted planes, the top one highlighted.
    cx, cy = 840, 96
    rnd = random.Random(4)
    for li in range(4):
        oy = cy + li * 64
        col = t["signal"] if li == 0 else t["ink"]
        for gx in range(12):
            for gz in range(12):
                u, v = gx / 11 - 0.5, gz / 11 - 0.5
                x = cx + (u - v) * 120
                y = oy + (u + v) * 42
                op = 0.9 if li == 0 else 0.25 + 0.35 * rnd.random()
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.6" fill="{col}" opacity="{op:.2f}"/>')
    for k in (-1, 1):
        parts.append(f'<line x1="{cx + k*60}" y1="{cy+21}" x2="{cx + k*60}" y2="{cy + 3*64 + 21}" stroke="{t["line"]}" stroke-dasharray="2 4"/>')
    return svg(W, H, "".join(parts), t, label="Stack: application, custody and security, engine, protocol")


# ── Buttons ─────────────────────────────────────────────────
def button(label, primary, t, width):
    H = 52
    if primary:
        bg, fg, stroke = t["ink"], t["onink"], t["ink"]
    else:
        bg, fg, stroke = t["card"], t["ink"], t["line"]
    body = (
        f'<rect x="0.5" y="0.5" width="{width-1}" height="{H-1}" rx="26" fill="{bg}" stroke="{stroke}"/>'
        f'<text x="{width/2}" y="32" font-size="16" font-weight="500" text-anchor="middle" class="sans" fill="{fg}">{esc(label)}</text>'
    )
    return svg(width, H, body, t, label=label)


# ── Footer: the spread closes ───────────────────────────────
def footer(t):
    H = 120
    rnd = random.Random(9)
    dots = []
    for _ in range(900):
        s = rnd.choice((-1, 1))
        x = W / 2 + s * (rnd.random() ** 1.8) * (W / 2 - 20)
        spread = 1.5 + 9 * abs(x - W / 2) / (W / 2)
        y = 46 + rnd.uniform(-spread, spread)
        near = abs(x - W / 2) < 40
        col = t["signal"] if near and rnd.random() < 0.7 else t["ink"]
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{0.8 + rnd.random():.2f}" fill="{col}" opacity="{0.3 + 0.6 * rnd.random():.2f}"/>')
    body = (
        "".join(dots)
        + text(W / 2, 98, "Let’s close the spread.", "serif signal", 22, 400, anchor="middle", style="italic")
    )
    return svg(W, H, body, t, label="Let’s close the spread.")


def main():
    OUT.mkdir(exist_ok=True)
    builds = {
        "hero": hero,
        "stats": stats,
        "products": products,
        "bets": bets,
        "stack": stack,
        "footer": footer,
        "btn-telegram": lambda t: button("Message me on Telegram  →", True, t, 280),
        "btn-x": lambda t: button("Follow on X  ↗", False, t, 170),
        "btn-site": lambda t: button("Website  ↗", False, t, 150),
    }
    for name, fn in builds.items():
        for theme, t in THEMES.items():
            path = OUT / f"{name}-{theme}.svg"
            path.write_text(fn(t), encoding="utf-8")
    total = sum(p.stat().st_size for p in OUT.glob("*.svg"))
    print(f"wrote {len(builds) * 2} files, {total / 1024:.0f} KB")


if __name__ == "__main__":
    main()
