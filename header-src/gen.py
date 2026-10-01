#!/usr/bin/env python3
"""Generate header.svg: a strip map of Peyton's route, in pmserver.us's transit language."""
import base64, re, pathlib, sys
FREEZE = float(sys.argv[1]) if len(sys.argv) > 1 else None

HERE = pathlib.Path(__file__).parent
def b64(p): return base64.b64encode((HERE / p).read_bytes()).decode()

W, H = 960, 352
PAGE, PANEL, INK, ROUTE, LIVE = "#c9cbc7", "#ffffff", "#000000", "#ee352e", "#00933c"
T = 14  # seconds per loop

# --- logo: pull the inner markup from the site's logo.svg (64x64 viewBox) ---
logo_src = (HERE / "logo.svg").read_text()
logo_inner = re.sub(r"^.*?<svg[^>]*>", "", logo_src, flags=re.S).rsplit("</svg>", 1)[0]

# --- geometry ---
RAIL_Y = 234
X_DECIDE, X_CHECK, X_GATE, X_LIVE = 128, 428, 648, 880
LANES = [-39, -26, -13, 13, 26, 39]  # agent lanes, px off the rail

def lane_path(dy):
    y = RAIL_Y + dy
    return (f"M{X_DECIDE} {RAIL_Y} C{X_DECIDE+34} {RAIL_Y} {X_DECIDE+34} {y} {X_DECIDE+68} {y} "
            f"L{X_CHECK-68} {y} C{X_CHECK-34} {y} {X_CHECK-34} {RAIL_Y} {X_CHECK} {RAIL_Y}")

def pct(s): return f"{s / T * 100:.2f}%"

# --- timeline (seconds) ---
t_split   = 2.0    # agents leave DECIDE
t_stagger = 0.35   # per lane
t_lane    = 5.2    # one lane's worm: head leaves at 0, head arrives at half, tail arrives at end
t_merge   = t_split + t_stagger * (len(LANES) - 1) + t_lane / 2   # last head arrives at CHECK
t_leave_check = t_merge + 1.1
t_at_gate = t_leave_check + 0.9
t_tests   = t_at_gate + 0.4
t_live    = t_tests + 2.6
t_end     = T - 0.25

css = f"""
@font-face{{font-family:"ArchivoC";src:url(data:font/woff2;base64,{b64('archivo-800-72.woff2')}) format("woff2");font-weight:800}}
@font-face{{font-family:"ArchivoR";src:url(data:font/woff2;base64,{b64('archivo-700-100.woff2')}) format("woff2");font-weight:700}}
@font-face{{font-family:"CourierP";src:url(data:font/woff2;base64,{b64('courier-sub.woff2')}) format("woff2")}}
.h{{font-family:"ArchivoC","Archivo Narrow","Arial Narrow",Impact,sans-serif;font-weight:800;fill:{INK}}}
.r{{font-family:"ArchivoR","Archivo",Arial,sans-serif;font-weight:700;fill:{INK}}}
.q{{font-family:"CourierP","Courier Prime","Courier New",monospace;fill:{INK}}}
.name{{font-size:96px;letter-spacing:-0.02em}}
.st{{font-size:24px;letter-spacing:0.01em;text-anchor:middle}}
.cap{{font-size:14px;text-anchor:middle}}
.tag{{font-size:19px}}
.rail{{stroke:{ROUTE};stroke-width:12;fill:none;stroke-linecap:butt}}
.lane{{stroke:{INK};stroke-width:2.5;fill:none;stroke-dasharray:100 100;stroke-dashoffset:100;stroke-linecap:round}}
.station{{fill:{PANEL};stroke:{INK};stroke-width:7}}
.end{{fill:{PANEL};stroke:{INK};stroke-width:10}}

/* one clock: every element keys off the same {T}s loop */
.lane{{animation:worm {T}s linear infinite}}
{''.join(f'.l{i}{{animation-delay:calc(var(--f) + {t_split + i*t_stagger:.2f}s)}}' for i in range(len(LANES)))}

@keyframes worm{{
  0%{{stroke-dashoffset:100}}
  {pct(t_lane)}{{stroke-dashoffset:-100}}
  100%{{stroke-dashoffset:-100}}
}}
.marker{{fill:{INK};stroke:{PANEL};stroke-width:3;animation:ride {T}s linear infinite}}
@keyframes ride{{
  0%{{transform:translate({X_DECIDE}px,{RAIL_Y}px);opacity:0}}
  {pct(0.5)}{{transform:translate({X_DECIDE}px,{RAIL_Y}px);opacity:1}}
  {pct(t_split)}{{transform:translate({X_DECIDE}px,{RAIL_Y}px);opacity:1}}
  {pct(t_split+0.25)}{{transform:translate({X_DECIDE+20}px,{RAIL_Y}px);opacity:0}}
  {pct(t_merge-0.25)}{{transform:translate({X_CHECK-20}px,{RAIL_Y}px);opacity:0}}
  {pct(t_merge)}{{transform:translate({X_CHECK}px,{RAIL_Y}px);opacity:1}}
  {pct(t_leave_check)}{{transform:translate({X_CHECK}px,{RAIL_Y}px);opacity:1}}
  {pct(t_at_gate)}{{transform:translate({X_GATE}px,{RAIL_Y}px);opacity:1}}
  {pct(t_tests)}{{transform:translate({X_GATE}px,{RAIL_Y}px);opacity:1}}
  {pct(t_live)}{{transform:translate({X_LIVE}px,{RAIL_Y}px);opacity:1}}
  {pct(t_live+0.01)}{{opacity:0}}
  {pct(t_end)}{{transform:translate({X_LIVE}px,{RAIL_Y}px);opacity:0}}
  100%{{transform:translate({X_DECIDE}px,{RAIL_Y}px);opacity:0}}
}}
/* station lamp: the stop the marker is at goes solid */
.lamp{{animation-duration:{T}s;animation-iteration-count:infinite;animation-timing-function:step-end}}
.lamp-decide{{animation-name:lampA}}
@keyframes lampA{{0%{{fill:{INK}}}{pct(t_split)}{{fill:{PANEL}}}100%{{fill:{PANEL}}}}}
.lamp-check{{animation-name:lampB}}
@keyframes lampB{{0%{{fill:{PANEL}}}{pct(t_merge)}{{fill:{INK}}}{pct(t_leave_check)}{{fill:{PANEL}}}100%{{fill:{PANEL}}}}}
/* the gate is hollow until he says it */
.gate{{fill:{PANEL};stroke:{INK};stroke-width:3;animation:gateA {T}s step-end infinite}}
@keyframes gateA{{0%{{fill:{PANEL}}}{pct(t_at_gate)}{{fill:{INK}}}{pct(t_end)}{{fill:{PANEL}}}100%{{fill:{PANEL}}}}}
.gate-in{{fill:none;stroke:{PANEL};stroke-width:4;animation:gateB {T}s step-end infinite}}
@keyframes gateB{{0%{{opacity:0}}{pct(t_at_gate)}{{opacity:1}}{pct(t_end)}{{opacity:0}}100%{{opacity:0}}}}
/* tests: white dashes run the last stretch while the marker crosses it */
.tests{{stroke:{PANEL};stroke-width:4;fill:none;stroke-dasharray:6 14;stroke-dashoffset:0;opacity:0;animation:testsA {T}s linear infinite}}
@keyframes testsA{{
  0%,{pct(t_tests-0.001)}{{opacity:0;stroke-dashoffset:0}}
  {pct(t_tests)}{{opacity:1}}
  {pct(t_live)}{{opacity:1;stroke-dashoffset:-160}}
  {pct(t_live+0.001)}{{opacity:0}}
  100%{{opacity:0;stroke-dashoffset:-160}}
}}
.tests-cap{{opacity:0;animation:fadeTests {T}s step-end infinite}}
.build-cap{{opacity:0;animation:fadeBuild {T}s step-end infinite}}
@keyframes fadeBuild{{0%{{opacity:0}}{pct(t_split)}{{opacity:1}}{pct(t_merge+0.6)}{{opacity:0}}100%{{opacity:0}}}}
@keyframes fadeTests{{0%{{opacity:0}}{pct(t_tests)}{{opacity:1}}{pct(t_live)}{{opacity:0}}100%{{opacity:0}}}}
/* live: the terminal goes green, the lamp pings */
.live{{animation:liveA {T}s step-end infinite}}
@keyframes liveA{{0%{{fill:{PANEL}}}{pct(t_live)}{{fill:{LIVE}}}{pct(t_end)}{{fill:{PANEL}}}100%{{fill:{PANEL}}}}}
.live-txt{{fill:{LIVE};opacity:0;animation:liveB {T}s step-end infinite}}
@keyframes liveB{{0%{{opacity:0}}{pct(t_live)}{{opacity:1}}{pct(t_end)}{{opacity:0}}100%{{opacity:0}}}}
.ping{{fill:none;stroke:{LIVE};stroke-width:3;opacity:0;transform-origin:{X_LIVE}px {RAIL_Y}px;animation:pingA {T}s linear infinite}}
@keyframes pingA{{
  0%,{pct(t_live)}{{transform:scale(1);opacity:0}}
  {pct(t_live+0.05)}{{transform:scale(1);opacity:1}}
  {pct(t_live+1.0)}{{transform:scale(1.8);opacity:0}}
  {pct(t_live+1.0+0.01)}{{transform:scale(1);opacity:0}}
  {pct(t_live+1.2)}{{transform:scale(1);opacity:1}}
  {pct(t_live+2.1)}{{transform:scale(1.8);opacity:0}}
  100%{{opacity:0}}
}}
.marker,.lamp,.gate,.gate-in,.tests,.tests-cap,.build-cap,.live,.live-txt,.ping{{animation-delay:var(--f)}}
@media (prefers-reduced-motion:reduce){{
  .lane,.marker,.lamp,.gate,.gate-in,.tests,.tests-cap,.build-cap,.live,.live-txt,.ping{{animation:none}}
  .tests-cap,.build-cap{{opacity:1}}
  .lane{{stroke-dashoffset:0}}
  .marker{{opacity:0}}
  .gate{{fill:{INK}}} .gate-in{{opacity:1}}
  .live{{fill:{LIVE}}} .live-txt{{opacity:1}}
}}
"""

lanes_svg = "".join(f'<path class="lane l{i}" pathLength="100" d="{lane_path(dy)}"/>' for i, dy in enumerate(LANES))

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
  aria-labelledby="t d">
<title id="t">Peyton. I build software at night by directing AI agents.</title>
<desc id="d">A transit strip map. One red line runs through three stations: Decide (what gets built), Check (with my own eyes), Ship it (my call), then a stretch where every test runs in a fresh VM, ending at Live. Between Decide and Check, six thin tracks fan out and rejoin: the agents build it.</desc>
<style>:root{{--f:{"-%.2fs" % FREEZE if FREEZE is not None else "0s"}}}{"svg *{animation-play-state:paused !important}" if FREEZE is not None else ""}{css}</style>

<rect width="{W}" height="{H}" fill="{PAGE}"/>
<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="{PANEL}"/>

<!-- line bullet -->
<g transform="translate(46 52)">{logo_inner}</g>

<!-- name + his words -->
<text class="h name" x="126" y="118">PEYTON</text>
<text class="q tag" x="128" y="152">I build software at night by directing AI agents.</text>

<!-- tab, as on the site's bar -->
<rect x="{W-14-150}" y="14" width="150" height="38" fill="{INK}"/>
<text class="r" x="{W-14-75}" y="39" style="font-size:17px;fill:{PANEL};text-anchor:middle">pmserver.us</text>

<!-- the route -->
<path class="rail" d="M{X_DECIDE} {RAIL_Y} H{X_LIVE}"/>
{lanes_svg}
<path class="tests" d="M{X_GATE+22} {RAIL_Y} H{X_LIVE-28}"/>

<!-- stations -->
<circle class="station lamp lamp-decide" cx="{X_DECIDE}" cy="{RAIL_Y}" r="13.5"/>
<circle class="station lamp lamp-check" cx="{X_CHECK}" cy="{RAIL_Y}" r="13.5"/>
<g transform="translate({X_GATE} {RAIL_Y}) rotate(45)">
  <rect class="gate" x="-15" y="-15" width="30" height="30"/>
  <rect class="gate-in" x="-10" y="-10" width="20" height="20"/>
</g>
<circle class="ping" cx="{X_LIVE}" cy="{RAIL_Y}" r="25"/>
<circle class="end live" cx="{X_LIVE}" cy="{RAIL_Y}" r="18"/>

<!-- the rider -->
<circle class="marker" r="8"/>

<!-- labels -->
<text class="h st" x="{X_DECIDE}" y="{RAIL_Y+48}">DECIDE</text>
<text class="q cap" x="{X_DECIDE}" y="{RAIL_Y+70}">what gets built</text>
<text class="q cap build-cap" x="{(X_DECIDE+X_CHECK)//2}" y="{RAIL_Y-52}">the agents build it</text>
<text class="h st" x="{X_CHECK}" y="{RAIL_Y+48}">CHECK</text>
<text class="q cap" x="{X_CHECK}" y="{RAIL_Y+70}">with my own eyes</text>
<text class="h st" x="{X_GATE}" y="{RAIL_Y+48}">SHIP IT?</text>
<text class="q cap" x="{X_GATE}" y="{RAIL_Y+70}">my call</text>
<text class="q cap tests-cap" x="{(X_GATE+X_LIVE)//2-10}" y="{RAIL_Y-24}">every test, in a fresh VM</text>
<text class="h st live-txt" x="{X_LIVE}" y="{RAIL_Y+48}">LIVE</text>
</svg>
"""
out = HERE.parent / "header.svg" if FREEZE is None else HERE / "frames" / f"t{FREEZE:05.2f}.svg"
out.parent.mkdir(exist_ok=True)
out.write_text(svg)
print("header.svg", len(svg.encode()), "bytes; loop", T, "s; merge at", round(t_merge, 2), "gate", round(t_at_gate, 2), "live", round(t_live, 2))
