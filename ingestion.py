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

#generic fetching function for use throughout project
def fetch_movies(endpoint, pages):
    all_movies = []
    
    for page in range(1, pages + 1):
        url = f"{BASE_URL}{endpoint}?page={page}"
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        all_movies.extend(data.get("results", []))
        
        #for rate limiting
        time.sleep(0.2)
    
    return all_movies

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
        "poster_url": f"https://image.tmdb.org/t/p/w500{top_movie.get('poster_path')}", #creating poster url from path returned by API
        "last_updated": datetime.now().strftime("%d-%m-%Y %H:%M")
    }
    
def fetch_movies_for_genres():
    return fetch_movies("/discover/movie", pages=5) #returning first 5 pages of discover tab 

#function to fetch all movie genres from the API
def fetch_genres():
    url = f"{BASE_URL}/genre/movie/list"
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    return data.get("genres", [])

def fetch_top_rated():
    return fetch_movies("/movie/top_rated", pages=5) #fetching around about the top 100 highest rated movies

#function to fetch upcoming movie releases
def fetch_upcoming_movies():
    return fetch_movies("/movie/upcoming", pages=3)

#function to search for an actor and return the best match returned by the API
def search_actor(name):
    url = f"{BASE_URL}/search/person?query={name}"
    response = requests.get(url, headers=headers)
    data = response.json()

    results = data.get("results", [])
    if not results:
        return None

    return results[0] #returning first result since that would be the best match

#function to get movies associated with a specific actor
def fetch_actor_movies(person_id):
    url = f"{BASE_URL}/person/{person_id}/movie_credits"
    response = requests.get(url, headers=headers)
    data = response.json()

    return data.get("cast", [])