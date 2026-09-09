# Movie Recommender System

### 🚀 Live Demo

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge)](https://aks870-movies-recommender-system-app-ao5rb2.streamlit.app/)

A content-based Movie Recommender System built with Python and Machine Learning that recommends movies based on the similarity of their genres, keywords, cast, crew, and overview.
## 📸 Screenshots

### 🏠 Home & Movie Selection

![Movie Recommender Home](assets/01-home.png)

### 🎯 Movie Recommendations

![Movie Recommendations](assets/02-recommendations.png)

### 🎬 Movie Details

![Movie Details](assets/03-movie-details.png)

### 🧠 How It Works

![How It Works](assets/04-how-it-works.png)

### 🛠️ About the Project

![About the Project](assets/05-about-project.png)

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
