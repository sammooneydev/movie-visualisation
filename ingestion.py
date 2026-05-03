import requests
from dotenv import load_dotenv
import os
import time
from transform_data import clean_movies
from datetime import datetime

#pulling API key from .env file
load_dotenv()

#assigning API key to local variable
API_KEY = os.environ['API_KEY']

BASE_URL = "https://api.themoviedb.org/3"

#passing API key 
headers = {'Authorization': f"Bearer {API_KEY}"}

def fetch_popular():
    url = f"{BASE_URL}/movie/popular?page=1" #getting first page of most popular movies
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    movies = data.get("results", [])
    
    if not movies:
        return None
    
    #assigning top_movie to first result on popular page, as this is the current top movie
    top_movie = movies[0]
    
    return {
        "title": top_movie.get("title"),
        "rating": top_movie.get("vote_average"),
        "poster_url": f"https://image.tmdb.org/t/p/w500{top_movie.get("poster_path")}", #creating poster url from path returned by API
        "last_updated": datetime.now().strftime("%d-%m-%Y %H:%M")
    }
    
