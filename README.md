# Movie Recommender System

A content-based Movie Recommender System built with Python and Machine Learning that recommends movies based on the similarity of their genres, keywords, cast, crew, and overview.

## Features

- Movie-based recommendations
- Content-based recommendation system
- Search and select from thousands of movies
- Cosine similarity-based recommendations
- Similarity score for each recommendation
- Interactive Streamlit web interface
- Clean and responsive user interface

## How It Works

The system uses a **content-based filtering** approach.

Movie information such as:

- Overview
- Genres
- Keywords
- Top cast members
- Director

is combined into a single `tags` feature.

The tags are converted into numerical vectors using **CountVectorizer**, and **Cosine Similarity** is used to measure how similar movies are to each other.

### Recommendation Pipeline

```text
Movie Dataset
      |
      v
Data Preprocessing
      |
      v
Feature Engineering
      |
      v
Movie Tags
      |
      v
CountVectorizer
      |
      v
Cosine Similarity
      |
      v
Similar Movies
      |
      v
Streamlit Web App