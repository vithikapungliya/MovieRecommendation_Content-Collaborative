from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import auth
import pandas as pd
from .models import Training, Questionnaire, Movie, Playlist
from .api import get_image_api
from .colab_recommend import *
from datetime import date
import random
from .content import recommend_content

def index(request):
    return render(request,"signup.html")

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                last_user_id=User.objects.last().id
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'],id=last_user_id+1)
                auth.login(request,user)
                return redirect('home')
        else:
            return render (request,'signup.html', {'error':'Password does not match!'})
    else:
        return render(request,'signup.html')

def Login(request):
    # create_superuser()
    # User.objects.last().id=0
    # call_save()
    # movies=pd.DataFrame(list(Movie.objects.all().values()))
    # print(recommend(200, Movie))
    if request.method=="POST":
        username = request.POST.get('username') 
        password = request.POST.get('password')

        user = authenticate(username = username, password=password)
        
        if user:
            if user.is_active:
                login(request, user) #login is the django's default function
                
                return redirect("home")

            else: 
                return HttpResponse("Account not Active")
        
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid Login details supplied!")

    else:
        return render(request, 'login.html',{})

def search_movie(request):
    movie=request.GET['search']
    movie.lower()
    mydata = list(Movie.objects.filter(movie_title__icontains=movie).values())
    return render(request,"list.html",{"searched_movie":mydata,"search":movie})


def add_user_ratings(request, movie_id):
    # print(request.POS)
    rating = request.POST["rating"]
    rating=float(rating)
    print(rating)
    if Training.objects.filter(user_id = request.user.id, movie_id=movie_id).exists():
        training_val = Training.objects.get(user_id = request.user.id, movie_id=movie_id)
        training_val.rating = rating
        training_val.save()
    else:
        TrainingSet= Training(user_id= request.user.id, rating= rating, movie_id = movie_id)
        TrainingSet.save()
    return redirect("detail",movie_id=movie_id)

def split_and_find(s):
    l = []
    for i in s.split("|"):
        mydata = list(Movie.objects.filter(genre__icontains=i).values())
        l=l+mydata
    return random.sample(l, 5)

@login_required(login_url='/login')    
def recommending_movies(request):
    li = ["Adventure",
	"Animation",
	"Children" ,
	"Comedy",
	"Fantasy",
	"Romance",
	"Crime",
	"Thriller",
	"Action",
	"Horror",
	"Drama",
	"Sci-Fi",
	"IMAX",
	"Mystery",
	"Musical",
	"Documentry",
	"War",
	"Fantasy",
	"Western"]
    movie_for_user = recommend(request.user.id, Movie) 
    movie_for_user=Movie.objects.filter(movie_id__in = movie_for_user).values()
    # movie_for_user=list(map(dict, set(tuple(sorted(d.items())) for d in movie_for_user)))
    # print(len(movie_for_user))# List of dictionary: [{'movie_id': 280, 'movie_title': 'The Shawshank Redemption', 'movie_genre': 'Crime|Drama', 'rating': 4.216464863324311}]
    if Questionnaire.objects.filter(user_id=request.user.id).exists():
        question = Questionnaire.objects.get(user_id = request.user.id)
        if(date.today().weekday()<5): #this is weekday
            movie_for_day = split_and_find(question.weekdays)
        else:
            movie_for_day = split_and_find(question.weekends)
        if request.method =='POST':
            # print(request.POST)
            mood=request.POST["mood"]
            if mood=="tired":
                movie_for_mood = split_and_find(question.tired)
            elif mood=="happy":
                movie_for_mood = split_and_find(question.happy)
            elif mood=="sad":
                movie_for_mood = split_and_find(question.sad)
            else:
                movie_for_mood = split_and_find(question.inspiration)
            # print(mood)
            return render(request,"list.html",{"colab":movie_for_user,"day":movie_for_day,"mood":movie_for_mood,"li":li}) #colab+day+mood
        else:
            # print(movie_for_user)
            return render(request,"list.html",{"colab":movie_for_user,"day":movie_for_day,"li":li}) # colab + day
    else:
        # print(len(movie_for_user))
        return render(request,"list.html",{"colab":movie_for_user,"li":li}) ## colaborative


@login_required(login_url='/login')    
def recommending_movies_genre(request,genre):
    mydata = list(Movie.objects.filter(genre__icontains=genre).values())
    return render(request,"list.html",{"genre":random.sample(mydata, 12),"genre_name":genre}) ## colaborative
def combine(l):
    return "|".join(l)

def questionnaire_input(request):
    # answer = request.GET['q1']
    # print(request.GET['q2']) 
    if request.method=="POST":
        print(request.POST)
        user_id=request.user.id
        week_day_genre_list=list(request.POST['q1'])
        weekday=combine(week_day_genre_list)
        week_end_genre_list=list(request.POST['q2'])
        weekend=combine(week_end_genre_list)
        happy_genre_list=list(request.POST['q3'])
        happy=combine(week_day_genre_list)
        sad_genre_list=list(request.POST['q4'])
        sad=combine(week_day_genre_list)
        tired_genre_list=list(request.POST['q5'])
        tired=combine(week_day_genre_list)
        inspirational_genre_list=list(request.POST['q6'])
        inspirational=combine(week_day_genre_list)

        if Questionnaire.objects.filter(user_id = request.user.id).exists():
            question = Questionnaire.objects.get(user_id = request.user.id)
            question.weekdays = weekday
            question.weekends=weekend
            question.tired=tired
            question.happy=happy
            question.sad=sad
            question.inspiration=inspirational
            question.save()
        else:
            Questionnaire_set=Questionnaire(user_id=user_id,weekdays=weekday,weekends=weekend,tired=tired,happy=happy,sad=sad,inspiration=inspirational)
            Questionnaire_set.save()

        return redirect("home")
    else:
        return render(request,"quest.html")

def Rating(request,movie_id):
    movie_obj=Movie.objects.get(movie_id=movie_id)
    try:
        list_movies=recommend_content(movie_obj.movie_title)
        # list_movies=list(map(dict, set(tuple(sorted(d.items())) for d in list_movies)))
    # movie_display=list(movie_obj.values())
        content_recommendations=list(Movie.objects.filter(movie_title__in=list_movies).values())
        return render(request,"detail.html",{"display":movie_obj,"content":content_recommendations})
    except:
        return render(request,"detail.html",{"display":movie_obj})

def save_to_playlist(request, movie_id):
    if Playlist.objects.filter(user_id = request.user.id, movie_id=movie_id).exists():
        return redirect("detail",movie_id=movie_id)
    else:
        playlist=Playlist(user_id=request.user.id, movie_id=movie_id)
        playlist.save()
        return redirect("detail",movie_id=movie_id)

def genre_playlist(request,genre):
    playlist = Playlist.objects.filter(user_id = request.user.id)
    movie_ids = playlist.values_list("movie_id", flat = True)
    movie_list=list(Movie.objects.filter(genre__icontains=genre, movie_id__in = movie_ids).values())
    return render(request,"playlist.html",{"genre_playlist":movie_list,"genre_name":genre})


def call_playlist(request):
    genres=set()
    movie_dict={}

    playlist = Playlist.objects.filter(user_id = request.user.id)
    movie_ids = playlist.values_list("movie_id", flat = True)
    movies=Movie.objects.filter(movie_id__in=movie_ids)
    movie_genres = movies.values_list("genre", flat = True)
    for i in movie_genres:
        movie_genre_list=i.split("|")
        genres.update(movie_genre_list)

    for i in genres:
        movie_dict[i]=list(Movie.objects.filter(genre__icontains=i, movie_id__in = movie_ids).values())

    # print(movie_dict)
    return render(request,"playlist.html",{"playlist":movie_dict})

    # all_movie_objects=list(Movie.objects.filter(movie_id__in=movie_ids).values())

def save_to_database():
    
    df=pd.read_csv("MovieRecommendationCF/static/movie_url.csv")
    df=df[["movie_id","movie_title","movie_url", "genre"]]
    df_records = df.to_dict('records')

    model_instances = [Movie(
    movie_id = record['movie_id'],
    movie_title = record['movie_title'],
    movie_url = record['movie_url'],
    genre = record['genre']
    )for record in df_records]

    Movie.objects.bulk_create(model_instances)

def call_save():
    save_to_database()


def create_superuser():
    """
    Creates and saves a superuser with the given email and password.
    """
    user = User.objects.create_user(
        id = 0,
        username="admin",
        password="1234",
    )
    user.is_staff = True
    user.is_superuser = True
    user.save()