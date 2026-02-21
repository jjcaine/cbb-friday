# CBB Friday — College Basketball Analysis

Z-scores, auction values, hot player detection, and quad breakdowns for college basketball.
Built for live analysis with Claude Code + marimo.

**Data:** 2025-26 season, all D1 teams. Focus on Big East and A-10 conferences.

## Setup (one time)

1. Install uv (if you don't have it):
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone this repo and install dependencies:
   ```
   git clone https://github.com/jjcaine/cbb-friday.git
   cd cbb-friday
   uv sync
   ```

That's it. Two commands.

## Run the notebook

In one terminal, start the marimo notebook:

```
uv run marimo edit notebooks/cbb_analysis.py --watch
```

This opens an interactive notebook in your browser. The `--watch` flag auto-reloads when Claude Code edits the file, and marimo's reactive runtime re-runs affected cells automatically.

In a second terminal (same directory), start Claude Code:

```
claude
```

## The exercise

The notebook starts with a base setup: data loading, a data overview, a team dropdown, and a season averages table. From there, you use Claude Code to build out the analysis by giving it prompts. Here's what to walk through:

### Step 1: Get oriented

> Get up to speed on this repo. We're going to be doing some college basketball analysis in the cbb_analysis.py file, which is a marimo notebook.

This gets Claude to read the repo structure, the data files, the notebook, and understand what it's working with.

### Step 2: Z-scores across fantasy categories

> Calculate the Z-score for all Big East players across the following stats. These are the scoring categories in our fantasy league:
>
> - Assists (AST) — weight 1
> - Blocks (BLK) — weight 1
> - Points (PTS) — weight 1
> - Rebounds (REB) — weight 1
> - Steals (STL) — weight 1
> - Three Pointers Made (3PM) — weight 1
> - Turnovers (TO) — weight 1
> - Adjusted Field Goal % (AdjFG%) — weight 1
> - Free Throw % (FT%) — weight 1

Claude will add cells to the notebook that compute per-game averages, Z-score each category (inverting turnovers), and produce a composite Z-score ranking.

### Step 3: Visualize the distribution

> Plot the distribution of Z-scores for all players in the Big East.

Adds a histogram of composite Z-scores so you can see the spread.

### Step 4: Hot streak detection

> Show me the top 50 players in composite Z-score across the entire season and then versus their last 10 games, so we can compare and see who might be on a hot streak versus their composite score — who is undervalued when accounting for recency.

This is the most interesting one. Claude builds a season-vs-recent comparison using the season-wide mean/std (so the Z-scores are on the same scale), computes the delta, and visualizes it.

## Re-download data

Data is already included, but if you want to refresh it:

```
uv run python scripts/download_data.py
```

## What's in the data

| File | What it is |
|---|---|
| `data/player_boxscores.parquet` | Game-by-game player stats (points, rebounds, assists, etc.) for all D1 players |
| `data/team_boxscores.parquet` | Game-by-game team stats |
| `data/schedule.parquet` | Game results with home/away, scores, venue, rankings |
| `data/teams.csv` | Team info with conference assignments |
