🎬 IMDb 2024 Movies Analysis
📌 Problem Statement

IMDb releases thousands of movies every year across multiple genres.
This project focuses on scraping IMDb 2024 movies, cleaning and transforming the dataset, storing it in TiDB Cloud (SQL database), performing Exploratory Data Analysis (EDA), and building an interactive Streamlit dashboard to answer key business questions.

🚀 Project Workflow

Data Collection (Web Scraping)

Used Selenium to scrape 2024 movies across genres: Action, Comedy, Thriller, Romance, Horror.

Saved each genre dataset into CSV (/data folder).

Data Cleaning (Pandas)

Standardized column names → title, genre, rating, votes, duration.

Converted duration into minutes & hours.

Removed numbering prefixes (e.g., 1. Dune → Dune).

Exploratory Data Analysis (EDA)

Conducted in eda.ipynb.

Steps included:

df.info() and df.describe()

Missing values check

Visualizations (Genre distribution, Rating histograms, Vote patterns)

Observations: Genres like Action & Comedy dominate; most ratings fall between 6–8.

Database Integration (TiDB Cloud)

Created database: imdb2024.

Uploaded cleaned data into table movies using SQLAlchemy.

Verified with queries:

SELECT * FROM movies LIMIT 10;
SELECT title, rating FROM movies WHERE rating < 5;
SELECT genre, AVG(rating) FROM movies GROUP BY genre;


Interactive Dashboard (Streamlit)

Built streamlit_app.py with 5 pages:

Overview → Summary metrics (Total movies, Avg rating, Avg votes).

Questions → Displays 10 key business questions.

Analysis → Visualizations for each question.

Filters → Interactive filtering (ratings, votes, genre, duration).

Data Preview → View first 50 records.

📊 Business Use Cases (Answered in Dashboard)

Top 10 Movies by Ratings & Votes

Genre Distribution

Average Duration by Genre

Voting Trends by Genre

Rating Distribution

Top-Rated Movie per Genre

Most Popular Genres by Total Votes

Duration Extremes (Shortest & Longest movies)

Ratings by Genre (Heatmap)

Ratings vs Votes (Correlation analysis)

📂 Project Structure
📦 imdb-2024-analysis
 ┣ 📂 data/                # Scraped CSVs (Action.csv, Comedy.csv, etc.)
 ┣ 📂 analysis/            # Analysis scripts & plots
 ┣ 📜 scraper.py           # Selenium web scraper
 ┣ 📜 save_to_sql.py       # Upload CSVs to TiDB Cloud
 ┣ 📜 sql.ipynb            # SQL queries demo
 ┣ 📜 eda.ipynb            # Exploratory Data Analysis
 ┣ 📜 streamlit_app.py     # Streamlit dashboard
 ┣ 📜 README.md            # Project documentation

🛠️ Tech Stack

Python (Selenium, Pandas, SQLAlchemy, Streamlit, Plotly, Matplotlib, Seaborn)

Database → TiDB Cloud (MySQL compatible)

Visualization → Plotly, Streamlit

Version Control → GitHub

📌 Insights & Observations

Action and Comedy are the most frequent genres in 2024.

Average ratings mostly lie between 6.5 – 7.5.

Some movies have exceptionally high votes but average ratings → showing hype vs quality.

Romance & Thriller genres show longer average durations compared to Comedy.

🚀 How to Run

Clone the repository:

git clone https://github.com/<your-username>/imdb-2024-analysis.git
cd imdb-2024-analysis


Install dependencies:

pip install -r requirements.txt


Run Streamlit app:

streamlit run streamlit_app.py

🏆 Credits

Project by: Moogambika Govindaraj

Data Source: IMDb 2024

Cloud Database: TiDB Cloud
