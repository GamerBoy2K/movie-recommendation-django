from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse

def indexPage(request):
    return render(request,'index.html')

def movieDe(request):
    return render(request,'movie-details.html')

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')


def movieDetails(request,id):
    m=movies.objects.filter(movieId=id)
    return render(request,'movieDetails.html',{'m':m})

def detailsMov(request,pno):
    u=movies.objects.all()[((pno*10)-10):(pno*10)]
    return render(request,'displayMovies.html',{'a':u})

def search(request):
    try:
        movieId=request.GET['movieID']
        dummy=movie_recommendations(movieId)
        return HttpResponse(dummy)
    except:
        return render(request,'search.html')
# Create your views here.


#AI contant based

# define a function to extract features from the movie titles and genres
def extract_features(df):
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # load the Movielens dataset
    import os

    absolute_path = os.getcwd()+'\movies.csv'
    #movies = pd.read_csv('../movies.csv')
    movies = pd.read_csv(absolute_path)

    # split the genres column into binary columns
    genres = movies['genres'].str.get_dummies('|')

    # merge the binary genre columns with the original dataframe
    movies = pd.concat([movies, genres], axis=1)

    #__________________________________________________________
    #inside function to handel the error
    #__________________________________________________________
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['title'] + ' ' + df[genres.columns].astype(str).apply(lambda x: ' '.join(x), axis=1))
    return tfidf_matrix

# define a function to recommend movies based on content similarity
def recommend_movies(movie_id, n=10):
    # get the title and genre of the input movie
    title = movies[movies['movieId'] == movie_id]['title'].values[0]

    # extract features from all movies in the dataset
    movie_features = extract_features(movies)

    # get the index of the input movie
    input_index = movies[movies['movieId'] == movie_id].index[0]

    # calculate the similarity between the input movie and all other movies
    similarities = cosine_similarity(movie_features[input_index], movie_features)

    # get the indices of the most similar movies
    similar_movie_indices = similarities.argsort()[0][::-1][1:n+1].flatten()

    # get the movieIds of the most similar movies
    similar_movie_ids = [movies.iloc[i]['movieId'] for i in similar_movie_indices]

    # get the titles of the most similar movies
    similar_movie_titles = [movies[movies['movieId'] == id]['title'].values[0] for id in similar_movie_ids]

    return similar_movie_ids


# define a Django view that calls the recommend_movies function and returns the results as a JSON response
def movie_recommendations(movie_id):
    recommendations = recommend_movies(int(movie_id))
    return recommendations
''''''