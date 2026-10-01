<div align="center">

<a href="https://pmserver.us"><img src="./header.svg" alt="Peyton. I build the software I use every day. A transit strip map: one red line through Decide (what gets built), the agents build it, Check (with my own eyes), Ship it? (my call), every test in a fresh VM, then Live."></a>

<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpmserver.us%2Fapi%2Fpublic%2Fproof&query=%24.gate_merges&label=merges%20tested%20first&color=ee352e&style=flat-square" alt="merges tested first">
<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpmserver.us%2Fapi%2Fpublic%2Fproof&query=%24.vm_runs&label=CI%20runs%2C%20each%20in%20a%20fresh%20VM&color=000&style=flat-square" alt="CI runs%2C each in a fresh VM">
<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpmserver.us%2Fapi%2Fpublic%2Fproof&query=%24.caught_before_merge&label=caught%20before%20merge&color=ee352e&style=flat-square" alt="caught before merge">
<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpmserver.us%2Fapi%2Fpublic%2Fproof&query=%24.security_reports&label=nightly%20security%20reports&color=000&style=flat-square" alt="nightly security reports">

</div>

Hey, I'm Peyton, in Sioux Falls, SD. Everything here runs on one mini PC in my house, and most of it I use every day. In February I asked Grok how to set up a server and typed every command it gave me by hand. [Here's how that went.](https://pmserver.us/evolution)

## Things I've built

<table>
<tr>
<td width="50%" valign="top">
<img src="https://pmserver.us/assets/site/img/finance-month-desktop.png" alt="Finance app"><br>
<b>Finance</b> · <i>in daily use</i><br>
My money, fed by my bank through Plaid. Built around one rule: never show more cash than I actually have, and never show stale data as fresh.
</td>
<td width="50%" valign="top">
<img src="https://pmserver.us/assets/site/img/admin-cockpit-full.png" alt="Server dashboard"><br>
<b>Server dashboard</b> · <i>in daily use</i><br>
The cockpit for my server and the app behind <a href="https://pmserver.us">pmserver.us</a>. Every number comes from a live endpoint. No data, no panel.
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="https://pmserver.us/assets/site/img/firepos-desktop.png" alt="FirePOS"><br>
<b>FirePOS</b> · <i>built for a real business</i><br>
Point of sale and stock for a fireworks retailer that was stuck on a POS they didn't own. React PWA, Node, Postgres. Stock moves warehouse → container → tent, and it has to ring fast in a tent on any device.
</td>
<td width="50%" valign="top">
<img src="https://pmserver.us/assets/site/img/journey-desktop.png" alt="Journey"><br>
<b>Journey</b> · <i>built for a real business</i><br>
Booking for a family camper rental business: a public storefront with live availability, and an admin side for the owner.
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://pmserver.us/rocket-league"><img src="https://pmserver.us/assets/site/img/rl-andys-room-poster.jpg" alt="Andy's Room, a Rocket League map"></a><br>
<b>Rocket League maps</b> · <i>for fun</i><br>
Custom maps an agent builds by driving the level editor. The field gets checked against Psyonix's own by firing the same rays at both and comparing the hits. <a href="https://pmserver.us/rocket-league">How they got good.</a>
</td>
<td width="50%" valign="top">
<img src="https://pmserver.us/assets/site/img/server.jpg" alt="The server"><br>
<b>The server</b> · <i>runs all of it</i><br>
One mini PC in my house. Password manager, file sync, photos, a chat server that pings me when something breaks, and Minecraft for friends.
</td>
</tr>
</table>

## How I build

AI agents do most of the typing. My part is deciding what gets built, writing down the rules each app must never break, and building the checks that prove it.

- **My own CI.** It polls GitHub every two minutes, builds one integration commit from every ready PR, runs the unit tests and real browser runs in a fresh VM, then destroys the disk. Nothing merges unless that run is green.
- **Rollback rehearsals.** Start the old version, upgrade, undo. The data has to come back byte for byte. Set up for Finance, Dashboard and Tokdash so far.
- **A scanner that can't fake a quiet night.** A nightly security audit, and a scan that didn't run never shows as all clear. That rule exists because my digest once 404'd for two weeks while its own self-test passed.

<details>
<summary>The full loop, from idea to live</summary>
<br>

<img src="./loop.svg" alt="The loop. Idea or issue: a voice rant, or a bug I hit using the app. Grill: one question at a time. Build: on a branch, never the live app. Try it: a preview copy, plus a different model's review. Ship it? My call; no goes back to Build. Fresh VM: every test, in a throwaway VM. Green? No goes back to Build: the agent reads the failure, fixes it and runs it again. Rollback rehearsal, only on the apps it's set up for: Finance, Dashboard, Tokdash. Live.">

</details>

## Rabbit holes

- **Minecraft for friends.** Servers that sleep when nobody's on and wake up when someone connects.
- **A trading bot that has to prove itself.** Five instances paper-trade crypto to find out whether any strategy has a real edge. No real money until one does.
- **Tokdash.** My fork of Jingbiao Mei's AI usage meter, reporting from every machine.
- **My Omarchy desktop.** Widgets, keybinds and dictation, built in as I need them.

## Public repos

| Repo | What |
|---|---|
| [ground-up](https://github.com/not-compromised/ground-up) | A learning system you run with your coding agents, so AI-built repos stay yours to read |
| [skills-mcp](https://github.com/not-compromised/skills-mcp) | Some of my agent skills and MCP servers |

<div align="center">
<sub>Security habits from a year of Cyber Operations at Dakota State University. More at <a href="https://pmserver.us">pmserver.us</a>.</sub>
</div>
