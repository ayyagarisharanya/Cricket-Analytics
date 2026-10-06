import streamlit as st
import pandas as pd

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Cricket Analytics",
    page_icon="🏏",
    layout="wide"
)

# ---------------- Create Sample Data ----------------
@st.cache_data
def load_data():
    data = {
        "season": ["2020","2020","2020","2021","2021","2021","2022","2022"],
        "player": [
            "Virat Kohli","Rohit Sharma","Jasprit Bumrah",
            "Virat Kohli","Rohit Sharma","Bhuvneshwar Kumar",
            "KL Rahul","Andre Russell"
        ],
        "team": [
            "RCB","MI","MI",
            "RCB","MI","SRH",
            "LSG","KKR"
        ],
        "runs": [466, 332, 10, 405, 381, 15, 616, 335],
        "wickets": [0, 0, 27, 0, 0, 18, 0, 11]
    }
    return pd.DataFrame(data)

df = load_data()

# ---------------- Helper Function ----------------
def filter_by_season(data, season):
    if season == "All Seasons":
        return data
    return data[data["season"] == season]

# ---------------- Functions ----------------
def top_batsmen(season):
    data = filter_by_season(df, season)
    grouped = data.groupby("player")["runs"].sum().reset_index()
    return grouped.sort_values(by="runs", ascending=False).head(5)

def top_bowlers(season):
    data = filter_by_season(df, season)
    grouped = data.groupby("player")["wickets"].sum().reset_index()
    return grouped.sort_values(by="wickets", ascending=False).head(5)

def compare_players(p1, p2, season):
    data = filter_by_season(df, season)
    player1 = data[data["player"].str.lower() == p1.lower()]
    player2 = data[data["player"].str.lower() == p2.lower()]
    return pd.concat([player1, player2])

def team_stats(team, season):
    data = filter_by_season(df, season)
    team_data = data[data["team"].str.lower() == team.lower()]
    grouped = team_data.groupby("player")[["runs", "wickets"]].sum().reset_index()
    return grouped

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Settings")

season_options = ["All Seasons"] + sorted(df["season"].unique().tolist())
season = st.sidebar.selectbox("Select Season", season_options)

# ---------------- Main UI ----------------
st.title("🏏 Cricket Performance Analytics")
st.write("Ask cricket-related questions and get analytics insights instantly!")

st.info(
    "💡 Try:\n"
    "- top batsman\n"
    "- top bowler\n"
    "- compare virat kohli and rohit sharma\n"
    "- team rcb"
)

query = st.text_input("💬 Ask your question:")

# ---------------- Chatbot Logic ----------------
if query:
    query = query.lower().strip()

    if any(word in query for word in ["top batsman", "top scorer", "most runs", "best batsman"]):
        result = top_batsmen(season)
        st.subheader("🏏 Top Batsmen")
        st.dataframe(result)
        if not result.empty:
            st.bar_chart(result.set_index("player"))

    elif any(word in query for word in ["top bowler", "best bowler", "most wickets"]):
        result = top_bowlers(season)
        st.subheader("🎯 Top Bowlers")
        st.dataframe(result)
        if not result.empty:
            st.bar_chart(result.set_index("player"))

    elif "compare" in query:
        try:
            if "and" not in query:
                raise ValueError
            parts = query.split("compare")[1].strip().split("and")
            p1 = parts[0].strip()
            p2 = parts[1].strip()

            result = compare_players(p1, p2, season)
            st.subheader("📊 Player Comparison")
            st.dataframe(result)

        except:
            st.error("Use format: compare player1 and player2")

    elif "team" in query:
        try:
            team = query.split("team")[1].strip()
            result = team_stats(team, season)
            st.subheader(f"🏏 {team.upper()} Team Stats")
            st.dataframe(result)

        except:
            st.error("Try: team mi")

    else:
        st.warning("🤖 I didn't understand. Try different keywords.")

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Cricket Analytics Chatbot • Built with Streamlit & Pandas")