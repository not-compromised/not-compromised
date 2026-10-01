#!/usr/bin/env python3
"""Generate loop.svg: the README's loop as a vertical route, in the same language as header.svg.
Usage: loop.py            -> ../loop.svg
       loop.py <seconds>  -> frames/loop-t<seconds>.svg, frozen at that moment (for screenshots)"""
import base64, pathlib, sys

HERE = pathlib.Path(__file__).parent
FREEZE = float(sys.argv[1]) if len(sys.argv) > 1 else None
def b64(p): return base64.b64encode((HERE / p).read_bytes()).decode()

PAGE, PANEL, INK, ROUTE, LIVE = "#c9cbc7", "#ffffff", "#000000", "#ee352e", "#00933c"
W = 560
T = 16  # seconds per loop

# --- geometry ---
RX = 118            # the rail
BX1, BX2 = 74, 48   # return tracks (no -> back to Build), SHIP IT? and GREEN?
SPX = RX + 46       # the rehearsal spur
TX = RX + 36        # label column
STEP = 78
Y = {}
names = ["idea", "grill", "build", "try", "ship", "vm", "green", "rehearse", "live"]
for i, n in enumerate(names):
    Y[n] = 64 + i * STEP
Y["rehearse"] += 6; Y["live"] += 10
H = Y["live"] + 58

def pct(s): return f"{s / T * 100:.2f}%"

# --- the ride: marker visits every stop on the main line (the spur is not every change's route) ---
ride = ["idea", "grill", "build", "try", "ship", "vm", "green", "live"]
DWELL, MOVE = 0.9, 0.7
arrive = {}
t = 0.6
for n in ride:
    arrive[n] = t
    t += DWELL + MOVE
t_end = T - 0.3

def ride_frames():
    out = [f"0%{{transform:translate({RX}px,{Y['idea']}px);opacity:0}}",
           f"{pct(0.5)}{{transform:translate({RX}px,{Y['idea']}px);opacity:1}}"]
    for n in ride:
        a = arrive[n]
        out.append(f"{pct(a)}{{transform:translate({RX}px,{Y[n]}px);opacity:1}}")
        out.append(f"{pct(a + DWELL)}{{transform:translate({RX}px,{Y[n]}px);opacity:1}}")
    out.append(f"{pct(arrive['live'] + 0.05)}{{opacity:0}}")
    out.append(f"100%{{transform:translate({RX}px,{Y['live']}px);opacity:0}}")
    return "\n  ".join(out)

def lamp(n):  # station solid while the marker dwells
    return f".lamp-{n}{{animation-name:lamp-{n}}}@keyframes lamp-{n}{{0%{{fill:{PANEL}}}{pct(arrive[n])}{{fill:{INK}}}{pct(arrive[n]+DWELL)}{{fill:{PANEL}}}100%{{fill:{PANEL}}}}}"

def gate_css(n):  # a gate stays inverted once he has passed it
    return (f".gate-{n}{{animation:gate-{n} {T}s step-end infinite}}@keyframes gate-{n}{{0%{{fill:{PANEL}}}{pct(arrive[n])}{{fill:{INK}}}{pct(t_end)}{{fill:{PANEL}}}100%{{fill:{PANEL}}}}}"
            f".gatein-{n}{{animation:gatein-{n} {T}s step-end infinite}}@keyframes gatein-{n}{{0%{{opacity:0}}{pct(arrive[n])}{{opacity:1}}{pct(t_end)}{{opacity:0}}100%{{opacity:0}}}}")

css = f"""
@font-face{{font-family:"ArchivoC";src:url(data:font/woff2;base64,{b64('archivo-800-72.woff2')}) format("woff2");font-weight:800}}
@font-face{{font-family:"ArchivoR";src:url(data:font/woff2;base64,{b64('archivo-700-100.woff2')}) format("woff2");font-weight:700}}
@font-face{{font-family:"CourierP";src:url(data:font/woff2;base64,{b64('courier-sub.woff2')}) format("woff2")}}
.h{{font-family:"ArchivoC","Archivo Narrow","Arial Narrow",Impact,sans-serif;font-weight:800;fill:{INK};font-size:27px;letter-spacing:0.01em}}
.r{{font-family:"ArchivoR","Archivo",Arial,sans-serif;font-weight:700;fill:{INK};font-size:14px}}
.q{{font-family:"CourierP","Courier Prime","Courier New",monospace;fill:{INK};font-size:16px}}
.rail{{stroke:{ROUTE};stroke-width:12;fill:none}}
.spur{{stroke:{ROUTE};stroke-width:5;fill:none;stroke-dasharray:9 7;stroke-linecap:butt}}
.back{{stroke:{INK};stroke-width:3;fill:none;stroke-linejoin:round}}
.station{{fill:{PANEL};stroke:{INK};stroke-width:7}}
.small{{fill:{PANEL};stroke:{INK};stroke-width:5}}
.end{{fill:{PANEL};stroke:{INK};stroke-width:10}}
.gate{{fill:{PANEL};stroke:{INK};stroke-width:3}}
.gatein{{fill:none;stroke:{PANEL};stroke-width:4;opacity:0}}
.marker{{fill:{INK};stroke:{PANEL};stroke-width:3;animation:ride {T}s linear infinite}}
@keyframes ride{{
  {ride_frames()}
}}
.lamp{{animation-duration:{T}s;animation-iteration-count:infinite;animation-timing-function:step-end}}
{''.join(lamp(n) for n in ["idea","grill","build","try","vm"])}
{gate_css("ship")}{gate_css("green")}
.live{{animation:liveA {T}s step-end infinite}}
@keyframes liveA{{0%{{fill:{PANEL}}}{pct(arrive['live'])}{{fill:{LIVE}}}{pct(t_end)}{{fill:{PANEL}}}100%{{fill:{PANEL}}}}}
.live-txt{{animation:liveB {T}s step-end infinite}}
@keyframes liveB{{0%{{fill:{INK}}}{pct(arrive['live'])}{{fill:{LIVE}}}{pct(t_end)}{{fill:{INK}}}100%{{fill:{INK}}}}}
.ping{{fill:none;stroke:{LIVE};stroke-width:3;opacity:0;transform-origin:{RX}px {Y['live']}px;animation:pingA {T}s linear infinite}}
@keyframes pingA{{
  0%,{pct(arrive['live'])}{{transform:scale(1);opacity:0}}
  {pct(arrive['live']+0.05)}{{transform:scale(1);opacity:1}}
  {pct(arrive['live']+1.0)}{{transform:scale(1.8);opacity:0}}
  {pct(arrive['live']+1.01)}{{transform:scale(1);opacity:0}}
  {pct(arrive['live']+1.2)}{{transform:scale(1);opacity:1}}
  {pct(arrive['live']+2.1)}{{transform:scale(1.8);opacity:0}}
  100%{{opacity:0}}
}}
.marker,.lamp,.gate,.gatein,.live,.live-txt,.ping{{animation-delay:var(--f)}}
@media (prefers-reduced-motion:reduce){{
  .marker,.lamp,.gate,.gatein,.live,.live-txt,.ping{{animation:none}}
  .marker{{opacity:0}} .gate{{fill:{INK}}} .gatein{{opacity:1}}
  .live{{fill:{LIVE}}} .live-txt{{fill:{LIVE}}}
}}
"""

def station(n, cls="station lamp", r=13.5):
    return f'<circle class="{cls} lamp-{n}" cx="{RX}" cy="{Y[n]}" r="{r}"/>'

def gate(n):
    return (f'<g transform="translate({RX} {Y[n]}) rotate(45)"><rect class="gate gate-{n}" x="-15" y="-15" width="30" height="30"/>'
            f'<rect class="gatein gatein-{n}" x="-10" y="-10" width="20" height="20"/></g>')

def label(n, name, lines, x=TX):
    y = Y[n]
    out = [f'<text class="h" x="{x}" y="{y+10}">{name}</text>']
    for i, ln in enumerate(lines):
        out.append(f'<text class="q" x="{x}" y="{y+32+i*19}">{ln}</text>')
    return "\n".join(out)

# return tracks: from the gate's left point, out to a column, up to Build, into the station
yb = Y["build"]
back_ship = f"M{RX-20} {Y['ship']} H{BX1} V{yb} H{RX-20}"
back_green = f"M{RX-20} {Y['green']} H{BX2} V{yb} H{BX1}"
arrow = f'<path fill="{INK}" d="M{RX-22} {yb-7} L{RX-10} {yb} L{RX-22} {yb+7} Z"/>'

# the rehearsal spur: leaves the rail after Green?, passes its own stop, rejoins before Live
ys0, ys1 = Y["green"] + 34, Y["live"] - 34
yr = Y["rehearse"]
spur = (f"M{RX} {ys0} C{RX} {ys0+26} {SPX} {yr-40} {SPX} {yr-14} V{yr+14} "
        f"C{SPX} {yr+40} {RX} {ys1-26} {RX} {ys1}")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">The loop</title>
<desc id="d">Idea or issue: a voice rant, or a bug I hit using the app. Grill: one question at a time. Build: on a branch, never the live app. Try it: a preview copy, plus a different model's review. Ship it? My call; no goes back to Build. Fresh VM: every test, in a throwaway VM. Green? No goes back to Build: the agent reads the failure, fixes it and runs it again. Rollback rehearsal, only on the apps it is set up for: Finance, Dashboard, Tokdash. Live.</desc>
<style>:root{{--f:{"-%.2fs" % FREEZE if FREEZE is not None else "0s"}}}{"svg *{animation-play-state:paused !important}" if FREEZE is not None else ""}{css}</style>
<rect width="{W}" height="{H}" fill="{PAGE}"/>
<rect x="10" y="10" width="{W-20}" height="{H-20}" fill="{PANEL}"/>

<!-- no -> back to Build -->
<path class="back" d="{back_green}"/>
<path class="back" d="{back_ship}"/>
{arrow}
<text class="r" x="{RX-24}" y="{Y['ship']-7}" text-anchor="end">no</text>
<text class="r" x="{RX-24}" y="{Y['green']-7}" text-anchor="end">no</text>

<!-- the route -->
<path class="rail" d="M{RX} {Y['idea']} V{Y['live']}"/>
<path class="spur" d="{spur}"/>
<text class="r" x="{RX-12}" y="{Y['ship']+36}" text-anchor="end">yes</text>
<text class="r" x="{RX-12}" y="{Y['green']+36}" text-anchor="end">yes</text>

<!-- stops -->
{station("idea")}
{station("grill")}
{station("build")}
{station("try")}
{gate("ship")}
{station("vm")}
{gate("green")}
<circle class="small" cx="{SPX}" cy="{yr}" r="10"/>
<circle class="ping" cx="{RX}" cy="{Y['live']}" r="25"/>
<circle class="end live" cx="{RX}" cy="{Y['live']}" r="18"/>
<circle class="marker" r="8"/>

<!-- labels -->
{label("idea", "IDEA / ISSUE", ["a voice rant, or a bug I hit", "using the app"])}
{label("grill", "GRILL", ["one question at a time"])}
{label("build", "BUILD", ["on a branch, never the live app"])}
{label("try", "TRY IT", ["a preview copy, plus a", "different model's review"])}
{label("ship", "SHIP IT?", ["my call"])}
{label("vm", "FRESH VM", ["every test, in a throwaway VM"])}
{label("green", "GREEN?", ["no: the agent reads the failure,", "fixes it and runs it again"])}
{label("rehearse", "ROLLBACK REHEARSAL", ["only on the apps it's set up for:", "Finance, Dashboard, Tokdash"], x=SPX+28)}
<text class="h live-txt" x="{TX}" y="{Y['live']+10}">LIVE</text>
</svg>
"""
if FREEZE is None:
    out = HERE.parent / "loop.svg"
else:
    out = HERE / "frames" / f"loop-t{FREEZE:05.2f}.svg"; out.parent.mkdir(exist_ok=True)
out.write_text(svg)
print(out, len(svg.encode()), "bytes;", W, "x", H, "; live at", round(arrive["live"], 2), "s")
