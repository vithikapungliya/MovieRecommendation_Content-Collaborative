import numpy as np # Linear Algebra and lists
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import ast
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

new = pd.read_csv("MovieRecommendationCF/static/Final_ContentFiltering.csv") # just reading 
cv = CountVectorizer(max_features=5000,stop_words='english')
vector = cv.fit_transform(new['tags']).toarray()
similarity = cosine_similarity(vector)

    # l=np.array(list_movies)
    # l=l.flatten()
    # a=[l[i]["title"] for i in range(len(l))] - Views.py Covert O/P of Colaborative Filtering to I/P of Content.
    

def recommend_content(movie):
    l=[]
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:7]:
        l.append(new.iloc[i[0]].title)
    return l