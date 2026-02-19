import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md("""
    # College Basketball Analysis — 2025-26 Season

    Player stats, Z-scores, hot streaks, and quad breakdowns.
    Data sourced from ESPN via sportsdataverse.
    """)
    return


@app.cell
def _():
    import pathlib

    import numpy as np
    import pandas as pd
    import plotly.express as px
    from scipy import stats

    import marimo as mo

    # Load data — resolve relative to this notebook file, not CWD
    data_dir = pathlib.Path(__file__).resolve().parent.parent / "data"
    player_box = pd.read_parquet(data_dir / "player_boxscores.parquet")
    team_box = pd.read_parquet(data_dir / "team_boxscores.parquet")
    schedule = pd.read_parquet(data_dir / "schedule.parquet")
    teams = pd.read_csv(data_dir / "teams.csv")
    return mo, player_box, schedule, teams


@app.cell
def _(mo, player_box, schedule, teams):
    mo.md(f"""
    ## Data Overview

    | | Count |
    |---|---:|
    | **Teams** | {teams['team_display_name'].nunique():,} |
    | **Games** | {schedule['id'].nunique():,} |
    | **Players** | {player_box['athlete_display_name'].nunique():,} |
    | **Player-game rows** | {len(player_box):,} |
    | **Date range** | {player_box['game_date'].min()} to {player_box['game_date'].max()} |
    | **Conferences** | {teams['conference_name'].nunique()} |
    """)
    return


@app.cell
def _(mo, teams):
    # Build dropdown options for Big East and A-10 teams
    focus_conferences = ["Big East Conference", "Atlantic 10 Conference"]
    focus_teams = (
        teams[teams["conference_name"].isin(focus_conferences)]
        .sort_values("team_display_name")
    )
    team_options = {row["team_display_name"]: row["team_id"] for _, row in focus_teams.iterrows()}

    team_dropdown = mo.ui.dropdown(
        options=team_options,
        value="Xavier Musketeers",
        label="Pick a team",
    )
    team_dropdown
    return (team_dropdown,)


@app.cell
def _(mo, player_box, team_dropdown):
    selected_team_id = team_dropdown.value
    team_games = player_box[player_box["team_id"] == selected_team_id]
    team_name = team_games["team_display_name"].iloc[0] if len(team_games) > 0 else "Unknown"
    n_games = team_games["game_id"].nunique()

    season_avgs = (
        team_games.groupby("athlete_display_name")[["points", "rebounds", "assists", "steals", "blocks", "turnovers", "minutes"]]
        .mean()
        .round(1)
        .sort_values("points", ascending=False)
        .head(10)
    )

    mo.md(f"### {team_name} — Top 10 by PPG ({n_games} games)")
    return (season_avgs,)


@app.cell
def _(mo, season_avgs):
    mo.ui.table(season_avgs.reset_index())
    return


if __name__ == "__main__":
    app.run()
