from http.client import responses

import streamlit  as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title="Movie Recommendation System", layout="centered")

def fetchPoster(movieId):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movieId))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']


moviesList =  pickle.load(open('movies.pkl','rb'))
# moviesList = pd.DataFrame(moviesList)
similarity =  pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    movieIndex = moviesList[moviesList['title'] == movie].index[0]
    myMovieDistancesList = similarity[movieIndex]
    top5RecommendedMoviesList = sorted(list(enumerate(myMovieDistancesList)), reverse=True, key=lambda x: x[1])[1:6]

    recommendedMovies = []
    recommendedMoviesPoster = []
    for i in top5RecommendedMoviesList:
        movieId = moviesList.iloc[i[0]].movie_id
        #fetch poster based on id from API
        recommendedMovies.append(moviesList.iloc[i[0]]['title'])
        recommendedMoviesPoster.append(fetchPoster(movieId))

    return recommendedMovies,recommendedMoviesPoster

st.title('Movie Recommended System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    moviesList['title'],
    index=None,
    placeholder="Select your movie...",
)

if st.button("Recommend"):
    if selected_movie_name == None:
        st.write('Please select movie first')
    else:
        names,poster = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.image(poster[0])
            st.text(names[0])

        with col2:
            st.image(poster[1])
            st.text(names[1])

        with col3:
            st.image(poster[2])
            st.text(names[2])

        with col4:
            st.image(poster[3])
            st.text(names[3])

        with col5:
            st.image(poster[4])
            st.text(names[4])
