import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, FLOAT, INTEGER

# 1. Load your scraped CSV
df = pd.read_csv("data/all_movies.csv")

# 2. Remove duplicates by title
df = df.drop_duplicates(subset=["title"], keep="first")

# 3. TiDB Cloud connection details
host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
port = 4000
user = "sJS9A4ifsRxCyhp.root"
password = "BZOhl53om6ZM6iOO"
database = "imdb2024"

# 4. Create SQLAlchemy connection string
engine = create_engine(
    f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
)

# 5. Save DataFrame into SQL (replace table if exists)
df.to_sql(
    "movies",      # table name
    engine,
    if_exists="replace",   # replace old table
    index=False,
    dtype={
        "title": VARCHAR(255),
        "genre": VARCHAR(50),
        "rating": FLOAT,
        "votes": INTEGER,
        "duration_min": INTEGER
    }
)

print(f"Uploaded {len(df)} movies successfully to TiDB Cloud!")
