import regex as re
from surprise import Reader, Dataset
from surprise import SVD
import pandas as pd
import random
from .models import Training, Movie


def recommend(user_id, Movie):
        
    def get_movie_id(movie_title, Movie):
        movie_id = Movie.objects.filter(movie_title=movie_title).values()
        return movie_id[0]["movie_id"]
    
    def get_movie_info(movie_id, Movie, rating):
        """
        Returns some basic information about a book given the movie id and the metadata dataframe.
        """
        Movie_object = Movie.objects.get(movie_id=movie_id)
        movie_info = {
            "movie_id": Movie_object.movie_id,
            "movie_title":Movie_object.movie_title,
            "movie_url":Movie_object.movie_url,
            "movie_genre": Movie_object.genre,
            "rating":rating
        }
        return movie_info

    def predict_review(user_id, movie_title, model, Movie):
    
        """
        Predicts the review (on a scale of 1-5) that a user would assign to a specific book. 
        """
    
        movie_id = get_movie_id(movie_title, Movie)
        review_prediction = model.predict(uid=user_id, iid=movie_id)
        return review_prediction.est

    def generate_recommendation(user_id, model, Movie, thresh=4):
    
        """
        Generates a book recommendation for a user based on a rating threshold. Only
        books with a predicted rating at or above the threshold will be recommended
        """
        l=[] 
        movie_titles_object = Movie.objects.all() #Has the movies of entire Dataset
        all_movie_titles = movie_titles_object.values_list("movie_title", flat = True)
        # random.shuffle(book_titles)
    
        for movie_title in all_movie_titles:
            rating = predict_review(user_id, movie_title, model, Movie)
            d={} #for every title, it predits the rating usinsg SVD model
            if rating >= thresh: 
               movie_id = get_movie_id(movie_title, Movie) #returns movie Id for that paticualr movie
            #    a=get_movie_info(movie_id, Movie, rating) #gets meta data of that movie - should be a list of dicts
               l.append(movie_id) #appending in the main list
        return l
    
 
    reader = Reader(rating_scale=(0.5, 5.0)) 
    df = pd.DataFrame(list(Training.objects.all().values()))
    # print(df.head(10))
    data = Dataset.load_from_df(df[['user_id', 'movie_id', 'rating']], reader)
    svd = SVD(n_epochs=5)
    
    trainset = data.build_full_trainset()
    svd.fit(trainset)

    l = generate_recommendation(user_id, svd, Movie) 
    if(len(l)>12):
        return random.sample(l, 12)
    else:
        return l