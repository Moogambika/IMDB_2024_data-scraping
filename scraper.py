import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# Create data folder if not exists
os.makedirs("data", exist_ok=True)

# Setup Chrome WebDriver
driver = webdriver.Chrome()

# Genres to scrape
genres_list = ["action", "comedy", "thriller", "romance", "horror"]

# Movies per genre
movies_per_genre = 1000
movies_per_page = 50
pages_per_genre = (movies_per_genre + movies_per_page - 1) // movies_per_page  # ceil division

for genre in genres_list:
    titles, ratings, votes, durations, genres_col = [], [], [], [], []

    for page in range(pages_per_genre):
        start = page * movies_per_page + 1
        url = f"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres={genre}&start={start}"
        driver.get(url)
        time.sleep(3)

        # Find movies on page
        movie_items = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

        for movie in movie_items:
            if len(titles) >= movies_per_genre:
                break

            # Title
            try:
                title = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
            except:
                title = "N/A"

            # Genre (chip text, fallback is the page genre)
            try:
                genre_text = movie.find_element(By.CSS_SELECTOR, "span.ipc-chip__text").text
            except:
                genre_text = genre.capitalize()

            # Rating
            try:
                rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text
            except:
                rating = "N/A"

            # Votes
            try:
                vote = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text
            except:
                vote = "0"

            # Duration
            try:
                duration = movie.find_element(By.XPATH, './/span[contains(text(),"h") or contains(text(),"m")]').text
            except:
                duration = "N/A"

            titles.append(title)
            genres_col.append(genre_text)
            ratings.append(rating)
            votes.append(vote)
            durations.append(duration)

        print(f"Scraped page {page+1} for {genre} movies...")

    # Save each genre dataset
    df = pd.DataFrame({
        "Movie Name": titles,
        "Genre": genres_col,
        "Rating": ratings,
        "Votes": votes,
        "Duration": durations
    })
    df.to_csv(f"data/{genre.capitalize()}.csv", index=False)
    print(f"Saved {genre.capitalize()}.csv with {len(df)} movies")

driver.quit()
