from dash import Dash, html, dcc, callback, Output, Input
from ingestion import fetch_popular, fetch_movies, fetch_movies_for_genres, fetch_genres
from transform_data import extract_movie_genres, clean_genres, clean_movies, count_movies_per_genre
import plotly.express as px

#fetching most popular film from API
movie = fetch_popular()

app = Dash()

app.layout = html.Div([

    #application header
    html.Div([
        html.H1(
            'TMDB Visualisation Dashboard',
            style={'textAlign': 'center'}
        )
    ]),

    dcc.Interval(
    id='interval-component',
    interval=30 * 60 * 1000,  #refresh every 30 mins
    n_intervals=0
    ),
    
    #most popular movie right now + bar chart of genres
    html.Div([

    html.Div(id="movie-card", style={'width': '30%'}),

    html.Div([
        dcc.Graph(id="genre_chart")
    ], style={'width': '65%'})

], style={
    'display': 'flex',
    'justifyContent': 'space-between',
    'alignItems': 'flex-start',
    'padding': '20px'
})
])

#callback function to update movie-card every 30 mins + on page refresh
@callback(
    Output('movie-card', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_movie(n):
    movie = fetch_popular()

    if not movie:
        return html.Div("No data available")

    return html.Div([

        html.H2("Current Most Popular Movie"),

        html.Img(
            src=movie["poster_url"],
            style={'width': '200px'}
        ),

        html.H3(movie["title"]),

        html.P(f"Average Rating: {round(movie['rating'], 1)}"),

        html.P(f"Last updated: {movie['last_updated']}")

    ], style={
        'backgroundColor': '#2a2a2a',
        'padding': '10px',
        'borderRadius': '6px',
        'textAlign': 'center',
        'width': '250px',
        'margin': '20px auto'
    })

#callback to update genre bar chart every 30 mins + on page refresh
@callback(
    Output('genre_chart', 'figure'),
    Input('interval-component', 'n_intervals')
)    
def update_genre_chart(n):
    #fetching movies for analysis of genre distribution
    raw_movies = fetch_movies("/discover/movie", pages=3)

    #getting movie to genre relationships
    movie_genres = extract_movie_genres(raw_movies)

    #fetching list of genres for lookup
    raw_genres = fetch_genres()
    genres = clean_genres(raw_genres) #cleaning genre data

    #creating lookup dict (id to genre name)
    genre_lookup = {g["id"]: g["name"] for g in genres}
    
    #counting number of movies in each genre
    counts = count_movies_per_genre(movie_genres)
    
    return create_genre_count(counts, genre_lookup)

def create_genre_count(counts, genre_lookup):
    names = []
    values = []
    
    #mapping genre ids to names and counts
    for genre_id, count in counts.items():
        names.append(genre_lookup.get(genre_id, "unknown"))
        values.append(count)
        
    figure = px.bar(x=names, y=values)
    
    #making figure darker colour to fit with dashboard theme
    figure.update_layout(
    plot_bgcolor='#1e1e1e',
    paper_bgcolor='#1e1e1e',
    font_color='white'
    )
    return figure

if __name__ == '__main__':
    app.run(debug=True)
