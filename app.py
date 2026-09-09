import streamlit as st
from recommender import (recommend,movies,get_movie_details,get_movie_by_title)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

if "recommended_movie" not in st.session_state:
    st.session_state.recommended_movie = ""


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
    padding: 24px 18px;
    border-radius: 18px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    min-height: 185px;
    margin-bottom: 18px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.movie-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.14);
}

.movie-number {
    font-size: 13px;
    font-weight: 700;
    opacity: 0.7;
    letter-spacing: 0.5px;
}

.movie-title {
    font-size: 19px;
    font-weight: 650;
    margin-top: 14px;
    line-height: 1.35;
    min-height: 54px;
    word-break: break-word;
}

.similarity {
    font-size: 14px;
    margin-top: 14px;
    font-weight: 600;
}

.movie-id {
    font-size: 12px;
    margin-top: 8px;
    opacity: 0.6;
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
# Movie List
# --------------------------------------------------

movie_list = sorted(
    movies["title"].dropna().unique().tolist()
)


# --------------------------------------------------
# Project Stats
# --------------------------------------------------

stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.metric("🎬 Movies", f"{len(movie_list):,}")

with stat_col2:
    st.metric("🤖 Recommendation Type", "Content-Based")

with stat_col3:
    st.metric("✨ Results", "Top 5")


# --------------------------------------------------
# Choose Movie
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🔎 Choose a Movie</div>',
    unsafe_allow_html=True
)

st.caption(
    f"🎬 {len(movie_list):,} movies available • "
    "Type a movie name to search"
)

selected_movie = st.selectbox(
    "Select a movie from the list",
    movie_list,
    index=0
)


# --------------------------------------------------
# Clear Old Recommendations When Movie Changes
# --------------------------------------------------

if (
    st.session_state.recommended_movie
    and st.session_state.recommended_movie != selected_movie
):
    st.session_state.recommendations = []
    st.session_state.recommended_movie = ""


# --------------------------------------------------
# Selected Movie Preview
# --------------------------------------------------

selected_details = get_movie_by_title(selected_movie)

if selected_details:

    st.markdown("### 🎬 Selected Movie")

    preview_col1, preview_col2, preview_col3, preview_col4, preview_col5 = st.columns(5)

    with preview_col1:
        st.markdown(
            f"**🎬 {selected_details['title']}**"
        )

    with preview_col2:
        st.markdown(
            f"**⭐ Rating**  \n"
            f"{selected_details['rating']:.1f}/10"
        )

    with preview_col3:
        st.markdown(
            f"**📅 Release Date**  \n"
            f"{selected_details['release_date'] or 'Not available'}"
        )

    with preview_col4:

        if selected_details["runtime"]:
            st.markdown(
                f"**⏱️ Runtime**  \n"
                f"{selected_details['runtime']} minutes"
            )

        else:
            st.markdown(
                "**⏱️ Runtime**  \n"
                "Not available"
            )

    with preview_col5:
        st.markdown(
            f"**📈 Popularity**  \n"
            f"{selected_details['popularity']:.2f}"
        )

    # Movie Overview
    st.markdown("#### 📝 Overview")

    if selected_details["overview"]:
        st.write(selected_details["overview"])

    else:
        st.write("Overview not available.")

    # Movie Genres
    st.markdown("#### 🎭 Genres")

    if selected_details["genres"]:
        st.write(selected_details["genres"])

    else:
        st.write("Genres not available.")


# --------------------------------------------------
# Recommendation Button
# --------------------------------------------------

button_col1, button_col2 = st.columns(2)

with button_col1:
    recommend_button = st.button(
        f"🎯 Find Movies Like {selected_movie}",
        use_container_width=True
    )

with button_col2:
    clear_button = st.button(
        "🗑️ Clear Recommendations",
        use_container_width=True
    )


if clear_button:
    st.session_state.recommendations = []
    st.session_state.recommended_movie = ""
    st.rerun()


# --------------------------------------------------
# Recommendations
# --------------------------------------------------

if recommend_button:

    with st.spinner("🤖 Finding movies similar to your selection..."):

        st.session_state.recommendations = recommend(
            selected_movie,
            number_of_recommendations=5
        )

    st.session_state.recommended_movie = selected_movie

    if st.session_state.recommendations:
        st.success(
            f"✨ Recommendations generated for **{selected_movie}**"
        )

    else:
        st.warning(
            f"⚠️ No recommendations found for **{selected_movie}**"
        )


recommendations = st.session_state.recommendations


if not recommendations:
    st.info(
        f"🎬 Select a movie above and click "
        f"'🎯 Find Movies Like {selected_movie}' "
        "to discover similar movies."
    )


if recommendations:

    st.markdown(
        '<div class="section-title">✨ Recommended For You — Top 5</div>',
        unsafe_allow_html=True
    )

    if st.session_state.recommended_movie:
        st.info(
            f"🎬 Showing recommendations based on "
            f"**{st.session_state.recommended_movie}**"
        )

    st.caption(
        f"🎬 {len(recommendations)} similar movies found for "
        f"**{selected_movie}**"
    )

    st.caption(
        "🎯 Recommendations are generated using movie overview, "
        "genres, keywords, cast and director information."
    )


    # Remove duplicate titles
    unique_recommendations = []
    seen_titles = set()

    for movie in recommendations:

        title = movie["title"]

        if title not in seen_titles:

            unique_recommendations.append(movie)
            seen_titles.add(title)


    # Create recommendation columns
    columns = st.columns(3)

    for index, movie in enumerate(unique_recommendations):

        with columns[index % 3]:

            movie_number = index + 1
            movie_title = movie["title"]
            movie_id = movie["movie_id"]
            score = movie["score"]


            # Movie Card
            card_html = (
                '<div class="movie-card">'
                f'<div class="movie-number">#{movie_number}</div>'
                f'<div class="movie-title">{movie_title}</div>'
                f'<div class="similarity">🎯 Match Score: {score:.3f}</div>'
                f'<div class="movie-id">🎬 Movie ID: {movie_id}</div>'
                '</div>'
            )

            st.markdown(
                card_html,
                unsafe_allow_html=True
            )


            # Movie Details
            details = get_movie_details(movie_id)

            if details:

                with st.expander("🎬 View Details"):

                    st.markdown(f"### 🎬 {details['title']}")

                    if details["tagline"]:
                        st.caption(f"“{details['tagline']}”")

                    st.markdown("#### 📝 Overview")

                    if details["overview"]:
                        st.write(details["overview"])

                    else:
                        st.write("Overview not available.")


                    st.markdown("#### 🎭 Movie Information")

                    info_col1, info_col2, info_col3 = st.columns(3)

                    with info_col1:
                        st.markdown(
                            f"**⭐ Rating**  \n"
                            f"{details['rating']:.1f}/10"
                        )

                    with info_col2:
                        st.markdown(
                            f"**📅 Release Date**  \n"
                            f"{details['release_date'] or 'Not available'}"
                        )

                    with info_col3:

                        if details["runtime"]:
                            st.markdown(
                                f"**⏱️ Runtime**  \n"
                                f"{details['runtime']} minutes"
                            )

                        else:
                            st.markdown(
                                "**⏱️ Runtime**  \n"
                                "Not available"
                            )


                    st.markdown("#### 🎬 Credits")

                    credit_col1, credit_col2 = st.columns(2)

                    with credit_col1:
                        st.markdown(
                            f"**🎥 Director**  \n"
                            f"{details['director']}"
                        )

                    with credit_col2:
                        st.markdown(
                            f"**🎭 Genres**  \n"
                            f"{details['genres'] or 'Not available'}"
                        )


                    st.markdown(
                        f"**👥 Cast**  \n"
                        f"{details['cast'] or 'Not available'}"
                    )

                    st.markdown(
                        f"**📈 Popularity:** "
                        f"{details['popularity']:.2f}"
                    )

            else:
                st.warning(
                    "⚠️ Movie details are not available for this recommendation."
                )


# --------------------------------------------------
# How Recommendation Works
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🧠 How It Works</div>',
    unsafe_allow_html=True
)

with st.expander("🔍 Understand the Recommendation System"):

    st.markdown(
        """
        This movie recommender uses a **content-based filtering**
        approach to find movies similar to your selected movie.

        ### ⚙️ Recommendation Pipeline

        **1. Movie Data**

        Movie information such as overview, genres, keywords,
        cast and director is used as the basis for recommendations.

        **2. Feature Extraction**

        Important movie text is converted into numerical features
        using **CountVectorizer**.

        **3. Similarity Calculation**

        The system compares movies using **cosine similarity**
        through a nearest-neighbor search model.

        **4. Similar Movies**

        The system finds movies with the most similar feature
        patterns to the selected movie.

        **5. Top Recommendations**

        Finally, the **5 most similar movies** are displayed
        along with their similarity scores.
        """
    )

    st.info(
        "💡 The recommendations are based on movie content and "
        "metadata, not on user ratings or watch history."
    )


# --------------------------------------------------
# About Project
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📌 About This Project</div>',
    unsafe_allow_html=True
)

with st.expander("🎬 Movie Recommender System"):

    st.markdown(
        """
        This project is a **Machine Learning based movie
        recommendation system** built using Python and Streamlit.

        ### 🚀 Technologies Used

        - 🐍 Python
        - 🎨 Streamlit
        - 🐼 Pandas
        - 🔢 NumPy
        - 🤖 Scikit-learn
        - 📊 CountVectorizer
        - 🔍 Nearest Neighbors

        ### 🎯 Main Features

        - Search and select movies
        - Content-based movie recommendations
        - Top 5 similar movies
        - Similarity scores
        - Movie details
        - Genre, cast and director information
        - Rating, release date and runtime
        - Interactive Streamlit interface
        """
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