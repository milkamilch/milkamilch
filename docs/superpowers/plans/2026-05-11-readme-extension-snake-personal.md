# README Extension: Snake + Personal Block Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `$ ps aux | grep lars` personal interests block and an animated contribution snake (via GitHub Action) to the existing GitHub profile README.

**Architecture:** Two independent additions to `README.md` in `/home/lars/milkamilch/`, plus one new GitHub Actions workflow file. The snake is generated daily by `Platane/snk@v3`, pushed to the `output` branch, and embedded via a `<picture>` tag that supports dark/light mode. The personal block is pure Markdown appended before the snake.

**Tech Stack:** GitHub Markdown, GitHub Actions (Platane/snk@v3, crazy-max/ghaction-github-pages@v3), YAML

---

## File Structure

```
milkamilch/milkamilch/
├── README.md                          ← append personal block + snake picture tag
└── .github/
    └── workflows/
        └── snake.yml                  ← create: daily snake generation action
```

---

### Task 1: Add personal block to README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Verify current README ends with the streak stats block**

  ```bash
  tail -10 README.md
  ```

  Expected: last lines contain `</div>` closing the streak stats center-div.

- [ ] **Step 2: Append the personal block**

  Add this content at the end of `README.md`:

  ````markdown
  <br>

  ```bash
  $ ps aux | grep lars
  ```

  ```
  PID   COMMAND
  1337  🎮 gaming
  1338  🤾 handball
  1339  🖥️  homelab
  1340  ⛳ golf
  ```
  ````

  The first fenced block (` ```bash `) shows the prompt. The second fenced block (` ``` ` with no language) renders the PID table in monospace.

- [ ] **Step 3: Verify the appended content looks correct**

  ```bash
  tail -15 README.md
  ```

  Expected: both code blocks visible, properly closed, PID table present.

- [ ] **Step 4: Commit**

  ```bash
  git add README.md
  git commit -m "feat: add personal interests block (ps aux)"
  ```

---

### Task 2: Create GitHub Actions snake workflow

**Files:**
- Create: `.github/workflows/snake.yml`

- [ ] **Step 1: Create the workflows directory**

  ```bash
  mkdir -p .github/workflows
  ```

- [ ] **Step 2: Write the workflow file**

  Create `.github/workflows/snake.yml` with this exact content:

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

- [ ] **Step 3: Validate the YAML syntax**

  ```bash
  python3 -c "import yaml; yaml.safe_load(open('.github/workflows/snake.yml'))" && echo "YAML valid"
  ```

  Expected: `YAML valid`

- [ ] **Step 4: Commit**

  ```bash
  git add .github/workflows/snake.yml
  git commit -m "feat: add daily snake generation GitHub Action"
  ```

---

### Task 3: Add snake picture tag to README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Append the snake section at the end of README.md**

  Add this content at the very end of `README.md`:

  ```markdown
  <br>

  <div align="center">

  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/milkamilch/milkamilch/output/github-contribution-grid-snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/milkamilch/milkamilch/output/github-contribution-grid-snake.svg" />
    <img alt="contribution snake" src="https://raw.githubusercontent.com/milkamilch/milkamilch/output/github-contribution-grid-snake.svg" />
  </picture>

  </div>
  ```

- [ ] **Step 2: Verify the full end of README.md**

  ```bash
  tail -20 README.md
  ```

  Expected: personal block + snake picture block both present, `</div>` closes the center div.

- [ ] **Step 3: Commit**

  ```bash
  git add README.md
  git commit -m "feat: add contribution snake to README"
  ```

---

### Task 4: Manual steps (user must do these after pushing)

These steps cannot be automated and must be done by the user on GitHub:

- [ ] **Step 1: Enable workflow write permissions**

  Go to: `https://github.com/milkamilch/milkamilch/settings/actions`

  Under **Workflow permissions** → select **Read and write permissions** → Save.

  Without this, the Action cannot push to the `output` branch and will fail with a 403.

- [ ] **Step 2: Push to GitHub and trigger the Action manually**

  ```bash
  git push origin main
  ```

  Then go to: `https://github.com/milkamilch/milkamilch/actions`

  Find "Generate Snake" → click **Run workflow** → **Run workflow** (green button).

  Wait ~30 seconds. The `output` branch should appear with the SVG files.

- [ ] **Step 3: Verify the snake renders on your profile**

  Go to `https://github.com/milkamilch` — the snake animation should appear at the bottom of the README.

  If it shows a broken image instead: the `output` branch doesn't exist yet — re-trigger the workflow and wait.
