# merge_clean_with_duplicates_info.py
import os
import pandas as pd

DATA_DIR = "data"
GENRES = ["Action", "Comedy", "Thriller", "Romance", "Horror"]

# Load all genre CSVs
frames = []
for g in GENRES:
    path = os.path.join(DATA_DIR, f"{g}.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        if "Genre" not in df.columns:
            df["Genre"] = g
        frames.append(df)
    else:
        print(f"⚠️ Missing file: {path}")

if not frames:
    raise SystemExit("No genre files found. Run the scraper first.")

# Merge all data
df = pd.concat(frames, ignore_index=True)

# Standardize column names
df = df.rename(columns={"Movie Name": "title", "Duration": "duration_raw", "Genre": "genre"})

# Fill missing values for safety
df["title"] = df["title"].fillna("N/A")
df["genre"] = df["genre"].fillna("N/A").astype(str)

# Count duplicates
total_rows_before = len(df)
duplicates_count = df.duplicated(subset=["title"]).sum()
print(f"Total movies before removing duplicates: {total_rows_before}")
print(f"Number of duplicate titles found: {duplicates_count}")

# Remove duplicates based on title only
df = df.drop_duplicates(subset=["title"], keep="first")
total_rows_after = len(df)
print(f"Total movies after removing duplicates: {total_rows_after}")

# Save merged dataset
out_path = os.path.join(DATA_DIR, "all_movies.csv")
df.to_csv(out_path, index=False)
print(f"Saved cleaned dataset to {out_path}")
