import streamlit as st
from recommender import recommend, movies


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
<style>
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 35px;
}

.section-title {
    font-size: 28px;
    font-weight: 650;
    margin-top: 30px;
    margin-bottom: 20px;
}

.movie-card {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    min-height: 150px;
    margin-bottom: 15px;
    text-align: center;
}

.movie-number {
    font-size: 14px;
    font-weight: 600;
}

.movie-title {
    font-size: 19px;
    font-weight: 650;
    margin-top: 12px;
    line-height: 1.3;
}

.similarity {
    font-size: 14px;
    margin-top: 15px;
}

.footer {
    text-align: center;
    margin-top: 60px;
    padding: 20px;
    font-size: 14px;
}
</style>
""",
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎬 Movie Recommender</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Discover movies similar to the ones you love.</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Movie Selection
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🔎 Choose a Movie</div>',
    unsafe_allow_html=True
)

movie_list = sorted(
    movies["title"].dropna().unique().tolist()
)

selected_movie = st.selectbox(
    "Select a movie from the list",
    movie_list,
    label_visibility="collapsed"
)


# --------------------------------------------------
# Recommendation Button
# --------------------------------------------------

recommend_button = st.button(
    "🎯 Recommend Movies",
    use_container_width=True
)


# --------------------------------------------------
# Recommendations
# --------------------------------------------------

if recommend_button:

    recommendations = recommend(
        selected_movie,
        number_of_recommendations=5
    )

    if recommendations:

        st.markdown(
            '<div class="section-title">✨ Recommended For You</div>',
            unsafe_allow_html=True
        )

        # Remove duplicate titles
        unique_recommendations = []
        seen_titles = set()

        for movie in recommendations:

            title = movie["title"]

            if title not in seen_titles:
                unique_recommendations.append(movie)
                seen_titles.add(title)

        columns = st.columns(len(unique_recommendations))

        for index, movie in enumerate(unique_recommendations):

            with columns[index]:

                movie_number = index + 1
                movie_title = movie["title"]
                score = movie["score"]

                card_html = (
                    '<div class="movie-card">'
                    f'<div class="movie-number">#{movie_number}</div>'
                    f'<div class="movie-title">{movie_title}</div>'
                    f'<div class="similarity">🎯 Similarity: {score:.3f}</div>'
                    '</div>'
                )

                st.markdown(
                    card_html,
                    unsafe_allow_html=True
                )

    else:

        st.warning(
            "⚠️ Sorry, we couldn't find recommendations for this movie."
        )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
<div class="footer">
    🎬 Movie Recommender System
    <br>
    Built with Python, Streamlit & Machine Learning
</div>
""",
    unsafe_allow_html=True
)