<div align="center">

<a href="https://pmserver.us"><img src="./header.svg" alt="Peyton. I build software at night by directing AI agents. A transit strip map: one red line through Decide (what gets built), the agents build it, Check (with my own eyes), Ship it? (my call), every test in a fresh VM, then Live."></a>


<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpmserver.us%2Fapi%2Fpublic%2Fproof&query=%24.gate_merges&label=merges%20tested%20first&color=ee352e&style=flat-square" alt="merges tested first">
<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpmserver.us%2Fapi%2Fpublic%2Fproof&query=%24.vm_runs&label=CI%20runs%2C%20each%20in%20a%20fresh%20VM&color=000&style=flat-square" alt="CI runs">
<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpmserver.us%2Fapi%2Fpublic%2Fproof&query=%24.caught_before_merge&label=caught%20before%20merge&color=ee352e&style=flat-square" alt="caught before merge">
<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpmserver.us%2Fapi%2Fpublic%2Fproof&query=%24.security_reports&label=nightly%20security%20reports&color=000&style=flat-square" alt="nightly security reports">
<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpmserver.us%2Fapi%2Fpublic%2Ftokens&query=%24.sessions_this_month&label=agent%20sessions%20this%20month&color=ee352e&style=flat-square" alt="agent sessions this month">
<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpmserver.us%2Fapi%2Fpublic%2Ftokens&query=%24.peak_agents_this_month&label=peak%20agents%20at%20once&color=000&style=flat-square" alt="peak agents at once">

<sub>Live from my server's own records. 22 billion tokens since March (as of Sep 30, 2026), mostly agents re-reading code.</sub>

</div>

---

I'm self-taught, in Sioux Falls, SD. In February I asked Grok how to set up a server and typed every command it gave me by hand. Eight months later, one mini PC at home runs 20+ services, my own CI, a nightly security audit, and the AI agents I direct from my desk and my phone.

I don't write most of my code. I decide what gets built, check it with my own eyes, and say ship it.

## What I added on top

The process is the standard stuff: branches, review, CI, rollbacks. I got there one annoyance at a time. What's mine is how the agents are run.

- **One context, every agent.** My rules for how work gets done live in one private repo. Every machine pulls it every few minutes, and Claude, Codex, Grok and OpenCode all read the same thing.
- **A bad agent run is a context bug.** When an agent screws up, I ask what threw it off: my context, missing context, the model, or the framework. The fix goes into the context, and every agent follows it from then on.
- **Models check each other.** A different model reviews each change and can't edit anything. A second one, with none of the builder's context, reads diffs for security holes. Anything touching money gets its own review.
- **Agents get their own desktop.** They can take a screen, keyboard and mouse and drive real apps.
- **Bugs become rules in my own words.** Each bug I hit becomes an invariant, something the app must always get right, stated in plain English. Rolling out one app at a time. None has merged yet.

<details>
<summary>The full loop, from idea to live</summary>
<br>

<img src="./loop.svg" alt="The loop. Idea or issue: a voice rant, or a bug I hit using the app. Grill: one question at a time. Build: on a branch, never the live app. Try it: a preview copy, plus a different model's review. Ship it? My call; no goes back to Build. Fresh VM: every test, in a throwaway VM. Green? No goes back to Build: the agent reads the failure, fixes it and runs it again. Rollback rehearsal, only on the apps it's set up for: Finance, Dashboard, Tokdash. Live.">

</details>

## What it's caught

The worst bugs are the ones where everything looks fine.

- For two weeks my nightly security digest 404'd and never reached my phone, and its own self-test passed the whole time. The same fix found a report section that had been silently dropped, because the list of watched files had outgrown Linux's argument-length limit. Now the self-test fails on both, and a scan that didn't run never shows as all clear.
- An audit in my Rocket League map toolkit still passed with every mesh swapped for the wrong one. A second model caught it.
- My CI gives every run a throwaway VM with no passwords or real data, and it does the merging, so nothing red lands. Since it went live on Sep 20, 38 of 239 runs caught a problem before merge (as of Sep 30; the badges up top are live).
- Rollbacks get rehearsed on Finance, Dashboard and Tokdash: start the old version, upgrade, undo. The data has to come back byte for byte.

What this doesn't prove: some of the UI is rough, and none of it is finished. What software is?

## What came out of it

<table>
<tr>
<td width="50%" valign="top">
<img src="https://pmserver.us/assets/site/img/finance-month-desktop.png" alt="Finance app"><br>
<b>Finance</b> · <i>in daily use</i><br>
My money dashboard, fed by my bank.
</td>
<td width="50%" valign="top">
<img src="https://pmserver.us/assets/site/img/admin-cockpit-full.png" alt="Server dashboard"><br>
<b>Server dashboard</b> · <i>in daily use</i><br>
The cockpit for my server, and the app behind <a href="https://pmserver.us">pmserver.us</a>.
</td>
</tr>
<tr>
<td valign="top">
<img src="https://pmserver.us/assets/site/img/firepos-desktop.png" alt="FirePOS"><br>
<b>FirePOS</b> · <i>built for a real business</i><br>
Point of sale and stock for fireworks tents. 148 commits in its first 3 days.
</td>
<td valign="top">
<img src="https://pmserver.us/assets/site/img/journey-desktop.png" alt="Journey"><br>
<b>Journey</b> · <i>built for a real business</i><br>
Booking for a family camper rental business.
</td>
</tr>
<tr>
<td valign="top">
<a href="https://pmserver.us/rocket-league"><img src="https://pmserver.us/assets/site/img/rl-andys-room-poster.jpg" alt="Andy's Room, a Rocket League map"></a><br>
<b>Rocket League maps</b> · <i>for fun</i><br>
An agent builds them by driving the level editor. This is Andy's Room, a ring run through a Toy Story bedroom. The first maps worked and were bad. <a href="https://pmserver.us/rocket-league">How they got good.</a>
</td>
<td valign="top">
<img src="https://pmserver.us/assets/site/img/server.jpg" alt="The server"><br>
<b>The server</b> · <i>runs all of it</i><br>
Password manager, file sync, photos, a Discord-like chat the server talks to me in, uptime checks, and Minecraft for friends.
</td>
</tr>
</table>

Also: **Tokdash** (my AI usage meter, a fork of Jingbiao Mei's), my **Omarchy** desktop setup, and a crypto **trader bot** that paper-trades to find out if a strategy really works.

## Public repos

| Repo | What |
|---|---|
| [ground-up](https://github.com/not-compromised/ground-up) | A learning system you run with your coding agents, so AI-built repos stay yours to read |
| [skills-mcp](https://github.com/not-compromised/skills-mcp) | Some of my agent skills and MCP servers |

## How it got here

| When | Version | What changed |
|---|---|---|
| Feb | v1 | Grok in a chat window. I typed every command. |
| Feb | v2 | Claude Code. The agent types, I say what I want. |
| Feb | v3 | A team of bots on chat. Nobody read their reports, me included. |
| Jun | v4 | Back after a month off, going ham. 296 commits in June, 1019 in July. |
| Jul | v5 | T3 Code: many threads, any machine, one shared context. |
| Aug | v6 | Omarchy: the desktop became something I just ask for. |
| Sep | v7 | Voice. An idea comes out as a rant, and the rant is the prompt. |

<div align="center">
<sub>Security habits from a year of Cyber Operations at Dakota State University. Full story at <a href="https://pmserver.us/evolution">pmserver.us/evolution</a>.</sub>
</div>
