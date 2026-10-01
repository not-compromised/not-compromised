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

I'm not an experienced developer. In February I asked Grok how to set up a server, and typed every command it gave me by hand.

What I'm good at is picking things up fast and working from first principles. When something breaks or bugs me, I don't patch it and move on. I ask why it happened, what would make it impossible, and build that.

## Eight months

| When | Version | What changed |
|---|---|---|
| Feb | v1 | Grok in a chat window. I typed every command. |
| Feb | v2 | Claude Code. The agent types, I say what I want. |
| Feb | v3 | A team of bots on chat. Nobody read their reports, me included. |
| Jun | v4 | Back after a month off, going ham. 296 commits in June, 1019 in July. |
| Jul | v5 | T3 Code: many threads, any machine, one shared context. |
| Aug | v6 | Omarchy: the desktop became something I just ask for. |
| Sep | v7 | Voice. An idea comes out as a rant, and the rant is the prompt. |

Every version fixed what bugged me about the last one.

## First principles, in practice

**The first Rocket League map worked, and it was bad.** More attempts weren't going to fix it, so I asked what makes a good map. My take after the first one: "yeah maybe our previous map wasnt too big it just wasn't intricate enough". The agent took a well-built community map apart in the editor, read Psyonix's standard arena straight out of the game, and now fires rays at our field and Psyonix's collision to check they match. [How the maps got good.](https://pmserver.us/rocket-league)

**When an agent gets something wrong, I don't just retry.** I ask what threw it off: my context, missing context, the model, or the framework. The fix goes into one context repo that every machine pulls every few minutes, so every agent (Claude, Codex, Grok, OpenCode) follows it from then on.

**A check that says "all clear" can be lying.** For two weeks my nightly security digest 404'd and never reached my phone, and its own self-test passed the whole time. Now I ask of every check what it looks like when it didn't run. A scan that didn't run never shows as all clear, and an audit in my map toolkit that passed with every mesh swapped for the wrong one got caught by a second model.

**Do I need to learn to code line by line?** I went back over my bugs to find out. About two-thirds of the ones you could see in code needed someone who knew what the money and data must always do, not someone who knew syntax. So that's what I'm learning. Each bug becomes an invariant for that app, written in my own words. It's rolling out one app at a time, and none has merged yet.

**I wanted to know how I actually work, not how I think I work.** So I had agents mine 740 of my own messages to them, and I change my setup from what that turns up.

## How I build

I decide what gets built, check it with my own eyes, and say ship it. Agents write the code. Every change runs every test in a throwaway VM on CI I built myself, and nothing red merges.

<details>
<summary>The full loop, from idea to live</summary>
<br>

<img src="./loop.svg" alt="The loop. Idea or issue: a voice rant, or a bug I hit using the app. Grill: one question at a time. Build: on a branch, never the live app. Try it: a preview copy, plus a different model's review. Ship it? My call; no goes back to Build. Fresh VM: every test, in a throwaway VM. Green? No goes back to Build: the agent reads the failure, fixes it and runs it again. Rollback rehearsal, only on the apps it's set up for: Finance, Dashboard, Tokdash. Live.">

</details>

What this doesn't prove: I don't write most of it line by line, some of the UI is rough, and none of it is finished. What software is?

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

<div align="center">
<sub>Security habits from a year of Cyber Operations at Dakota State University. Full story at <a href="https://pmserver.us/evolution">pmserver.us/evolution</a>.</sub>
</div>
