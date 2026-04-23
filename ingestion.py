import requests
from dotenv import load_dotenv
import os
import time

#pulling API key from .env file
load_dotenv()

#assigning API key to local variable
API_KEY = os.environ['API_KEY']

BASE_URL = "https://api.themoviedb.org/3"

#passing API key 
headers = {'Authorization': f"Bearer {API_KEY}"}

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

movies = fetch_movies("/movie/popular", pages = 1)

print(f"fetched {len(movies)} movies")