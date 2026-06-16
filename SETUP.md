# Setting up the GitHub Repository

This guide walks you through pushing the AI Infrastructure Almanac to GitHub and setting up the automation for regular updates.

## Step 1: Create the GitHub repository

```bash
# Option A: Via GitHub CLI (if installed)
gh repo create ai-infrastructure-almanac --public --description "A living encyclopedia of AI infrastructure tools — the systems that make AI/LLM production-ready." --license cc-by-4.0

# Option B: Via GitHub web UI
# 1. Go to https://github.com/new
# 2. Name: ai-infrastructure-almanac
# 3. Description: A living encyclopedia of AI infrastructure tools
# 4. Visibility: Public
# 5. License: CC BY 4.0
# 6. Click "Create repository"
```

## Step 2: Initialize and push the local repo

```bash
cd /path/to/ai-infrastructure-almanac

git init
git add .
git commit -m "Founding edition: 670+ tools across 8 categories, June 2026"

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/ai-infrastructure-almanac.git
# OR if using SSH:
git remote add origin git@github.com:YOUR_USERNAME/ai-infrastructure-almanac.git

git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Actions for automated updates (optional)

Create `.github/workflows/monthly-update.yml`:

```yaml
name: Monthly Edition Update

on:
  schedule:
    - cron: '0 7 1 * *'  # 7:00 AM UTC on the 1st of each month
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - name: Update metadata
        run: |
          # This is where you'd run a script to refresh GitHub stars,
          # last push dates, release notes, etc.
          echo "$(date +%Y-%m-%d) Monthly update triggered" >> editions/update.log
      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git commit -m "Monthly edition update: $(date +%Y-%m)" || echo "No changes"
          git push
```

## Step 4: Set up a cron job for research (local agent)

The research and benchmark updates are run by an agent on a schedule. To set this up in Kimi Work:

```bash
# The cron job has been configured to run monthly on the 15th at 07:00 AM
# It will refresh the research, update editions, and flag new tools for triage.
```

The cron job is configured via the Kimi Work `Cron` tool with:
- **Trigger**: `cron` expression `0 7 15 * *` (monthly, 15th at 7:00 AM)
- **Workspace**: Your local workspace
- **Prompt**: "Refresh the AI Infrastructure Almanac: check for new tools, updated metadata, notable releases, and prepare the next edition draft."

## Directory structure after setup

```
ai-infrastructure-almanac/
├── README.md                          # Project overview
├── architecture.md                    # Stack architecture + how we test
├── SETUP.md                           # This file
├── .github/
│   └── workflows/
│       └── monthly-update.yml         # GitHub Actions for metadata refresh
├── categories/                        # 12 category directories
│   ├── code-editors/
│   ├── agent-frameworks/
│   ├── observability/
│   ├── vector-databases/
│   ├── model-serving/
│   ├── security-guardrails/
│   ├── llmops-platforms/
│   ├── context-protocols/
│   ├── authentication/                # Cross-reference to context-protocols
│   ├── evaluation-testing/            # Cross-reference to observability + security
│   ├── prompt-management/             # Cross-reference to llmops-platforms
│   └── data-processing/               # Cross-reference to vector-databases
├── editions/                          # Monthly editions
│   └── 2026-06.md                   # Founding edition
├── benchmarks/                        # Benchmark results
│   └── methodology.md               # How we test
├── methodology/
│   └── benchmark-harness.md         # Detailed harness spec
├── data/
│   └── roster.json                    # Machine-readable catalog (547 tools)
└── assets/                            # Charts, diagrams, screenshots
    └── (populated by editions)
```

## License

Content: CC BY 4.0  
Code/harness: MIT
