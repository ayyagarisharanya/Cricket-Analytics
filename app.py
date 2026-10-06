
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="🏏 Cricket Analytics ",
    page_icon="🏏",
    layout="wide"
)
# ---------------- Load Data ----------------
@st.cache_data
def load_data():

    data = {
        "season": [
            "2020","2020","2020","2020","2020",
            "2021","2021","2021","2021","2021",
            "2022","2022","2022","2022","2022",
            "2023","2023","2023","2023","2023",
            "2024","2024","2024","2024","2024"
        ],

        "player": [
            "Virat Kohli","Rohit Sharma","Jasprit Bumrah","MS Dhoni","Hardik Pandya",
            "Virat Kohli","Rohit Sharma","Bhuvneshwar Kumar","Rishabh Pant","Shikhar Dhawan",
            "KL Rahul","Andre Russell","Jos Buttler","Yuzvendra Chahal","David Warner",
            "Shubman Gill","Suryakumar Yadav","Ravindra Jadeja","Trent Boult","Kane Williamson",
            "Virat Kohli","Rohit Sharma","Jasprit Bumrah","KL Rahul","Andre Russell"
        ],

        "team": [
            "RCB","MI","MI","CSK","MI",
            "RCB","MI","SRH","DC","DC",
            "LSG","KKR","RR","RR","DC",
            "GT","MI","CSK","RR","SRH",
            "RCB","MI","MI","LSG","KKR"
        ],

        "runs": [
            466,332,10,200,281,
            405,381,15,419,587,
            616,335,863,50,432,
            890,605,250,120,320,
            639,410,5,520,300
        ],

        "wickets": [
            0,0,27,0,10,
            0,0,18,0,0,
            0,11,0,27,0,
            0,0,20,25,5,
            0,0,22,0,15
        ]
    }

    return pd.DataFrame(data)

df = load_data()

# ---------------- Helper ----------------
def filter_by_season(data, season):
    if season == "All Seasons":
        return data
    return data[data["season"] == season]

# ---------------- Core Functions ----------------
def top_batsmen(season):
    data = filter_by_season(df, season)
    return data.groupby("player")["runs"].sum().reset_index().sort_values(by="runs", ascending=False)

def top_bowlers(season):
    data = filter_by_season(df, season)
    return data.groupby("player")["wickets"].sum().reset_index().sort_values(by="wickets", ascending=False)

def compare_players(p1, p2, season):
    data = filter_by_season(df, season)
    return data[data["player"].str.lower().isin([p1.lower(), p2.lower()])]

def team_stats(team, season):
    data = filter_by_season(df, season)
    return data[data["team"].str.lower() == team.lower()].groupby("player")[["runs","wickets"]].sum().reset_index()

# ---------------- Player Dashboard ----------------
def player_dashboard(player, season):
    data = filter_by_season(df, season)
    player_data = data[data["player"].str.lower() == player.lower()]

    if player_data.empty:
        st.error("❌ Player not found")
        return

    st.subheader(f"🏏 {player.title()} Dashboard")

    # Metrics
    total_runs = player_data["runs"].sum()
    total_wickets = player_data["wickets"].sum()
    matches = len(player_data)

    col1, col2, col3 = st.columns(3)
    col1.metric("🏃 Runs", total_runs)
    col2.metric("🎯 Wickets", total_wickets)
    col3.metric("📅 Matches", matches)

    # Graphs
    st.markdown("### 📊 Performance Trends")

    runs_chart = player_data.groupby("season")["runs"].sum()
    wickets_chart = player_data.groupby("season")["wickets"].sum()

    # Runs Line Chart
    fig1, ax1 = plt.subplots()
    ax1.plot(runs_chart.index, runs_chart.values, marker='o')
    ax1.set_title("Runs Over Seasons")
    ax1.set_xlabel("Season")
    ax1.set_ylabel("Runs")
    st.pyplot(fig1)

    # Wickets Bar Chart
    fig2, ax2 = plt.subplots()
    ax2.bar(wickets_chart.index, wickets_chart.values)
    ax2.set_title("Wickets Over Seasons")
    ax2.set_xlabel("Season")
    ax2.set_ylabel("Wickets")
    st.pyplot(fig2)

    # Table
    st.markdown("### 📋 Detailed Stats")
    st.dataframe(player_data)

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Settings")

season_options = ["All Seasons"] + sorted(df["season"].unique().tolist())
season = st.sidebar.selectbox("📅 Select Season", season_options)

# ---------------- Header ----------------
st.title("🏏 Cricket Analytics ")
st.write("Ask anything about cricket stats!")

st.info("""
Try:
- top batsman
- top bowler
- player Rohit Sharma
- compare virat kohli and rohit sharma
- team mi
""")

# ---------------- Input ----------------
query = st.text_input("💬 Enter your query:")

# ---------------- Logic ----------------
if query:
    query = query.lower().strip()

    # Top Batsman
    if "batsman" in query or "runs" in query:
        result = top_batsmen(season)
        st.subheader("🏆 Top Batsmen")
        st.dataframe(result.head(5))
        st.bar_chart(result.head(5).set_index("player"))

    # Top Bowler
    elif "bowler" in query or "wickets" in query:
        result = top_bowlers(season)
        st.subheader("🎯 Top Bowlers")
        st.dataframe(result.head(5))
        st.bar_chart(result.head(5).set_index("player"))

    # Player Dashboard
    elif "player" in query:
        try:
            player = query.split("player")[1].strip()
            player_dashboard(player, season)
        except:
            st.error("Try: player virat kohli")

    # Compare Players
    elif "compare" in query:
        try:
            parts = query.split("compare")[1].split("and")
            p1, p2 = parts[0].strip(), parts[1].strip()

            result = compare_players(p1, p2, season)
            st.subheader("⚔️ Player Comparison")
            st.dataframe(result)

        except:
            st.error("Use: compare player1 and player2")

    # Team Stats
    elif "team" in query:
        try:
            team = query.split("team")[1].strip()
            result = team_stats(team, season)

            st.subheader(f"🏏 {team.upper()} Team Stats")
            st.dataframe(result)

        except:
            st.error("Try: team mi")

    else:
        st.warning("🤖 Try something like 'top batsman' or 'player virat kohli'")

# ---------------- Footer ----------------
st.markdown("---")
st.caption("🏏 Cricket Analytics  • All-in-One Dashboard")