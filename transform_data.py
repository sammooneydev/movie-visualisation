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
