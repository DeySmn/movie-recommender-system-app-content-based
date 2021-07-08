import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4cbbd14a48bf514d7586055a19dc6dfd&language=en-US'.format(movie_id))

    data = response.json()

    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster = []
    for i in movies_list:

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System!!')

selected_movie_name=st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters=recommend(selected_movie_name)

    cnt=1
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    colno = col1
    for name,poster in zip(names,posters):
        if cnt==1:
            colno=col1
        elif cnt==2:
            colno=col2
        elif cnt==3:
            colno=col3
        elif cnt==4:
            colno=col4
        elif cnt==5:
            colno=col5
        with colno:
            st.text(name)
            st.image(poster)
        cnt+=1


