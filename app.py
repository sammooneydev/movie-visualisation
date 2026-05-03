from dash import Dash, html, dcc, callback, Output, Input
from ingestion import fetch_popular, fetch_movies, fetch_movies_for_genres, fetch_genres, fetch_top_rated, fetch_upcoming_movies
from transform_data import extract_movie_genres, clean_genres, clean_movies, count_movies_per_genre, get_top_100_movies, prepare_top_10, group_by_release_date
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

    html.Div(id="movie-card", style={'width': '280px'}),

    html.Div([
        dcc.Graph(id="genre_chart")
    ], style={
        'flex': '1',
        'backgroundColor': '#2a2a2a',
        'padding': '10px',
        'borderRadius': '8px',
        'border': '1px solid #444',
    })

], style={
    'display': 'flex',
    'justifyContent': 'center',
    'alignItems': 'flex-start',
    'gap': '20px',
    'padding': '20px'
}),
    
    #top 10 movies chart + upcoming release heatmap
    html.Div([
    html.Div([
        dcc.Graph(id="top_movies_chart")
    ], style={
        'width': '48%',
        'backgroundColor': '#2a2a2a',
        'padding': '15px',
        'borderRadius': '8px',
        'border': '1px solid #444'
    }),

    html.Div([
        dcc.Graph(id="release_heatmap")
    ], style={
        'width': '48%',
        'backgroundColor': '#2a2a2a',
        'padding': '15px',
        'borderRadius': '8px',
        'border': '1px solid #444'
    })

], style={
    'display': 'flex',
    'justifyContent': 'space-between',
    'gap': '20px',
    'padding': '20px'
})
])

#callback to update upcoming releases heatmap
@callback(
    Output('release_heatmap', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_heatmap(n):
    raw_movies = fetch_upcoming_movies()

    date_counts = group_by_release_date(raw_movies)

    return create_release_heatmap(date_counts)

#callback to update top movies chart
@callback(
    Output('top_movies_chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_top_movies(n):
    #fetching top rated movies
    raw_movies = fetch_top_rated()

    #cleaning movie data
    movies = clean_movies(raw_movies)

    #getting top 100 films
    top_movies = get_top_100_movies(movies)

    #preparing top 10 for display
    titles, ratings = prepare_top_10(top_movies)

    return create_top_movies_chart(titles, ratings)

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
        
    figure = px.bar(x=names, y=values, title="Distribution of Movies per Genre on Discover Page")
    
    #making figure darker colour to fit with dashboard theme
    figure.update_layout(
    plot_bgcolor='#1e1e1e',
    paper_bgcolor='#1e1e1e',
    font_color='white',
    
    xaxis_title="Genre",
    yaxis_title="Number of Movies",
    
    title={
        'x': 0.5,
        'xanchor': 'center'
    },
    
    xaxis={'categoryorder':'total descending'}
    )
    return figure

def create_top_movies_chart(titles, ratings):
    figure = px.bar(
        x=ratings,
        y=titles,
        orientation='h',
        title="Average Rating of Top 10 Highest Rated Movies"
    )

    #dark theme styling + spacing out bars a smidge
    figure.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font_color='white',
        xaxis_title="Average Rating",
        yaxis_title="Movie Title",
        title={
            'x': 0.5,
            'xanchor': 'center'
        },
        bargap=0.4
    )
    
    figure.update_traces(
        width=0.6
    )

    return figure

def create_release_heatmap(date_counts):
    dates = list(date_counts.keys())
    values = list(date_counts.values())

    figure = px.density_heatmap(
        x=dates,
        y=values,
        title="Heatmap of Upcoming Movie Releases"
    )

    figure.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font_color='white',
        title={
            'x': 0.5,
            'xanchor': 'center'
        },
        height=400,
    )

    return figure

if __name__ == '__main__':
    app.run(debug=True)
