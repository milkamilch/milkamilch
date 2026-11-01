<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,100:39ff14&height=180&section=header&text=Lars%20Wenner&fontSize=42&fontColor=39ff14&animation=fadeIn&fontAlignY=38&desc=Backend%20Dev%20%C2%B7%20M.Sc.%20Student%20%C2%B7%20Builder&descAlignY=58&descSize=18&descColor=e6fce6)

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&pause=1000&color=39FF14&center=true&vCenter=true&width=560&lines=whoami+%3E+backend+dev+%40+zolitron+%F0%9F%91%BE;currently+%3E+routing+garbage+trucks+with+OR-Tools+%F0%9F%9A%9B;also+%3E+doing+a+master%27s+on+the+side+%F0%9F%8E%93;known+issue+%3E+JS+skills+%28wontfix%29)](https://github.com/milkamilch)

</div>

```bash
lars@dortmund:~$ neofetch
```

<div align="center">

<img alt="neofetch" width="100%" src="https://raw.githubusercontent.com/milkamilch/milkamilch/output/neofetch.svg" />

</div>

```bash
lars@dortmund:~$ cat about.md
```

> 💼 **Backend Developer at Zolitron** — tour planning for waste collection: Java · Spring Boot · OR-Tools<br>
> 🎓 **M.Sc. Business Informatics** (Wirtschaftsinformatik), in progress · B.Sc. 2026 ✔<br>
> 🧠 Into optimization problems, backends that don't page you at 3 a.m., and homelabs<br>
> 🌍 Dortmund, Germany

```text
lars@dortmund:~$ // ──────────────────────────────────────────────
```

```bash
lars@dortmund:~$ ls -l ~/projects
```

| | Project | What it does | Stack |
|---|---|---|---|
| 🎓 | **[ztp-ki-framework](https://github.com/milkamilch/ztp-ki-framework)** | My B.Sc. thesis: zero-touch provisioning for bare-metal servers that detects failures live and heals itself (retry / reboot / rollback). Research question: from how many servers on does it pay off for SMEs? | `Python` `Isolation Forest` `Redfish` `Ansible` |
| 🐳 | **[env-buddy](https://github.com/milkamilch/env-buddy)** | Self-service dashboard for on-demand Docker test environments — start, stop, snapshot, share with the team | `FastAPI` `React` `Docker` |
| 🧩 | **[PersonalOs](https://github.com/milkamilch/PersonalOs)** | Self-hosted productivity PWA — habits, goals, journal, finance, plus a Claude-powered assistant with RAG over my own docs | `Spring Boot` `React` `RAG` |
| ⛳ | **[FairwayIQ](https://github.com/milkamilch/FairwayIQ)** | Golf app with AI swing analysis via pose estimation, round & handicap tracking | `Expo` `Prisma` `MediaPipe` |
| ➗ | **[Kalkulix](https://github.com/milkamilch/Kalkulix)** | Real-time 1v1 math duels with ELO, streaks and quests — QuizDuel, but the questions fight back | `Expo` `Fastify` `tRPC` `Socket.io` |
| 💪 | **[TrainingsApp](https://github.com/milkamilch/TrainingsApp)** | iOS workout tracker that writes the plan and bumps the weights for you | `SwiftUI` `SwiftData` |
| 📺 | **[iptv-player](https://github.com/milkamilch/iptv-player)** | Lightweight desktop IPTV player — Xtream Codes / M3U, EPG, HLS · [download](https://github.com/milkamilch/iptv-player/releases/latest) | `Electron` `React` |

```bash
lars@dortmund:~$ cat FairwayIQ/architecture.md
```

```mermaid
flowchart LR
    Mobile["📱 Expo App"] -->|REST + JWT| Backend["Express API\n(Prisma)"]
    Backend --> Postgres[("PostgreSQL")]
    Backend -->|swing video| MLService["swing-ml\n(MediaPipe Pose)"]
    MLService -->|metrics| Backend
```

```text
lars@dortmund:~$ // ──────────────────────────────────────────────
```

```bash
lars@dortmund:~$ ls tech_stack/
```

![Java](https://img.shields.io/badge/Java_25-21262d?style=flat-square&logo=openjdk&logoColor=39ff14)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-21262d?style=flat-square&logo=springboot&logoColor=39ff14)
![OR-Tools](https://img.shields.io/badge/OR--Tools-21262d?style=flat-square&logo=google&logoColor=39ff14)
![Python](https://img.shields.io/badge/Python-21262d?style=flat-square&logo=python&logoColor=39ff14)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-21262d?style=flat-square&logo=postgresql&logoColor=39ff14)
![Redis](https://img.shields.io/badge/Redis-21262d?style=flat-square&logo=redis&logoColor=39ff14)
![Docker](https://img.shields.io/badge/Docker-21262d?style=flat-square&logo=docker&logoColor=39ff14)
![Ansible](https://img.shields.io/badge/Ansible-21262d?style=flat-square&logo=ansible&logoColor=39ff14)
![TypeScript](https://img.shields.io/badge/TypeScript-21262d?style=flat-square&logo=typescript&logoColor=39ff14)
![React](https://img.shields.io/badge/React_19-21262d?style=flat-square&logo=react&logoColor=39ff14)
![Vue](https://img.shields.io/badge/Vue_3-21262d?style=flat-square&logo=vuedotjs&logoColor=39ff14)
![Arch Linux](https://img.shields.io/badge/Arch_Linux_%28btw%29-21262d?style=flat-square&logo=archlinux&logoColor=39ff14)

```text
lars@dortmund:~$ // ──────────────────────────────────────────────
```

```bash
lars@dortmund:~$ cat ~/.todo
```

```diff
+ [x] B.Sc. Business Informatics
+ [x] Get a job where my routes end up in real trucks
! [ ] M.Sc. Business Informatics          # compiling…
! [ ] Lower my golf handicap              # FairwayIQ is on it
- [ ] Understand JavaScript               # wontfix
```

```bash
lars@dortmund:~$ ps aux | grep lars
```

```
PID   COMMAND
1337  🎮 gaming
1338  🤾 handball
1339  🖥️  homelab
1340  ⛳ golf
1341  📚 studying (nice -n 19)
```

<div align="center">

[![GitHub Streak](https://streak-stats.demolab.com?user=milkamilch&theme=chartreuse-dark&hide_border=true&date_format=j.%20n.%5B%20Y%5D)](https://git.io/streak-stats)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/milkamilch/milkamilch/output/github-contribution-grid-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/milkamilch/milkamilch/output/github-contribution-grid-snake.svg" />
  <img alt="contribution snake" src="https://raw.githubusercontent.com/milkamilch/milkamilch/output/github-contribution-grid-snake.svg" />
</picture>

![Profile Views](https://komarev.com/ghpvc/?username=milkamilch&color=39ff14&style=flat-square&label=profile+views)

</div>
