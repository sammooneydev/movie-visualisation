def clean_movie(raw_movie):
    if not raw_movie.get("id"):
        return None #skip any invalid rows that might have been returned
    
    title = raw_movie.get("title", "").strip()
    if not title:
        return None #skip any rows without a film title
    
    return {
        "id": raw_movie["id"],
        "title": title,
        "release_date": raw_movie.get("release_date"),
        "rating": float(raw_movie.get("vote_average", 0.0)),
        "vote_count": int(raw_movie.get("vote_count", 0)),
        "popularity": float(raw_movie.get("popularity", 0.0))
    }

def clean_movies(raw_movies):
    cleaned = []

    for movie in raw_movies:
        cleaned_movie = clean_movie(movie)

        if cleaned_movie:
            cleaned.append(cleaned_movie)

    return cleaned

#function to split up lists of genre ids that the api spits out
def extract_movie_genres(raw_movies):
    movie_genres = []

    for movie in raw_movies:
        movie_id = movie.get("id")
        genres = movie.get("genre_ids", [])

        for genre_id in genres:
            movie_genres.append({
                "movie_id": movie_id,
                "genre_id": genre_id
            })

    return movie_genres

#creating a clean list of genres to make genre lookups easy
def clean_genres(raw_genres):
    return [
        {
            "id": g["id"],
            "name": g["name"]
        }
        for g in raw_genres
    ]
    
#fucntion to pull out the cast of a given movie using the /credits API endpoint
def extract_cast(movie_id, credits_json):
    cast_list = []
    actors = []

    for actor in credits_json.get("cast", [])[:20]:  #limit to the top 20 cast members
        actor_id = actor.get("id")
        name = actor.get("name")

        if not actor_id or not name:
            continue

        actors.append({
            "id": actor_id,
            "name": name
        })

        cast_list.append({
            "movie_id": movie_id,
            "actor_id": actor_id
        })

    return actors, cast_list