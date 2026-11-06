import streamlit as st
import pandas as pd


# Page settings
st.set_page_config(page_title="Premier League Tracker", layout="wide")


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


# Make column names easier to read
def clean_column_name(column):
    column = str(column)
    column = column.replace("_", " ")

    special_names = {
        "playerId": "Player ID",
        "playerName": "Player Name",
        "team_id": "Team ID",
        "team_name": "Team Name",
        "FTHG": "Home Goals",
        "FTAG": "Away Goals",
        "GF": "Goals For",
        "GA": "Goals Against",
        "xG": "Expected Goals",
        "xA": "Expected Assists"
    }

    if column in special_names:
        return special_names[column]

    return column.title()


# Display a dataframe with clearer column names
def show_table(data):
    column_settings = {}

    for column in data.columns:
        column_settings[column] = st.column_config.Column(
            clean_column_name(column)
        )

    st.dataframe(
        data,
        hide_index=True,
        column_config=column_settings,
        use_container_width=True
    )


# Load the three CSV files
matches = pd.read_csv("matches_2021-22_to_2025-26.csv")
players = pd.read_csv("player_season_stats.csv")
tables = pd.read_csv("calculated_league_tables.csv")


# Sidebar navigation
st.sidebar.title("Premier League")

page = st.sidebar.radio(
    "Choose Page",
    ["Home", "Players", "Matches", "League Table", "Rankings", "Analytics"]
)

season = st.sidebar.selectbox(
    "Choose Season",
    ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
)


# Filter the data using the selected season
season_matches = matches[matches["Season"] == season]
season_players = players[players["season"] == season]
season_table = tables[tables["Season"] == season]


# HOME PAGE
if page == "Home":
    st.title("Premier League Tracker")
    st.write("Football statistics from five Premier League seasons.")

    total_goals = season_matches["FTHG"].sum() + season_matches["FTAG"].sum()

    average_goals = 0
    if len(season_matches) > 0:
        average_goals = round(total_goals / len(season_matches), 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Matches", len(season_matches))
    col2.metric("Total Goals", int(total_goals))
    col3.metric("Average Goals", average_goals)

    st.subheader("League Table")
    show_table(season_table.sort_values("Position"))

    st.subheader("Top Goal Scorers")
    top_scorers = season_players.sort_values("goals", ascending=False).head(5)
    show_table(top_scorers[["playerName", "team_name", "goals"]])

    st.subheader("Recent Matches")
    recent_matches = season_matches.tail(5)
    show_table(recent_matches[["Date", "HomeTeam", "FTHG", "FTAG", "AwayTeam"]])


# PLAYERS PAGE
elif page == "Players":
    st.title("Player Centre")

    available_players = sorted(season_players["playerName"].dropna().unique())

    if len(available_players) > 0:
        name = st.selectbox("Choose Player", available_players)
        player = season_players[season_players["playerName"] == name]

        st.subheader(name)

        clubs = player["team_name"].dropna().unique()
        st.write("Club:", ", ".join(clubs))
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
        col1.metric("Expected Goals", round(player["expectedGoals"].sum(), 2))
        col2.metric("Expected Assists", round(player["expectedAssists"].sum(), 2))
        col3.metric("Total Shots", int(player["totalShots"].sum()))
        col4.metric("Shots on Target", int(player["shotsOnTargetIncGoals"].sum()))

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

    show_table(season_matches[["Date", "HomeTeam", "FTHG", "FTAG", "AwayTeam"]])

    st.subheader("Match Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Home Goals", int(season_matches["FTHG"].sum()))
    col2.metric("Away Goals", int(season_matches["FTAG"].sum()))
    col3.metric("Total Matches", len(season_matches))


# LEAGUE TABLE PAGE
elif page == "League Table":
    st.title("Premier League Table")
    st.write("Final league standings for", season)

    show_table(season_table.sort_values("Position"))

    st.subheader("Points Comparison")
    team_points = season_table.set_index("Team")
    st.bar_chart(team_points["Points"])


# RANKINGS PAGE
elif page == "Rankings":
    st.title("Player Rankings")
    st.write("Top performing players in", season)

    st.subheader("Top Goal Scorers")
    top_scorers = season_players.sort_values("goals", ascending=False).head(10)
    show_table(top_scorers[["playerName", "team_name", "goals"]])

    st.subheader("Top Assists")
    top_assists = season_players.sort_values("goalAssists", ascending=False).head(10)
    show_table(top_assists[["playerName", "team_name", "goalAssists"]])

    st.subheader("Most Appearances")
    top_appearances = season_players.sort_values("appearances", ascending=False).head(10)
    show_table(top_appearances[["playerName", "team_name", "appearances"]])

    st.subheader("Most Clean Sheets")
    top_clean_sheets = season_players.sort_values("cleanSheets", ascending=False).head(10)
    show_table(top_clean_sheets[["playerName", "team_name", "cleanSheets"]])


# ANALYTICS PAGE
elif page == "Analytics":
    st.title("Premier League Analytics")
    st.write("Explore team and scoring statistics for", season)

    home_goals = season_matches["FTHG"].sum()
    away_goals = season_matches["FTAG"].sum()
    total_goals = home_goals + away_goals

    st.subheader("Goal Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Goals", int(total_goals))
    col2.metric("Home Goals", int(home_goals))
    col3.metric("Away Goals", int(away_goals))

    average_goals = 0
    if len(season_matches) > 0:
        average_goals = round(total_goals / len(season_matches), 2)
    st.metric("Average Goals Per Match", average_goals)

    st.subheader("Home Goals vs Away Goals")
    goal_data = pd.DataFrame(
        {"Goals": [home_goals, away_goals]},
        index=["Home Goals", "Away Goals"]
    )
    st.bar_chart(goal_data)

    st.subheader("Team Goals")
    team_goals = season_table.set_index("Team")[["GF", "GA"]]
    st.bar_chart(team_goals)

    st.subheader("Team Points")
    team_points = season_table.set_index("Team")[["Points"]]
    st.bar_chart(team_points)

    st.subheader("League Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Teams", len(season_table))
    col2.metric("Highest Points", int(season_table["Points"].max()))
    col3.metric("Most Goals Scored", int(season_table["GF"].max()))
