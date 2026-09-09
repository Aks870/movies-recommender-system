import pickle
import ast
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors


# --------------------------------------------------
# Load Recommendation Model
# --------------------------------------------------

with open("models/movies.pkl", "rb") as file:
    movies = pickle.load(file)

movies = movies.reset_index(drop=True)


# --------------------------------------------------
# Load Original Movie Dataset
# --------------------------------------------------

movies_data = pd.read_csv("data/tmdb_5000_movies.csv")
credits_data = pd.read_csv("data/tmdb_5000_credits.csv")


# Merge movie and credits data
movie_details = movies_data.merge(
    credits_data,
    on="title"
)


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def get_names(text):
    try:
        return [item["name"] for item in ast.literal_eval(text)]
    except (ValueError, SyntaxError, TypeError):
        return []


def get_cast(text):
    try:
        cast = ast.literal_eval(text)
        return [item["name"] for item in cast[:5]]
    except (ValueError, SyntaxError, TypeError):
        return []


def get_director(text):
    try:
        crew = ast.literal_eval(text)

        for person in crew:
            if person.get("job") == "Director":
                return person.get("name")

        return "Unknown"

    except (ValueError, SyntaxError, TypeError):
        return "Unknown"


# --------------------------------------------------
# Prepare Movie Details
# --------------------------------------------------

movie_details["genres"] = movie_details["genres"].apply(get_names)
movie_details["cast"] = movie_details["cast"].apply(get_cast)
movie_details["director"] = movie_details["crew"].apply(get_director)

movie_details["genres_text"] = movie_details["genres"].apply(
    lambda x: ", ".join(x)
)

movie_details["cast_text"] = movie_details["cast"].apply(
    lambda x: ", ".join(x)
)


# --------------------------------------------------
# Recommendation Model
# --------------------------------------------------

cv = CountVectorizer(
    max_features=5000,
    stop_words="english"
)

vectors = cv.fit_transform(
    movies["tags"].fillna("").astype(str)
)

model = NearestNeighbors(
    metric="cosine",
    algorithm="brute"
)
model.fit(vectors)

# --------------------------------------------------
# Recommendation Function
# --------------------------------------------------

def recommend(movie_name, number_of_recommendations=5):

    movie_name = movie_name.strip().lower()

    matches = movies[
        movies["title"].str.lower() == movie_name
    ]

    if matches.empty:
        return []

    index = matches.index[0]

    distances, indices = model.kneighbors(
        vectors[index],
        n_neighbors=number_of_recommendations + 1
    )

    recommendations = []
    seen_titles = set()

    for movie_index, distance in zip(
        indices[0][1:],
        distances[0][1:]
    ):

        score = 1 - distance

        title = movies.iloc[movie_index]["title"]

        if title in seen_titles:
            continue

        seen_titles.add(title)

        recommendations.append(
            {
                "movie_id": int(
                    movies.iloc[movie_index]["movie_id"]
                ),
                "title": title,
                "score": float(score)
            }
        )

        if len(recommendations) >= number_of_recommendations:
            break

    return recommendations

# --------------------------------------------------
# Movie Details Function
# --------------------------------------------------

def get_movie_details(movie_id):

    matches = movie_details[
        movie_details["id"] == movie_id
    ]

    if matches.empty:
        return None

    movie = matches.iloc[0]

    return {
    "title": movie["title"],
    "overview": movie["overview"],
    "genres": movie["genres_text"],
    "cast": movie["cast_text"],
    "director": movie["director"],
    "rating": float(movie["vote_average"]),
    "release_date": movie["release_date"],
    "runtime": movie["runtime"],
    "popularity": float(movie["popularity"]),
    "tagline": movie["tagline"]
    }

# --------------------------------------------------
# Get Movie Details By Title
# --------------------------------------------------

def get_movie_by_title(movie_title):

    movie_title = movie_title.strip().lower()

    matches = movie_details[
        movie_details["title"].str.lower() == movie_title
    ]

    if matches.empty:
        return None

    movie = matches.iloc[0]

    return {
        "movie_id": int(movie["id"]),
        "title": movie["title"],
        "overview": movie["overview"],
        "genres": movie["genres_text"],
        "rating": float(movie["vote_average"]),
        "release_date": movie["release_date"],
        "runtime": movie["runtime"],
        "popularity": float(movie["popularity"])
    }
# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    results = recommend(
        "Batman Returns",
        number_of_recommendations=5
    )

    print("\nRecommended Movies:\n")

    for number, movie in enumerate(
        results,
        start=1
    ):

        print(
            f"{number}. {movie['title']} "
            f"(ID: {movie['movie_id']}) "
            f"- Similarity: {movie['score']:.3f}"
        )

        details = get_movie_details(
            movie["movie_id"]
        )

        if details:
            print(
                f"   Genres: {details['genres']}"
            )
            print(
                f"   Director: {details['director']}"
            )