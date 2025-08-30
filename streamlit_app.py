import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.graph_objects as go
import pymysql

# ------------------------
# DATABASE CONNECTION (with SSL)
# ------------------------
HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
PORT = 4000
USER = "sJS9A4ifsRxCyhp.root"
PASSWORD = "BZOhl53om6ZM6iOO"
DB = "imdb2024"

ssl_args = {"ssl": {"ssl-mode": "REQUIRED"}}

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}",
    connect_args=ssl_args
)

# ------------------------
# LOAD DATA
# ------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM movies"
    df = pd.read_sql(query, engine)
    return df

df = load_data()

# ------------------------
# STREAMLIT APP LAYOUT
# ------------------------
st.set_page_config(page_title="IMDB 2024 Movies Dashboard", layout="wide")

pages = ["Overview", "Questions", "Analysis", "Filters", "Data Preview"]
page = st.sidebar.radio("Navigate", pages)

# ------------------------
# PAGE 1: OVERVIEW
# ------------------------
if page == "Overview":
    st.title("🎬 IMDB 2024 Movies Dashboard")
    st.write("Welcome! This dashboard provides insights into IMDB 2024 movies dataset hosted on TiDB Cloud.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Movies", df.shape[0])
    col2.metric("Average Rating", round(df['rating'].mean(), 2))
    col3.metric("Average Votes", round(df['votes'].mean(), 0))

# ------------------------
# PAGE 2: QUESTIONS
# ------------------------
elif page == "Questions":
    st.title("❓ Key Questions")
    st.markdown("""
    1. Top 10 Movies by Rating and Voting Counts  
    2. Genre Distribution  
    3. Average Duration by Genre  
    4. Voting Trends by Genre  
    5. Rating Distribution  
    6. Genre-Based Rating Leaders  
    7. Most Popular Genres by Voting  
    8. Duration Extremes  
    9. Ratings by Genre (Heatmap)  
    10. Correlation between Ratings and Voting Counts
    """)

# -----------------------------
# PAGE 3: ANALYSIS
# -----------------------------
elif page == "Analysis":
    st.title("IMDb 2024 – Analysis & Visualizations")

    # 1) Top 10 Movies by Rating & Votes
    st.header("1) Top 10 Movies by Rating & Voting Counts")
    top_rating = df.sort_values(["rating", "votes"], ascending=[False, False]).head(10)
    st.dataframe(top_rating[["title", "genre", "rating", "votes", "duration_min"]], use_container_width=True)

    # 2) Genre Distribution
    st.header("2) Genre Distribution")
    genre_count = df.groupby("genre_primary")["title"].count().reset_index(name="count").sort_values("count", ascending=False)
    fig2 = px.bar(genre_count, x="genre_primary", y="count", color="count", title="Number of Movies per Genre", text="count")
    st.plotly_chart(fig2, use_container_width=True)

    # 3) Average Duration by Genre
    st.header("3) Average Duration by Genre")
    duration_by_genre = (
        df.groupby("genre_primary")["duration_min"]
        .mean()
        .reset_index()
        .sort_values("duration_min", ascending=False)
    )
    fig3 = px.bar(
        duration_by_genre,
        x="duration_min",
        y="genre_primary",
        orientation="h",
        title="Average Movie Duration per Genre",
        color_discrete_sequence=["#9c254d"]
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 4) Voting Trends by Genre
    st.header("4) Voting Trends by Genre")
    votes_by_genre = (
    df.groupby("genre_primary")["votes"]
    .mean()
    .reset_index()
    .sort_values("votes", ascending=False)
     )

    fig4 = px.bar(
    votes_by_genre,
    x="genre_primary",
    y="votes",
    title="Average Votes by Genre",
    color_discrete_sequence=["#a48d91"]  # custom color applied
    )

    st.plotly_chart(fig4, use_container_width=True)


    # 5) Rating Distribution
    st.header("5) Rating Distribution")
    fig5 = px.histogram(df, x="rating", nbins=20, color_discrete_sequence=["purple"], title="Distribution of Ratings")
    st.plotly_chart(fig5, use_container_width=True)

    # 6) Genre-Based Rating Leaders
    st.header("6) Top-Rated Movie per Genre")
    rating_leaders = df.loc[df.groupby("genre_primary")["rating"].idxmax()][["genre_primary", "title", "rating", "votes"]].sort_values("rating", ascending=False)
    st.dataframe(rating_leaders, use_container_width=True)

    # 7) Most Popular Genres by Voting
    st.header("7) Most Popular Genres by Voting")
    votes_genre_total = df.groupby("genre_primary")["votes"].sum().reset_index()
    fig7 = px.pie(votes_genre_total, names="genre_primary", values="votes", title="Total Votes per Genre")
    st.plotly_chart(fig7, use_container_width=True)

    # 8) Duration Extremes
    st.header("8) Duration Extremes")

    shortest = (
        df.sort_values("duration_min", ascending=True)
          .head(5)[["title", "genre", "duration_min", "rating"]]
          .reset_index(drop=True)
    )

    longest = (
        df.sort_values("duration_min", ascending=False)
          .head(5)[["title", "genre", "duration_min", "rating"]]
          .reset_index(drop=True)
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🎬 Shortest Movies")
        st.dataframe(shortest, use_container_width=True)

    with c2:
        st.subheader("🎬 Longest Movies")
        longest_display = longest.rename(columns={"duration_min": "duration_max"})
        st.dataframe(longest_display, use_container_width=True)

    # 9) Ratings by Genre Heatmap
    st.header("9) Ratings by Genre Heatmap")
    heatmap_data = df.pivot_table(index="genre_primary", values="rating", aggfunc="mean")
    fig9 = px.imshow(
        heatmap_data,
        text_auto=True,
        color_continuous_scale=[
            [0, "#f5f5dc"],
            [0.5, "#d2b48c"],
            [1, "#8b5e3c"]
        ],
        aspect="auto",
        title="Average Ratings per Genre"
    )
    fig9.update_layout(
        plot_bgcolor="beige",
        paper_bgcolor="beige",
        font=dict(color="black"),
        width=800,
        height=500
    )
    st.plotly_chart(fig9, use_container_width=True)

    # 10) Correlation Analysis
    st.header("10) Ratings vs Votes")
    fig10 = px.scatter(
        df,
        x="rating",
        y="votes",
        color="genre_primary",
        hover_data=["title"],
        title="Ratings vs Votes"
    )
    st.plotly_chart(fig10, use_container_width=True)

# ------------------------
# PAGE 4: FILTERS
# ------------------------
elif page == "Filters":
    st.title("🔍 Filters")
    st.markdown("Apply filters to refine the dataset.")

    col1, col2 = st.columns(2)
    with col1:
        min_rating = st.slider("Minimum Rating", 0.0, 10.0, 0.0)
        max_rating = st.slider("Maximum Rating", 0.0, 10.0, 10.0)
    with col2:
        min_votes = st.number_input("Minimum Votes", 0, int(df["votes"].max()), 0)
        max_votes = st.number_input("Maximum Votes", 0, int(df["votes"].max()), int(df["votes"].max()))

    filtered_df = df[
        (df["rating"] >= min_rating) & (df["rating"] <= max_rating) &
        (df["votes"] >= min_votes) & (df["votes"] <= max_votes)
    ]

    st.write("Filtered Movies:", filtered_df.shape[0])
    st.dataframe(filtered_df, use_container_width=True)

# ------------------------
# PAGE 5: DATA PREVIEW
# ------------------------
elif page == "Data Preview":
    st.title("📑 Data Preview")
    st.dataframe(df.head(50), use_container_width=True)
