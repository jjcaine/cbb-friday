# CBB Friday — College Basketball Analysis

Z-scores, auction values, hot player detection, and quad breakdowns for college basketball.
Built for live analysis with Claude Code + marimo.

**Data:** 2024-25 season, all D1 teams. Focus on Big East and A-10 conferences.

## Setup (one time)

1. Install uv (if you don't have it):
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone this repo and install dependencies:
   ```
   git clone <url>
   cd cbb-friday
   uv sync
   ```

That's it. Two commands.

## Run the notebook

```
uv run marimo edit notebooks/cbb_analysis.py
```

This opens an interactive notebook in your browser. From there, Claude Code builds out the analysis live.

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

## Things to ask Claude during the session

- "Calculate Z-scores for all Big East players across points, rebounds, assists, steals, blocks, turnovers, FG%, FT%, 3PM"
- "Show me the top 10 value plays in Big East based on composite Z-score"
- "Compare the last 10 games vs season average for Xavier players — who's trending up?"
- "Calculate quad records for Xavier — explain what quad 1/2/3/4 means and show their record in each"
- "Show a heatmap of Z-scores for the top 20 Big East players"
