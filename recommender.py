import pickle

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# Load Movie Data
# --------------------------------------------------

with open("models/movies.pkl", "rb") as file:
    movies = pickle.load(file)


# Make sure DataFrame index matches similarity matrix positions
movies = movies.reset_index(drop=True)


# --------------------------------------------------
# Create Movie Vectors
# --------------------------------------------------

cv = CountVectorizer(
    max_features=5000,
    stop_words="english"
)

vectors = cv.fit_transform(
    movies["tags"].fillna("").astype(str)
)


# --------------------------------------------------
# Calculate Similarity
# --------------------------------------------------

similarity = cosine_similarity(vectors)


# --------------------------------------------------
# Recommendation Function
# --------------------------------------------------

def recommend(movie_name, number_of_recommendations=5):
    """
    Recommend movies similar to the selected movie.

    Returns:
        list of dictionaries containing:
        movie_id, title and similarity score.
    """

    movie_name = movie_name.strip().lower()

    matches = movies[
        movies["title"].str.lower() == movie_name
    ]

    if matches.empty:
        return []

    index = matches.index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommendations = []
    seen_titles = set()

    for movie_index, score in distances[1:]:

        title = movies.iloc[movie_index]["title"]

        # Remove duplicate movie titles
        if title in seen_titles:
            continue

        seen_titles.add(title)

        recommendations.append(
            {
                "movie_id": int(movies.iloc[movie_index]["movie_id"]),
                "title": title,
                "score": float(score)
            }
        )

        if len(recommendations) >= number_of_recommendations:
            break

    return recommendations


# --------------------------------------------------
# Local Testing
# --------------------------------------------------

if __name__ == "__main__":

    results = recommend("Batman Returns")

    print("\nRecommended Movies:\n")

    for number, movie in enumerate(results, start=1):

        print(
            f"{number}. "
            f"{movie['title']} "
            f"(ID: {movie['movie_id']}) "
            f"- Similarity: {movie['score']:.3f}"
        )