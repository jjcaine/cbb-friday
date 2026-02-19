"""Download college basketball data for the 2025-26 season.

Pulls pre-built parquet files from the sportsdataverse GitHub releases
(ESPN-sourced data, all D1 teams). No API key needed.
"""

import pathlib

import pandas as pd

DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"
SEASON = 2025  # sportsdataverse uses the spring year (2024-25 season = 2025)

# sportsdataverse GitHub release URLs
PLAYER_BOX_URL = f"https://github.com/sportsdataverse/sportsdataverse-data/releases/download/espn_mens_college_basketball_player_boxscores/player_box_{SEASON}.parquet"
TEAM_BOX_URL = f"https://github.com/sportsdataverse/sportsdataverse-data/releases/download/espn_mens_college_basketball_team_boxscores/team_box_{SEASON}.parquet"
SCHEDULE_URL = f"https://github.com/sportsdataverse/sportsdataverse-data/releases/download/espn_mens_college_basketball_schedules/mbb_schedule_{SEASON}.parquet"


def download_player_boxscores() -> pd.DataFrame:
    print("Downloading player boxscores...")
    df = pd.read_parquet(PLAYER_BOX_URL)
    # Drop rows where player didn't play (no stats)
    df = df[df["did_not_play"] != True].copy()  # noqa: E712
    print(f"  {len(df):,} player-game rows, {df['athlete_display_name'].nunique():,} unique players")
    print(f"  Date range: {df['game_date'].min()} to {df['game_date'].max()}")
    return df


def download_team_boxscores() -> pd.DataFrame:
    print("Downloading team boxscores...")
    df = pd.read_parquet(TEAM_BOX_URL)
    print(f"  {len(df):,} team-game rows, {df['team_display_name'].nunique():,} unique teams")
    return df


def download_schedule() -> pd.DataFrame:
    print("Downloading schedule...")
    df = pd.read_parquet(SCHEDULE_URL)
    print(f"  {len(df):,} games")
    return df


def build_teams_csv(schedule: pd.DataFrame) -> pd.DataFrame:
    """Build a teams lookup table with conference info from the schedule."""
    print("Building teams table...")

    # Get conference ID -> name mapping from the groups columns
    conf_map = (
        schedule[["groups_id", "groups_name", "groups_short_name"]]
        .dropna(subset=["groups_id"])
        .drop_duplicates(subset=["groups_id"])
        .rename(columns={
            "groups_id": "conference_id",
            "groups_name": "conference_name",
            "groups_short_name": "conference_short_name",
        })
    )
    conf_map["conference_id"] = conf_map["conference_id"].astype(int)

    # Extract unique teams from home and away sides
    home = schedule[["home_id", "home_display_name", "home_abbreviation", "home_logo", "home_conference_id"]].copy()
    home.columns = ["team_id", "team_display_name", "team_abbreviation", "team_logo", "conference_id"]

    away = schedule[["away_id", "away_display_name", "away_abbreviation", "away_logo", "away_conference_id"]].copy()
    away.columns = ["team_id", "team_display_name", "team_abbreviation", "team_logo", "conference_id"]

    teams = pd.concat([home, away]).dropna(subset=["team_id"]).drop_duplicates(subset=["team_id"])
    teams["team_id"] = teams["team_id"].astype(int)
    teams["conference_id"] = teams["conference_id"].astype("Int64")  # nullable int

    # Merge conference names
    teams = teams.merge(conf_map, on="conference_id", how="left")
    teams = teams.sort_values("team_display_name").reset_index(drop=True)

    print(f"  {len(teams):,} teams across {teams['conference_name'].nunique()} conferences")

    # Spot-check Big East and A-10
    for conf in ["Big East Conference", "Atlantic 10 Conference"]:
        conf_teams = teams[teams["conference_name"] == conf]["team_display_name"].tolist()
        print(f"  {conf}: {', '.join(conf_teams)}")

    return teams


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Download all data
    player_box = download_player_boxscores()
    team_box = download_team_boxscores()
    schedule = download_schedule()
    teams = build_teams_csv(schedule)

    # Save to data/
    player_box.to_parquet(DATA_DIR / "player_boxscores.parquet", index=False)
    print(f"  -> data/player_boxscores.parquet")

    team_box.to_parquet(DATA_DIR / "team_boxscores.parquet", index=False)
    print(f"  -> data/team_boxscores.parquet")

    schedule.to_parquet(DATA_DIR / "schedule.parquet", index=False)
    print(f"  -> data/schedule.parquet")

    teams.to_csv(DATA_DIR / "teams.csv", index=False)
    print(f"  -> data/teams.csv")

    # Quick Xavier sanity check
    print("\n--- Xavier spot check ---")
    xavier_games = player_box[player_box["team_display_name"].str.contains("Xavier", na=False)]
    print(f"Xavier player-game rows: {len(xavier_games):,}")
    print(f"Xavier players: {xavier_games['athlete_display_name'].nunique()}")
    top_scorer = xavier_games.groupby("athlete_display_name")["points"].mean().sort_values(ascending=False).head(3)
    print("Top scorers (PPG):")
    for name, ppg in top_scorer.items():
        print(f"  {name}: {ppg:.1f}")

    print("\nDone! All data saved to data/")


if __name__ == "__main__":
    main()
