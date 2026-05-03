def build_actor_movie_graph(actor, movies):
    elements = []

    actor_id = str(actor["id"])

    #actor node
    elements.append({
        "data": {
            "id": actor_id,
            "label": actor["name"],
            "type": "actor"
        }
    })

    #movie nodes + edges
    for movie in movies[:20]: #limiting nodes to 20 to allow for a good but controlled sample size
        movie_id = str(movie["id"])

        elements.append({
            "data": {
                "id": movie_id,
                "label": movie["title"],
                "type": "movie"
            }
        })

        elements.append({
            "data": {
                "source": actor_id,
                "target": movie_id
            }
        })

    return elements