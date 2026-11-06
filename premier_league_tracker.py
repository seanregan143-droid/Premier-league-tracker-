
import streamlit as st
import pandas as pd
from pathlib import Path


# Page settings
st.set_page_config(
    page_title="Premier League Tracker",
    layout="wide"
)


# Find data folder
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR 


# Website colours
st.markdown("""
<style>

.stApp {
    background-color: #FFFFFF;
    color: #1F2937;
}

[data-testid="stSidebar"] {
    background-color: #142B4A;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

h1, h2, h3 {
    color: #142B4A;
}

p, label {
    color: #1F2937;
}

[data-testid="stMetric"] {
    background-color: #EFF4FA;
    padding: 15px;
    border-radius: 8px;
}

[data-testid="stMetricLabel"] {
    color: #142B4A;
}

[data-testid="stMetricValue"] {
    color: #2563EB;
}

</style>
""", unsafe_allow_html=True)


# Clean column names
def clean_column_name(column):

    special_names = {
        "playerId": "Player ID",
        "playerName": "Player Name",
        "team_name": "Team Name",
        "team_id": "Team ID",

        "duelsLost": "Duels Lost",
        "expectedAssists": "Expected Assists",
        "fiftyFifty": "50/50 Challenges",
        "totalRedCards": "Total Red Cards",
        "totalTackles": "Total Tackles",
        "savesMadeFromOutsideBox": "Saves From Outside Box",
        "unsuccessfulShortPasses": "Unsuccessful Short Passes",
        "gamesPlayed": "Games Played",
        "successfulFiftyFifty": "Successful 50/50 Challenges",
        "totalUnsuccessfulPassesExclCrossesAndCorners": "Unsuccessful Passes Excluding Crosses and Corners",
        "totalPasses": "Total Passes",
        "goalKicks": "Goal Kicks",
        "savesMadeCaught": "Saves Caught",
        "aerialDuels": "Aerial Duels",
        "cleanSheets": "Clean Sheets",
        "penaltiesFaced": "Penalties Faced",
        "timePlayed": "Time Played",
        "aerialDuelsLost": "Aerial Duels Lost",
        "duelsWon": "Duels Won",
        "goalsConcededOutsideBox": "Goals Conceded Outside Box",
        "putthroughBlockedDistribution": "Blocked Distribution",
        "groundDuelsWon": "Ground Duels Won",
        "successfulShortPasses": "Successful Short Passes",
        "penaltyGoalsConceded": "Penalty Goals Conceded",
        "expectedGoalsOnTargetConceded": "Expected Goals on Target Conceded",
        "successfulLaunches": "Successful Launches",
        "totalClearances": "Total Clearances",
        "goalsConceded": "Goals Conceded",
        "groundDuelsLost": "Ground Duels Lost",
        "rightsidePasses": "Right-Sided Passes",
        "savesMade": "Saves Made",
        "totalFoulsWon": "Total Fouls Won",
        "winningGoal": "Winning Goals",
        "goalkeeperSmother": "Goalkeeper Smothers",
        "forwardPasses": "Forward Passes",
        "crossesNotClaimed": "Crosses Not Claimed",
        "tacklesLost": "Tackles Lost",
        "successfulPassesOppositionHalf": "Successful Passes in Opposition Half",
        "goalsConcededInsideBox": "Goals Conceded Inside Box",
        "groundDuels": "Ground Duels",
        "aerialDuelsWon": "Aerial Duels Won",
        "straightRedCards": "Straight Red Cards",
        "gkSuccessfulDistribution": "Successful Goalkeeper Distribution",
        "openPlayPasses": "Open Play Passes",
        "cornersWon": "Corners Won",
        "totalLossesOfPossession": "Total Losses of Possession",
        "tacklesWon": "Tackles Won",
        "successfulDribbles": "Successful Dribbles",
        "gkUnsuccessfulDistribution": "Unsuccessful Goalkeeper Distribution",
        "savesMadeParried": "Saves Parried",
        "leftsidePasses": "Left-Sided Passes",
        "successfulLongPasses": "Successful Long Passes",
        "totalTouchesInOppositionBox": "Touches in Opposition Box",
        "throwInsToOwnPlayer": "Throw-Ins to Own Player",
        "unsuccessfulLaunches": "Unsuccessful Launches",
        "successfulPassesOwnHalf": "Successful Passes in Own Half",
        "savesMadeFromInsideBox": "Saves From Inside Box",
        "unsuccessfulLongPasses": "Unsuccessful Long Passes",
        "unsuccessfulPassesOwnHalf": "Unsuccessful Passes in Own Half",
        "successfulCrossesOpenPlay": "Successful Open Play Crosses",
        "blockedShots": "Blocked Shots",
        "totalShots": "Total Shots",
        "throughBalls": "Through Balls",
        "unsuccessfulCrossesOpenPlay": "Unsuccessful Open Play Crosses",
        "successfulCrossesAndCorners": "Successful Crosses and Corners",
        "keyPassesAttemptAssists": "Key Passes and Attempted Assists",
        "unsuccessfulDribbles": "Unsuccessful Dribbles",
        "unsuccessfulCrossesAndCorners": "Unsuccessful Crosses and Corners",
        "timesTackled": "Times Tackled",
        "shotsOffTargetIncWoodwork": "Shots Off Target Including Woodwork",
        "totalFoulsConceded": "Total Fouls Conceded",
        "shotsBlockedOutsideBox": "Shots Blocked Outside Box",
        "foulAttemptedTackle": "Fouls From Attempted Tackles",
        "expectedGoals": "Expected Goals",
        "shotsOnTargetIncGoals": "Shots on Target Including Goals",
        "expectedGoalsOnTarget": "Expected Goals on Target",
        "successfulLayoffs": "Successful Layoffs",
        "shotsOnTargetOutsideBox": "Shots on Target Outside Box",
        "shotsOnTargetInBox": "Shots on Target Inside Box",
        "blocks": "Blocks",
        "shotsBlockedInBox": "Shots Blocked Inside Box",
        "rightFootGoals": "Right-Footed Goals",
        "freekickTotal": "Total Free Kicks",
        "attemptsFromSetPieces": "Attempts From Set Pieces",
        "expectedGoalsFreekick": "Expected Goals From Free Kicks",
        "foulWonPenalty": "Penalties Won",
        "unsuccessfulLayoffs": "Unsuccessful Layoffs",
        "penaltiesTaken": "Penalties Taken",
        "penaltiesConceded": "Penalties Conceded",
        "throwInsToOppositionPlayer": "Throw-Ins to Opposition Player",
        "ownGoalScored": "Own Goals Scored",
        "lastPlayerTackle": "Last Player Tackles",
        "secondGoalAssists": "Second Goal Assists",
        "successfulCornersIntoBox": "Successful Corners Into Box",
        "leftFootGoals": "Left-Footed Goals",
        "unsuccessfulCornersIntoBox": "Unsuccessful Corners Into Box",
        "hitWoodwork": "Shots That Hit Woodwork",
        "handballsConceded": "Handballs Conceded",
        "cornersTakenInclShortCorners": "Corners Taken Including Short Corners",
        "headedGoals": "Headed Goals",
        "redCards2ndYellow": "Red Cards From Second Yellow",
        "setPiecesGoals": "Goals From Set Pieces",
        "otherGoals": "Other Goals",
        "penaltiesSaved": "Penalties Saved",
        "savesFromPenalty": "Saves From Penalties",
        "clearancesOffTheLine": "Clearances Off the Line",

        "homeGoals": "Home Goals",
        "awayGoals": "Away Goals"
    }

    if column in special_names:
        return special_names[column]

    return str(column).replace("_", " ").title()


# Function to display tables
def show_table(data):

    column_settings = {
        column: st.column_config.Column(
            label=clean_column_name(column)
        )
        for column in data.columns
    }

    st.dataframe(
        data,
        hide_index=True,
        column_config=column_settings
    )


# Load data
matches = pd.read_csv(
    DATA_DIR / "matches_2021-22_to_2025-26.csv"
)

players = pd.read_csv(
    DATA_DIR / "player_season_stats.csv"
)

tables = pd.read_csv(
    DATA_DIR / "calculated_league_tables.csv"
)


# Sidebar
st.sidebar.title("Premier League")

page = st.sidebar.radio(
    "Choose Page",
    [
        "Home",
        "Players",
        "Matches",
        "League Table",
        "Rankings",
        "Analytics"
    ]
)

season = st.sidebar.selectbox(
    "Choose Season",
    ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
)


# Select season data
season_matches = matches[matches["Season"] == season]
season_players = players[players["season"] == season]
season_table = tables[tables["Season"] == season]


# HOME PAGE
if page == "Home":

    st.title("Premier League Tracker")
    st.write("Football statistics from five Premier League seasons.")

    total_goals = (
        season_matches["FTHG"].sum()
        + season_matches["FTAG"].sum()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Matches", len(season_matches))
    col2.metric("Total Goals", int(total_goals))

    average_goals = (
        round(total_goals / len(season_matches), 2)
        if len(season_matches) > 0 else 0
    )

    col3.metric("Average Goals", average_goals)

    st.subheader("League Table")

    show_table(
        season_table.sort_values("Position")
    )

    st.subheader("Top Goal Scorers")

    top_scorers = season_players.sort_values(
        "goals", ascending=False
    ).head(5)

    show_table(
        top_scorers[["playerName", "team_name", "goals"]]
    )

    st.subheader("Recent Matches")

    recent_matches = season_matches.tail(5)

    show_table(
        recent_matches[
            ["Date", "HomeTeam", "FTHG", "FTAG", "AwayTeam"]
        ]
    )


# PLAYERS PAGE
elif page == "Players":

    st.title("Player Centre")

    available_players = sorted(
        season_players["playerName"].dropna().unique()
    )

    if available_players:

        name = st.selectbox("Choose Player", available_players)

        player = season_players[
            season_players["playerName"] == name
        ]

        st.subheader(name)

        st.write(
            "Club:",
            ", ".join(player["team_name"].dropna().unique())
        )

        st.write("Position:", player.iloc[0]["position"])
        st.write("Season:", season)

        st.subheader("Main Statistics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Goals", int(player["goals"].sum()))
        col2.metric("Assists", int(player["goalAssists"].sum()))
        col3.metric("Appearances", int(player["appearances"].sum()))
        col4.metric("Clean Sheets", int(player["cleanSheets"].sum()))

        st.subheader("Attacking Statistics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Expected Goals",
            round(player["expectedGoals"].sum(), 2)
        )

        col2.metric(
            "Expected Assists",
            round(player["expectedAssists"].sum(), 2)
        )

        col3.metric("Total Shots", int(player["totalShots"].sum()))

        col4.metric(
            "Shots on Target",
            int(player["shotsOnTargetIncGoals"].sum())
        )

        st.subheader("Discipline")

        col1, col2 = st.columns(2)

        col1.metric("Yellow Cards", int(player["yellowCards"].sum()))
        col2.metric("Red Cards", int(player["totalRedCards"].sum()))

        st.subheader("Full Statistics")

        show_table(player)

    else:

        st.warning("No player statistics available for this season.")


# MATCHES PAGE
elif page == "Matches":

    st.title("Match Centre")

    st.write("All Premier League matches for", season)

    show_table(
        season_matches[
            ["Date", "HomeTeam", "FTHG", "FTAG", "AwayTeam"]
        ]
    )

    st.subheader("Match Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Home Goals", int(season_matches["FTHG"].sum()))
    col2.metric("Away Goals", int(season_matches["FTAG"].sum()))
    col3.metric("Total Matches", len(season_matches))


# LEAGUE TABLE PAGE
elif page == "League Table":

    st.title("Premier League Table")

    st.write("Final league standings for", season)

    show_table(
        season_table.sort_values("Position")
    )

    st.subheader("Points Comparison")

    team_points = season_table.set_index("Team")

    st.bar_chart(team_points["Points"])


# RANKINGS PAGE
elif page == "Rankings":

    st.title("Player Rankings")

    st.write("Top performing players in", season)

    st.subheader("Top Goal Scorers")

    top_scorers = season_players.sort_values(
        "goals", ascending=False
    ).head(10)

    show_table(
        top_scorers[["playerName", "team_name", "goals"]]
    )

    st.subheader("Top Assists")

    top_assists = season_players.sort_values(
        "goalAssists", ascending=False
    ).head(10)

    show_table(
        top_assists[["playerName", "team_name", "goalAssists"]]
    )

    st.subheader("Most Appearances")

    top_appearances = season_players.sort_values(
        "appearances", ascending=False
    ).head(10)

    show_table(
        top_appearances[["playerName", "team_name", "appearances"]]
    )

    st.subheader("Most Clean Sheets")

    top_clean_sheets = season_players.sort_values(
        "cleanSheets", ascending=False
    ).head(10)

    show_table(
        top_clean_sheets[["playerName", "team_name", "cleanSheets"]]
    )


# ANALYTICS PAGE
elif page == "Analytics":

    st.title("Premier League Analytics")

    st.write("Explore team and scoring statistics for", season)

    # Goal statistics
    home_goals = season_matches["FTHG"].sum()
    away_goals = season_matches["FTAG"].sum()
    total_goals = home_goals + away_goals

    st.subheader("Goal Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Goals", int(total_goals))
    col2.metric("Home Goals", int(home_goals))
    col3.metric("Away Goals", int(away_goals))

    average_goals = (
        round(total_goals / len(season_matches), 2)
        if len(season_matches) > 0 else 0
    )

    st.metric("Average Goals Per Match", average_goals)

    # Home and away goals chart
    st.subheader("Home Goals vs Away Goals")

    goal_data = pd.DataFrame({
        "Goals": [home_goals, away_goals]
    }, index=["Home Goals", "Away Goals"])

    st.bar_chart(goal_data)

    # Team performance
    st.subheader("Team Goals")

    team_goals = season_table.set_index("Team")[["GF", "GA"]]

    st.bar_chart(team_goals)

    # Points comparison
    st.subheader("Team Points")

    team_points = season_table.set_index("Team")[["Points"]]

    st.bar_chart(team_points)

    # League performance
    st.subheader("League Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Teams", len(season_table))
    col2.metric("Highest Points", int(season_table["Points"].max()))
    col3.metric("Most Goals Scored", int(season_table["GF"].max()))
