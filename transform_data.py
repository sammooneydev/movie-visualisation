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
    
def count_movies_per_genre(movie_genres):
    counts = {}
    
    for genre in movie_genres:
        genre_id = genre["genre_id"]
        counts[genre_id] = counts.get(genre_id, 0) + 1 #counting the number of films in any given genre on the fetched pages
        
    return counts