from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def indexPage(request):
    return render(request,'index.html')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect(adminDashboard)
    else:
        form = RegisterUserForm()
    return render(request,'signup.html', {'form':form})

def login_users(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(adminDashboard)
        else:
            messages.success(request,"Invalid Details")
            return redirect(invalidCredentials)
    else:
        return render(request,'login.html')

def logout_users(request):
    logout(request)
    return redirect(invalidCredentials)

def update_user(request):
    #return render(request, 'updateUser.html',{})
    
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        form=RegisterUserForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
        return render(request, 'updateUser.html',{'form':form})
    else:
        messages.success(request,"You must be logged in to update")
        return redirect(login)
    
    

def adminDashboard(request):
    return render(request,'adminHome.html')

def invalidCredentials(request):
    return render(request,'invalidCredentials.html')

def signup(request):
    return render(request,'signup.html')

def searchResult(request):
    searchKey=request.GET['searchBox']
    searchList=movies.objects.filter(title__icontains=searchKey)
    return render(request,'searchResult.html',{'ms':searchList, 'key':searchKey})

def addMovies(request):
    return render(request, 'addMovie.html')

def addMov(request):
    m=movies()
    ''' 
    if request.method == 'POST':
        print('Hollla')
        print(request.FILES)
    '''
    m.title=request.POST['title']
    m.genres=request.POST['genre']
    m.imagePoster=request.FILES['uploadFromPC']
    #print('holaaaaaaaa '+len(request.FILES['uploadFromPC']))
    m.save()
    
    return redirect(addMovies)
#this page for contant recommendation and selected movie details

def editMovie(request,id):
    m=movies.objects.get(movieId=id)
    return render(request,'editMovie.html',{'x':m})

def editFinalMovie(request):
    mid=request.POST['movieID']
    print(mid)
    m=movies.objects.get(movieId=mid)
    '''
    form=mform(request.POST,instance=m)
    if form.is_valid():
        print('hi')
        form.save()
        return redirect("../view")
    print('momoo')
    return render(request,'editMovie.html',{'x':m})
    '''
    m.title=request.POST['title']
    m.genres=request.POST['genre']
    m.imagePoster=request.FILES['uploadFromPC']
    m.save()
    return redirect(indexPage)

def movieDetails(request,id):
    m=movies.objects.filter(movieId=id)

    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # load the Movielens dataset
    import os

    absolute_path = os.getcwd()+'\movies.csv'
    #movies = pd.read_csv('../movies.csv')
    movie = pd.read_csv(absolute_path)

    # split the genres column into binary columns
    genres = movie['genres'].str.get_dummies('|')

    # merge the binary genre columns with the original dataframe
    movie = pd.concat([movie, genres], axis=1)

    #__________________________________________________________
    #inside function to handel the error
    #__________________________________________________________

    # define a function to extract features from the movie titles and genres
    def extract_features(df):
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['title'] + ' ' + df[genres.columns].astype(str).apply(lambda x: ' '.join(x), axis=1))
        return tfidf_matrix

    # define a function to recommend movies based on content similarity
    def recommend_movies(movie_id, n=4):
        # get the title and genre of the input movie
        title = movie[movie['movieId'] == movie_id]['title'].values[0]

        # extract features from all movies in the dataset
        movie_features = extract_features(movie)

        # get the index of the input movie
        input_index = movie[movie['movieId'] == movie_id].index[0]

        # calculate the similarity between the input movie and all other movies
        similarities = cosine_similarity(movie_features[input_index], movie_features)

        # get the indices of the most similar movies
        similar_movie_indices = similarities.argsort()[0][::-1][1:n+1].flatten()

        # get the movieIds of the most similar movies
        similar_movie_ids = [movie.iloc[i]['movieId'] for i in similar_movie_indices]

        # get the titles of the most similar movies
        similar_movie_titles = [movie[movie['movieId'] == id]['title'].values[0] for id in similar_movie_ids]

        return similar_movie_ids


    # define a Django view that calls the recommend_movies function and returns the results as a JSON response
    def movie_recommendations(movie_id):
        recommendations = recommend_movies(int(movie_id))
        return(recommendations)


    dummy=list(movie_recommendations(id))
    #list1=['102125','77561']
    ms=movies.objects.filter(movieId__in=dummy)
    
    return render(request,'movieDetails.html',{'m':m, 'ms':ms})

#this lists all the movies in the database with max of 10 limit per page
def allMovies(request,pno):
    maxResult=10
    u=movies.objects.all()[((pno*maxResult)-maxResult):(pno*maxResult)]
    return render(request,'displayMovies.html',{'a':u})


def search(request):
    try:
        movieId=request.GET['movieID']
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

        # define a function to extract features from the movie titles and genres
        def extract_features(df):
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
            return(recommendations)


        dummy=list(movie_recommendations(movieId))
        #return HttpResponse(dummy)
        m=movies.objects.filter(movieId__in=dummy)
        #return render(request,'search.html',{'a':dummy})
        return render(request,'search.html',{'a':m})
    except:
        return render(request,'search.html')
# Create your views here.

'''
#AI contant based

# define a function to extract features from the movie titles and genres
def extract_features(df):
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['title'] + ' ' + df[genres.columns].astype(str).apply(lambda x: ' '.join(x), axis=1))
    return tfidf_matrix

# define a function to recommend movies based on content similarity
def recommend_movies(movie_id, n=10):
    from sklearn.metrics.pairwise import cosine_similarity
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

    return similar_movie_titles

'''

'''
# define a Django view that calls the recommend_movies function and returns the results as a JSON response
def movie_recommendations(movie_id):
    recommendations = recommend_movies(int(movie_id))
    return recommendations
'''
'''
# define a Django view that calls the recommend_movies function and returns the results as a JSON response
def movie_recommendations(request):
    try:

        movie_id=request.GET['movieID']
        import pandas as pd

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

        recommendations = recommend_movies(int(movie_id))
        response_data = {
            'movie_id': movie_id,
            'recommendations': recommendations
        }
        return JsonResponse(response_data)
    except:
        return render(request,'search.html')
'''