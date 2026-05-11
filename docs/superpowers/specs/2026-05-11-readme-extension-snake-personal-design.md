# README Extension: Snake + Personal Block — Design Spec

**Datum:** 2026-05-11  
**Repo:** milkamilch/milkamilch

---

## Ziel

Zwei Ergänzungen zum bestehenden GitHub-Profil-README:

1. **Personal Block** — `$ ps aux | grep lars` mit Interessen als Prozesse
2. **Contribution Snake** — animiertes SVG das täglich via GitHub Action generiert wird

---

## 1. Personal Block

### Position

Direkt nach dem Streak-Stats-Block (`$ github-stats`), vor der Snake.

### Inhalt

```
$ ps aux | grep lars
PID   COMMAND
1337  🎮 gaming
1338  🤾 handball
1339  🖥️  homelab
1340  ⛳ golf
```

### Umsetzung

Reines Markdown — fenced bash block mit dem Prompt, dann eine Code-Block-ähnliche Darstellung als weiterer fenced Block (oder einfacher plain block). Die PID-Tabelle kommt als fenced code block ohne Syntax-Highlighting.

---

## 2. Contribution Snake

### Position

Ganz unten im README — visueller Abschluss.

### Funktionsweise

- GitHub Action (`Platane/snk@v3`) generiert täglich ein SVG des Contribution-Graphen als animierte Schlange
- SVG wird in den Branch `output` des Repos gepusht: `github-contribution-grid-snake-dark.svg`
- README referenziert das SVG per `<picture>` Tag (dark/light Mode Support)

### Workflow-Datei

`.github/workflows/snake.yml` im Repo `milkamilch/milkamilch`:

```yaml
name: Generate Snake

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: Platane/snk@v3
        with:
          github_user_name: milkamilch
          outputs: |
            dist/github-contribution-grid-snake.svg
            dist/github-contribution-grid-snake-dark.svg?palette=github-dark
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - uses: crazy-max/ghaction-github-pages@v3
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### README-Einbindung

```markdown
<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/milkamilch/milkamilch/output/github-contribution-grid-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/milkamilch/milkamilch/output/github-contribution-grid-snake.svg" />
  <img src="https://raw.githubusercontent.com/milkamilch/milkamilch/output/github-contribution-grid-snake.svg" />
</picture>

</div>
```

### Voraussetzungen

Damit die Action den `output` Branch pushen kann, muss im Repo unter **Settings → Actions → General → Workflow permissions** `Read and write permissions` aktiviert sein.

---

## Reihenfolge im README (final)

1. Header (Typing Animation)
2. `$ whoami`
3. `$ cat current_project.txt`
4. `$ ls tech_stack/`
5. `$ github-stats` (Streak)
6. `$ ps aux | grep lars` ← neu
7. Contribution Snake ← neu

---

## Dateien

| Datei | Beschreibung |
|---|---|
| `README.md` | Personal Block + Snake `<picture>` Tag ergänzt |
| `.github/workflows/snake.yml` | GitHub Action für tägliche Snake-Generierung |
