#!/usr/bin/env python3
"""Generate the profile's SVG assets (light + dark) into ../assets.

GitHub renders README images as plain <img>, so everything here is
self-contained SVG: system fonts, inline CSS, CSS keyframe animation.
Run:  python3 scripts/build.py
"""

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


def frame(width, height, t, fill=None):
    return (
        f'<rect width="{width}" height="{height}" rx="20" fill="{fill or t["card"]}"/>'
        f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="20" fill="none" stroke="{t["line"]}"/>'
    )


# ── Header: a terminal session ──────────────────────────────
def terminal(t):
    session = [
        ("whoami", [("Jean — Web3 architect & serial founder", "ink")]),
        ("cat roles", [("Founder · Co-founder · CEO · CTO", "ink")]),
        ("uptime", [("16y engineering · 12y founding · on-chain since 2017", "ink")]),
        ("ls ~/built", [("exchange/  perp-dex/  payment-rail/  quant-desk/  stowmind/  shellbeam/", "signal")]),
    ]
    top, lh = 96, 30
    rows = sum(1 + len(out) for _, out in session) + 1
    H = top + rows * lh + 6
    parts = [frame(W, H, t, t["bg"])]
    parts.append(f'<line x1="0" y1="52" x2="{W}" y2="52" stroke="{t["line"]}"/>')
    for i, c in enumerate((t["ink"], t["signal"], t["ink"])):
        parts.append(f'<circle cx="{30 + i * 20}" cy="26" r="6" fill="{c}"/>')
    parts.append(text(W / 2, 31, "jean@0xJean: ~", "mono muted", 14, anchor="middle"))

    # Content is static on purpose: renderers that snapshot the first frame
    # (mobile apps, previews) must still show every line. Only the cursor moves.
    css = """
    .cursor { animation: blink 1s steps(1) infinite; }
    @keyframes blink { 50% { opacity: 0; } }
    """
    y = top
    for cmd, out in session:
        parts.append(text(36, y, "❯", "mono signal", 18, 600) + text(62, y, cmd, "mono ink", 18, 500))
        y += lh
        for line, cls in out:
            parts.append(text(62, y, line, "mono " + cls, 17))
            y += lh
    parts.append(text(36, y, "❯", "mono signal", 18, 600))
    parts.append(f'<rect class="cursor" x="62" y="{y - 16}" width="10" height="20" fill="{t["ink"]}"/>')
    return svg(W, H, "".join(parts), t, css, "whoami: Jean — Web3 architect & serial founder. Founder, co-founder, CEO, CTO.")


# ── Chips: industries ───────────────────────────────────────
def chips(items, t, label, highlight=()):
    """Lay out pill tags across rows; `highlight` ones use the signal color."""
    size, ph, h, gap = 16, 18, 40, 10
    rows, row, x = [], [], 0
    for s in items:
        w = ph * 2 + len(s) * size * 0.56
        if row and x + w > W:
            rows.append(row)
            row, x = [], 0
        row.append((s, w, x))
        x += w + gap
    rows.append(row)
    H = len(rows) * (h + gap) - gap
    parts = []
    for r, row in enumerate(rows):
        y = r * (h + gap)
        for s, w, x in row:
            on = s in highlight
            fill = t["signal"] if on else t["card"]
            stroke = t["signal"] if on else t["line"]
            color = "#fff" if on else t["ink"]
            parts.append(f'<rect x="{x+0.5:.1f}" y="{y+0.5}" width="{w-1:.1f}" height="{h-1}" rx="{h/2}" fill="{fill}" stroke="{stroke}"/>')
            parts.append(
                f'<text x="{x + w/2:.1f}" y="{y + 26}" font-size="{size}" font-weight="500" text-anchor="middle" class="sans" fill="{color}">{esc(s)}</text>'
            )
    return svg(W, H, "".join(parts), t, label=label)


INDUSTRIES = [
    "Crypto exchanges (CEX)", "Perpetual DEX", "Crypto payments", "Quant trading", "DeFi",
    "Custody & wallet security", "Market infrastructure", "GameFi", "NFT", "AI × Web3",
    "AI agents & dev tools", "Desktop apps",
]
CORE = {"Crypto exchanges (CEX)", "Perpetual DEX", "Crypto payments", "Quant trading"}


# ── Expertise matrix ────────────────────────────────────────
def expertise(t):
    cols = [
        ("Trading systems", ["In-memory matching", "Order books & risk", "Perpetual futures", "Copy-trading", "100M-scale data"]),
        ("Smart contracts", ["Solidity · EVM", "Rust", "Gas optimization", "ERC-404 · x402", "Cross-chain messaging"]),
        ("Custody & payments", ["HSM key management", "Hot/cold multisig", "POS integration", "Multi-token settlement", "Security audits"]),
        ("Leadership", ["0 → 1 delivery", "System architecture", "Team building", "Founder · CEO · CTO", "Technical diligence"]),
    ]
    cw, pad = W / 4, 26
    H = 74 + 5 * 34 + 20
    parts = [frame(W, H, t)]
    for i, (title, items) in enumerate(cols):
        x = i * cw
        if i:
            parts.append(f'<line x1="{x}" y1="24" x2="{x}" y2="{H-24}" stroke="{t["line"]}"/>')
        parts.append(text(x + pad, 50, f"0{i+1}", "mono signal", 13, 500))
        parts.append(text(x + pad + 30, 50, title, "sans ink", 18, 600))
        for k, item in enumerate(items):
            y = 90 + k * 34
            parts.append(f'<circle cx="{x + pad + 3}" cy="{y - 5}" r="2.5" fill="{t["muted"]}"/>')
            parts.append(text(x + pad + 16, y, item, "sans muted", 15))
    return svg(W, H, "".join(parts), t, label="Expertise: trading systems, smart contracts, custody and payments, leadership")


# ── Open-source repo cards ──────────────────────────────────
REPOS = {
    "stowmind": ("StowMind", "Desktop app", ["Smart cleanup and AI file organization —", "privacy-first, rules before AI."], ["Tauri", "React", "Rust"], "#3178C6", "TypeScript"),
    "shellbeam": ("shellbeam", "SSH client", ["All-in-one SSH client — terminal, SFTP,", "port forwarding, AI and an encrypted vault."], ["Tauri", "Rust", "SFTP"], "#3178C6", "TypeScript"),
    "jean-skills": ("Jean-Skills", "Agent skills", ["Portable skills for Claude Code, Codex,", "Cursor & more — starting with Web3 EVM."], ["Agent Skills", "EVM", "DeFi"], None, "Markdown"),
    "jean-website": ("jean-website", "Personal site", ["My personal website — a live order", "book rendered in WebGL."], ["Three.js", "Vite", "i18n"], "#3178C6", "TypeScript"),
}


def repo_card(key, t):
    name, kind, desc, tags, lang_color, lang = REPOS[key]
    cw, H = 490, 200
    parts = [frame(cw, H, t)]
    parts.append(
        f'<g transform="translate(26 27)"><path d="M2 1.5A1.5 1.5 0 0 1 3.5 0h9A1.5 1.5 0 0 1 14 1.5v13a.5.5 0 0 1-.77.42L8 11.6l-5.23 3.32A.5.5 0 0 1 2 14.5z" fill="none" stroke="{t["muted"]}" stroke-width="1.3"/></g>'
    )
    parts.append(text(50, 41, "0xJean/", "mono muted", 14))
    parts.append(text(110, 41, name, "mono ink", 15, 600))
    parts.append(text(cw - 26, 41, kind.upper(), "mono signal", 12, 500, anchor="end", spacing=1))
    for k, line in enumerate(desc):
        parts.append(text(26, 86 + k * 24, line, "sans muted", 16))
    x = 26
    for tag in tags:
        w = 20 + len(tag) * 8
        parts.append(f'<rect x="{x}" y="132" width="{w}" height="26" rx="13" fill="none" stroke="{t["line"]}"/>')
        parts.append(text(x + w / 2, 150, tag, "sans ink", 13, 500, anchor="middle"))
        x += w + 8
    parts.append(f'<circle cx="31" cy="180" r="5" fill="{lang_color or t["muted"]}"/>')
    parts.append(text(43, 185, lang, "sans muted", 13))
    parts.append(text(cw - 26, 185, "View repository →", "sans ink", 13, 500, anchor="end"))
    return svg(cw, H, "".join(parts), t, label=f"{name}: {' '.join(desc)}")


# ── Buttons ─────────────────────────────────────────────────
def button(label, primary, t, width):
    H = 52
    bg, fg, stroke = (t["ink"], t["onink"], t["ink"]) if primary else (t["card"], t["ink"], t["line"])
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
    for _ in range(800):
        s = rnd.choice((-1, 1))
        x = W / 2 + s * (rnd.random() ** 1.8) * (W / 2 - 20)
        spread = 1.5 + 9 * abs(x - W / 2) / (W / 2)
        y = 46 + rnd.uniform(-spread, spread)
        near = abs(x - W / 2) < 34
        col = t["signal"] if near and rnd.random() < 0.7 else t["ink"]
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{0.8 + rnd.random():.2f}" fill="{col}" opacity="{0.3 + 0.6 * rnd.random():.2f}"/>')
    body = "".join(dots) + text(W / 2, 98, "Let’s close the spread.", "serif signal", 22, 400, anchor="middle", style="italic")
    return svg(W, H, body, t, label="Let’s close the spread.")


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    builds = {
        "terminal": terminal,
        "industries": lambda t: chips(INDUSTRIES, t, "Industries: " + ", ".join(INDUSTRIES), CORE),
        "expertise": expertise,
        **{f"repo-{k}": (lambda k: lambda t: repo_card(k, t))(k) for k in REPOS},
        "footer": footer,
        "btn-telegram": lambda t: button("Message me on Telegram  →", True, t, 280),
        "btn-x": lambda t: button("Follow on X  ↗", False, t, 170),
        "btn-site": lambda t: button("0xjean.com  ↗", False, t, 170),
    }
    for name, fn in builds.items():
        for theme, t in THEMES.items():
            (OUT / f"{name}-{theme}.svg").write_text(fn(t), encoding="utf-8")
    total = sum(p.stat().st_size for p in OUT.glob("*.svg"))
    print(f"wrote {len(builds) * 2} files, {total / 1024:.0f} KB")


if __name__ == "__main__":
    main()
