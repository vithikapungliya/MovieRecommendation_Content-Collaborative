from django.urls import path,include
from Reccomend import views
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    # path("",views.index,name="index"),
    path("",views.recommending_movies,name="home"),
    path("login",views.Login,name="Login"),
    path("logout",LogoutView.as_view(next_page="Login"),name="logout"),
    path("signup",views.signup,name="signup"),
    path("search",views.search_movie,name="search"),
    path("playlist/<int:movie_id>",views.save_to_playlist),
    path("Rating/<int:movie_id>",views.Rating,name="detail"),
    path("add_user_ratings/<int:movie_id>",views.add_user_ratings,name="user_rating"),
    path("genre/<genre>",views.recommending_movies_genre,name="genre"),
    path("questionnaire_input",views.questionnaire_input,name="questionnaire_input"),
    path("playlist",views.call_playlist, name="playlist"),
    path("genre_playlist/<genre>",views.genre_playlist,name="genre_playlist"),
    path("/reccomending_movies",views.recommending_movies,name="recommending_movies")
]