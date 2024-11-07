import os
import pickle
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_poster(movie_id):
    api_key = os.getenv('TMDB_API_KEY')
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except requests.RequestException as e:
        st.error(f"Error fetching movie poster: {e}")
        return None

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            poster = fetch_poster(movie_id)
            if poster:
                recommended_movie_posters.append(poster)
                recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        st.error("Movie not found in the dataset.")
        return [], []

st.header('Movie Recommender System')

# Use relative paths or environment variables for file locations
movies_file = os.getenv('MOVIES_FILE', 'movie_list.pkl')
similarity_file = os.getenv('SIMILARITY_FILE', 'similarity.pkl')

try:
    with open(movies_file, 'rb') as f:
        movies = pickle.load(f)
    with open(similarity_file, 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError as e:
    st.error(f"Error loading data files: {e}")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    if recommended_movie_names and recommended_movie_posters:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
    else:
        st.warning("No recommendations found for the selected movie.")