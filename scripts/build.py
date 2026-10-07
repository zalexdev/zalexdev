#!/usr/bin/env python3
"""
Renders every SVG under assets/ for the zalexdev profile README.
    python3 scripts/build.py
Edit the text/numbers below and re-run. No dependencies.
"""
import math, random
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

# ── palette ────────────────────────────────────────────────────────────────
BG, BG2, LINE = "#0b0d10", "#11151b", "#1d232c"
TXT, DIM, MUTE = "#d7dde5", "#7b8594", "#4a5361"
YEL, BLU, GRN, RED, VIO = "#ffd23f", "#4c9aff", "#5cff9d", "#ff5c6c", "#b28cff"
MONO = ("ui-monospace,'JetBrains Mono','Fira Code','Cascadia Code',SFMono-Regular,"
        "Menlo,Consolas,'Liberation Mono',monospace")

BASE_CSS = f"""
text{{font-family:{MONO};}}
.t{{fill:{TXT}}} .d{{fill:{DIM}}} .m{{fill:{MUTE}}}
.y{{fill:{YEL}}} .b{{fill:{BLU}}} .g{{fill:{GRN}}} .r{{fill:{RED}}} .v{{fill:{VIO}}}
.in{{opacity:0;animation:in .01s linear forwards}}
@keyframes in{{to{{opacity:1}}}}
.blink{{animation:blink 1.05s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
"""


def frame(w, h, body, css="", r=14):
    """Dark rounded panel with a faint dot grid and a slow scanline."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{BASE_CSS}{css}
.scan{{animation:scan 7s linear infinite}}
@keyframes scan{{from{{transform:translateY(-60px)}}to{{transform:translateY({h+60}px)}}}}
</style>
<defs>
<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{LINE}"/></pattern>
<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{YEL}" stop-opacity="0"/><stop offset=".5" stop-color="{YEL}" stop-opacity=".045"/><stop offset="1" stop-color="{YEL}" stop-opacity="0"/></linearGradient>
<clipPath id="panel"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>
</defs>
<g clip-path="url(#panel)">
<rect width="{w}" height="{h}" fill="{BG}"/>
<rect width="{w}" height="{h}" fill="url(#dots)"/>
{body}
<rect class="scan" x="0" y="0" width="{w}" height="60" fill="url(#scanG)"/>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{LINE}"/>
</svg>"""


def chrome(w, title):
    return f"""<rect width="{w}" height="34" fill="{BG2}"/><line x1="0" y1="34" x2="{w}" y2="34" stroke="{LINE}"/>
<circle cx="20" cy="17" r="5" fill="{RED}" opacity=".8"/><circle cx="38" cy="17" r="5" fill="{YEL}" opacity=".8"/><circle cx="56" cy="17" r="5" fill="{GRN}" opacity=".8"/>
<text x="{w/2}" y="21.5" text-anchor="middle" font-size="12" class="m">{escape(title)}</text>"""


# ── 1. hero ────────────────────────────────────────────────────────────────
def hero():
    W, H = 1000, 300
    rnd = random.Random(36911)
    bars, n = [], 96
    for i in range(n):
        x = 10 + i * (W - 20) / n
        hmax = 30 + 150 * (0.5 + 0.5 * math.sin(i / 7.0)) * rnd.uniform(.55, 1)
        col = YEL if i % 11 == 0 else (BLU if i % 3 else "#2b3a55")
        bars.append(f'<rect x="{x:.1f}" y="{H-hmax:.1f}" width="{(W-20)/n-3:.1f}" height="{hmax:.1f}" fill="{col}" opacity=".26" '
                    f'style="transform-origin:{x:.1f}px {H}px;animation:eq {rnd.uniform(.7,2.2):.2f}s ease-in-out {-rnd.uniform(0,2):.2f}s infinite alternate"/>')
    css = """
@keyframes eq{from{transform:scaleY(.12)}to{transform:scaleY(1)}}
.name{font-size:104px;font-weight:800}
.gl1{animation:g1 5s steps(1) infinite} .gl2{animation:g2 5s steps(1) infinite}
@keyframes g1{0%,88%,100%{transform:translate(0,0);opacity:0}89%{transform:translate(-7px,2px);opacity:.9}91%{transform:translate(5px,-3px);opacity:.9}93%{transform:translate(-2px,0);opacity:.9}95%{opacity:0}}
@keyframes g2{0%,88%,100%{transform:translate(0,0);opacity:0}89%{transform:translate(6px,-2px);opacity:.9}91%{transform:translate(-5px,3px);opacity:.9}93%{transform:translate(3px,1px);opacity:.9}95%{opacity:0}}
.rise{opacity:0;animation:rise .9s cubic-bezier(.2,.8,.2,1) .15s forwards}
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.sub{opacity:0;animation:rise .8s ease .7s forwards}
.cyc text{opacity:0;animation:cyc 16s infinite}
@keyframes cyc{0%{opacity:0}2%,23%{opacity:1}25%,100%{opacity:0}}
"""
    roles = ["boots a real Linux kernel inside an Android app",
             "built Stryker — the pentest lab in 150K+ pockets",
             "first public WhisperPair PoC, ~12h after disclosure",
             "architects AI backends at millions-of-users scale"]
    cyc = "".join(f'<text x="80" y="236" font-size="17" class="t" style="animation-delay:{i*4}s">'
                  f'<tspan class="y">&gt; </tspan>{escape(r)}</text>' for i, r in enumerate(roles))
    name = lambda cls: f'<text x="74" y="170" class="name {cls}" textLength="470" lengthAdjust="spacingAndGlyphs">zalexdev</text>'
    body = f"""
<g>{''.join(bars)}</g>
<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity=".95"/><stop offset=".65" stop-color="{BG}" stop-opacity=".45"/><stop offset="1" stop-color="{BG}" stop-opacity=".05"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#fade)"/>
<text x="80" y="62" font-size="13" class="m sub">// android · kernel · offensive security · backend</text>
<g class="rise">{name('b gl1')}{name('y gl2')}{name('t')}
  <rect x="562" y="96" width="14" height="76" class="y blink"/></g>
<g class="cyc">{cyc}</g>
"""
    return frame(W, H, body, css)


# ── 2. impact: odometer counters ──────────────────────────────────────────
def impact():
    W, H = 1000, 184
    tiles = [
        ("150K+", "installs", "Stryker · Android pentest", YEL),
        ("1.8k★", "GitHub stars", "strykerapp · GPLv3", YEL),
        ("~3s", "phone → dockerd", "linux-um-arm64 · no root", GRN),
        ("12h", "disclosure → public PoC", "CVE-2025-36911", RED),
    ]
    PAD, GAP = 24, 14
    tw = (W - 2 * PAD - 3 * GAP) / 4
    th = 136
    FS, CW, LH = 54, 32.6, 64
    css = """
.roll{animation:roll 1.8s cubic-bezier(.15,.85,.25,1) both}
@keyframes roll{from{transform:translateY(0)}}
.tile{opacity:0;animation:tin .6s ease both}
@keyframes tin{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
"""
    out, clips = [], []
    for i, (val, label, cap, col) in enumerate(tiles):
        cx, cy = PAD + i * (tw + GAP), 24
        base = cy + 74
        d0 = 0.2 + i * 0.12
        clips.append(f'<clipPath id="c{i}"><rect x="{cx}" y="{base-FS+4}" width="{tw}" height="{FS+2}"/></clipPath>')
        chars = []
        for k, ch in enumerate(val):
            x = cx + 22 + k * CW
            if ch.isdigit():
                dgt = int(ch)
                steps = 10 * (1 + min(k, 2)) + dgt  # later digits spin longer, always land on dgt
                col_txt = "".join(f'<text x="{x:.1f}" y="{base + j*LH}" font-size="{FS}" font-weight="800" fill="{col}">{j % 10}</text>'
                                  for j in range(steps + 1))
                chars.append(f'<g style="transform:translateY({-steps*LH}px);animation-delay:{d0+.15+k*.08:.2f}s" class="roll">{col_txt}</g>')
            else:
                chars.append(f'<text x="{x:.1f}" y="{base}" font-size="{FS}" font-weight="800" fill="{col}">{escape(ch)}</text>')
        out.append(
            f'<g class="tile" style="animation-delay:{d0:.2f}s">'
            f'<rect x="{cx}" y="{cy}" width="{tw:.1f}" height="{th}" rx="10" fill="{BG2}" stroke="{LINE}"/>'
            f'<rect x="{cx}" y="{cy+16}" width="3" height="{th-32}" fill="{col}"/>'
            f'<g clip-path="url(#c{i})">{"".join(chars)}</g>'
            f'<text x="{cx+22}" y="{base+26}" font-size="14" class="t">{escape(label)}</text>'
            f'<text x="{cx+22}" y="{base+47}" font-size="12" class="m">{escape(cap)}</text></g>')
    body = f'<defs>{"".join(clips)}</defs>' + "".join(out)
    return frame(W, H, body, css)


# ── 3. dmesg boot log ─────────────────────────────────────────────────────
def boot():
    W = 1000
    lines = [
        ("0.000000", "t", "Linux version 7.2-zalexdev (ARCH=um SUBARCH=arm64) — booting as a user process", None),
        ("0.003117", "t", "cpu0: Ukrainian 🇺🇦 · fluent in C, Java, Kotlin, Python", None),
        ("0.017702", "t", "stryker: rooted-Android pentest suite · 150K+ installs · nmap/msf/BLE/HID on-device", "g"),
        ("0.031000", "t", "stryker: open-sourced under GPLv3 — free, community-driven", "g"),
        ("0.064400", "t", "um-arm64: ported User-Mode Linux to aarch64 · Debian + Docker on an unrooted phone", "g"),
        ("0.071200", "t", "um-arm64: SMP, loadable modules, USB devices handed to real kernel drivers", "g"),
        ("0.077300", "t", "um-arm64: RFC posted to linux-um · upstream reception: \"Nice :-)\"", "g"),
        ("0.081900", "t", "phantomlink: wlan9 registered (ath9k_htc) — device is not actually here", "y"),
        ("0.093100", "t", "whisperpair: shipped first public PoC ~12h after partial disclosure", "g"),
        ("0.102300", "t", "backend: architect · FastAPI · Postgres HA · RabbitMQ · ClickHouse · LangGraph", "g"),
        ("0.224001", "y", "Run /sbin/magic as init process", None),
    ]
    LH, y0 = 25, 66
    H = y0 + LH * (len(lines) + 1) + 26
    rows, t = [], 0.35
    for i, (ts, cls, msg, tag) in enumerate(lines):
        y = y0 + i * LH
        if tag:
            label = "  OK  " if tag == "g" else " WARN "
            badge = (f'<text x="34" y="{y}" font-size="13.5" class="m">[</text>'
                     f'<text x="42" y="{y}" font-size="13.5" class="{tag}" font-weight="700" xml:space="preserve">{label}</text>'
                     f'<text x="93" y="{y}" font-size="13.5" class="m">]</text>')
        else:
            badge = f'<text x="34" y="{y}" font-size="13.5" class="m">[ ···· ]</text>'
        rows.append(f'<g class="in" style="animation-delay:{t:.2f}s">{badge}'
                    f'<text x="112" y="{y}" font-size="13.5" class="d">[{ts:>12}]</text>'
                    f'<text x="240" y="{y}" font-size="13.5" class="{cls}">{escape(msg)}</text></g>')
        t += 0.16 + (0.25 if i in (1, 3, 6) else 0)
    py = y0 + len(lines) * LH + 8
    cmd = "whoami"
    typed = "".join(f'<tspan class="in" style="animation-delay:{t+0.3+k*0.09:.2f}s">{c}</tspan>' for k, c in enumerate(cmd))
    out_t = t + 0.3 + len(cmd) * 0.09 + 0.35
    answer = "someone who makes hardware-shaped problems run in userspace."
    rows.append(f'<g class="in" style="animation-delay:{t:.2f}s"><text x="34" y="{py}" font-size="14.5">'
                f'<tspan class="g">magic@phone</tspan><tspan class="m">:</tspan><tspan class="b">~</tspan><tspan class="m">$ </tspan>'
                f'<tspan class="t">{typed}</tspan></text></g>')
    rows.append(f'<g class="in" style="animation-delay:{out_t:.2f}s"><text x="34" y="{py+LH}" font-size="14.5" class="y">{answer}</text>'
                f'<rect x="{34+(len(answer)+1)*8.75:.0f}" y="{py+LH-13}" width="9" height="17" class="t blink"/></g>')
    return frame(W, H, chrome(W, "dmesg  ·  zalexdev@aarch64") + "".join(rows))


# ── 4. matryoshka ─────────────────────────────────────────────────────────
def matryoshka():
    W, H = 1000, 380
    cx, cy = 210, 200
    layers = [
        ("Android app", "unrooted phone · plain untrusted_app", BLU),
        ("Linux 7.2 kernel", "ARCH=um SUBARCH=arm64 · runs as a process", YEL),
        ("Debian 12", "boots to dockerd in ~3 seconds", GRN),
        ("dockerd", "overlay2 · cgroup v2 · real kernel drivers", VIO),
        ("container", "pulled, started, port-forwarded to the phone", BLU),
        ("minecraft", "yes, really.", RED),
    ]
    css = """
.sq{fill:none;stroke-width:2;opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .55s cubic-bezier(.2,1.4,.4,1) forwards}
@keyframes pop{from{opacity:0;transform:scale(1.25)}to{opacity:1;transform:scale(1)}}
.core{transform-box:fill-box;transform-origin:center;animation:beat 1.6s ease-in-out 3.6s infinite}
@keyframes beat{50%{transform:scale(1.35)}}
.spin{transform-origin:210px 200px;animation:spin 40s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
"""
    g = []
    for i, (name, sub, col) in enumerate(layers):
        s = 300 - i * 50
        delay = 0.3 + i * 0.45
        g.append(f'<rect class="sq" x="{cx-s/2}" y="{cy-s/2}" width="{s}" height="{s}" rx="{26-i*3}" stroke="{col}" style="animation-delay:{delay:.2f}s"/>')
        ly = 82 + i * 47
        g.append(f'<g class="in" style="animation-delay:{delay+.2:.2f}s">'
                 f'<line x1="{cx+s/2-6}" y1="{cy-s/2+10}" x2="455" y2="{ly-5}" stroke="{col}" stroke-dasharray="4 4"/>'
                 f'<circle cx="{cx+s/2-6}" cy="{cy-s/2+10}" r="3" fill="{col}"/>'
                 f'<text x="470" y="{ly}" font-size="17" font-weight="700" fill="{col}">{escape(name)}</text>'
                 f'<text x="470" y="{ly+19}" font-size="13" class="d">{escape(sub)}</text></g>')
    g.append(f'<circle class="core in" cx="{cx}" cy="{cy}" r="7" fill="{RED}" style="animation-delay:3s"/>')
    ring = f'<circle class="spin" cx="{cx}" cy="{cy}" r="172" fill="none" stroke="{LINE}" stroke-dasharray="2 9"/>'
    title = (f'<text x="{W-40}" y="40" text-anchor="end" font-size="12" class="m">how deep does it go?</text>'
             '')
    return frame(W, H, ring + "".join(g) + title, css)


# ── 5. lsmod: the stack ───────────────────────────────────────────────────
def lsmod():
    mods = [
        ("c", "arch_um,ld_preload,af_packet", "systems", RED),
        ("android_ndk", "bionic,jni,usb_host", "mobile", YEL),
        ("java", "stryker", "mobile", YEL),
        ("kotlin", "wpair,umarm", "mobile", YEL),
        ("python", "fastapi,langgraph,celery", "backend", BLU),
        ("fastapi", "api_gateway,llm_router", "backend", BLU),
        ("postgresql", "patroni,pgbouncer [HA]", "data", GRN),
        ("redis", "rate_limit,queues,cache", "data", GRN),
        ("rabbitmq", "generation_pipeline", "data", GRN),
        ("clickhouse", "analytics", "data", GRN),
        ("langgraph", "agents,tool_calls", "ai", VIO),
        ("llm_router", "health_score,circuit_breaker", "ai", VIO),
        ("docker", "everything,including_phones", "infra", BLU),
    ]
    W = 1000
    LH, y0 = 24, 92
    H = y0 + LH * len(mods) + 34
    rnd = random.Random(7)
    rows = [f'<text y="{y0-30}" font-size="13.5" class="d"><tspan x="34">Module</tspan><tspan x="250">Size</tspan>'
            f'<tspan x="360">Used by</tspan><tspan x="{W-34}" text-anchor="end">class</tspan></text>']
    for i, (n, used, cls, col) in enumerate(mods):
        y = y0 + i * LH
        bw = rnd.uniform(.35, 1)
        rows.append(
            f'<g class="in" style="animation-delay:{.25+i*.07:.2f}s">'
            f'<text x="34" y="{y}" font-size="14" fill="{col}">{n}</text>'
            f'<text x="250" y="{y}" font-size="14" class="m">{rnd.randint(16, 980) * 64}</text>'
            f'<text x="360" y="{y}" font-size="14" class="t">{rnd.randint(1,9)}  <tspan class="d">{escape(used)}</tspan></text>'
            f'<rect x="{W-210}" y="{y-10}" width="{110*bw:.0f}" height="6" rx="3" fill="{col}" opacity=".55" '
            f'style="transform-origin:{W-210}px 0;animation:grow .9s cubic-bezier(.2,.8,.2,1) {.3+i*.07:.2f}s both"/>'
            f'<text x="{W-34}" y="{y}" font-size="12" text-anchor="end" class="m">{cls}</text></g>')
    css = "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    return frame(W, H, chrome(W, "lsmod  ·  loaded into zalexdev") + "".join(rows), css)


# ── 6. buttons ───────────────────────────────────────────────────
def button(label, sub, col, w=240):
    H = 52
    body = (f'<rect x="0" y="0" width="4" height="{H}" fill="{col}"/>'
            f'<text x="22" y="22" font-size="11" class="m">{escape(sub)}</text>'
            f'<text x="22" y="40" font-size="15" font-weight="700" fill="{col}">{escape(label)}</text>'
            f'<text x="{w-18}" y="34" text-anchor="end" font-size="16" class="d">↗</text>')
    return frame(w, H, body, r=10)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    files = {
        "hero.svg": hero(),
        "impact.svg": impact(),
        "boot.svg": boot(),
        "matryoshka.svg": matryoshka(),
        "lsmod.svg": lsmod(),
        "btn-web.svg": button("zalexdev.com", "web", YEL),
        "btn-tg.svg": button("@zalexdev", "telegram", BLU),
    }
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"  wrote assets/{name:<16} {len(svg)/1024:5.1f} KB")


if __name__ == "__main__":
    main()
