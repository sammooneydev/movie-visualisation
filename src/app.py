from dash import Dash, html, dcc, callback, Output, Input
from ingestion import fetch_popular, fetch_movies, fetch_movies_for_genres, fetch_genres, fetch_top_rated, fetch_upcoming_movies, search_actor, fetch_actor_movies
from transform_data import extract_movie_genres, clean_genres, clean_movies, count_movies_per_genre, get_top_100_movies, prepare_top_10, group_by_release_date
from graph_creator import build_actor_movie_graph
import dash_cytoscape as cyto
import plotly.express as px
import plotly.graph_objects as go

#fetching most popular film from API
movie = fetch_popular()

app = Dash(assets_folder="../assets")

app.layout = html.Div([

    # Header
    html.Div([
        html.H1('TMDB Visualisation Dashboard', style={'textAlign': 'center'})
    ]),

    dcc.Interval(
        id='interval-component',
        interval=30 * 60 * 1000, #refresh every 30 mins
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
    }),

    #actor node link graph
    html.Div([
        html.H2("Actor to Movie Node Link Graph", style={'textAlign':'center'}),
    html.Div([
        dcc.Input(
            id="actor-input",
            type="text",
            placeholder="Enter name of actor to generate interactive graph of films they have been in",
            style={
                'backgroundColor': '#1e1e1e',
                'color': 'white',
                'border': '1px solid #444',
                'padding': '10px',
                'borderRadius': '6px',
                'marginRight': '10px',
                'width': '575px',
                'height': '50px',
                'justifyContent': 'center'
            },
            debounce = True
        ),
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'marginBottom': '20px'
        }),
    
        cyto.Cytoscape(
            id='actor-graph',
            layout={
                'name': 'cose',
                'idealEdgeLength': 120,
                'nodeRepulsion':8000,
                'gravity': 0.5,
                'numIter': 1000,
                'initialTemp': 200
            },
            style={'width': '100%', 'height': '600px'},
            elements=[],
            zoom=0.6,
            minZoom=0.2,
            maxZoom=2,
            stylesheet=[
        {
            'selector': 'node[type="actor"]',
            'style': {
                'background-color': '#E69F00',
                'label': 'data(label)',
                'color': 'white',
                'font-size': '12px',
                'text-valign': 'center',
                'text-halign': 'center',
                'width': '40px',
                'height': '40px',
                'text-outline-width': 2,
                'text-outline-color': '#000000',
            }
        },
        {
            'selector': 'node[type="movie"]',
            'style': {
                'background-color': '#56B4E9',
                'label': 'data(label)',
                'color': 'white',
                'font-size': '10px',
                'text-valign': 'center',
                'text-halign': 'center',
                'width': '30px',
                'height': '30px',
                'text-outline-width': 2,
                'text-outline-color': '#000000',
            }
        },
        {
            'selector': 'edge',
            'style': {
                'line-color': '#888',
                'width': 1
            }
        }
    ]
)
], style={
        'padding': '20px',
        'backgroundColor': '#2a2a2a',
        'marginTop': '30px'
    })
])

#callback to update movie to actor node graph
@callback(
    Output("actor-graph", "elements"),
    Input("actor-input", "value"),
    prevent_initial_call=True
)
def update_actor_graph(actor_name):

    if not actor_name or len(actor_name) < 3:
        return []

    actor = search_actor(actor_name)

    if not actor:
        return []

    movies = fetch_actor_movies(actor["id"])

    elements = build_actor_movie_graph(actor, movies)

    return elements

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
            style={'width': '150px', 'height': '225px'}
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

    months = []
    days = []
    values = []

    for key, count in date_counts.items():
        month, day = key.split("-")

        months.append(int(month))
        days.append(int(day))
        values.append(count)

    #build grid-style heatmap (proper calendar feel)
    figure = go.Figure(data=go.Heatmap(
        x=days,
        y=months,
        z=values,
        colorscale="Plasma",
        hovertemplate=
        "Day: %{x}<br>" +
        "Month: %{y}<br>" +
        "Releases: %{z}<extra></extra>"
    ))

    #mapping numerical values for months to their actual names for more readable plot
    month_map = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    figure.update_layout(
        title="Heatmap of Upcoming Movie Releases",
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font_color='white',

        xaxis_title="Day of Month",
        yaxis_title="Month",

        #ordering months backwards so that they dislpay properly on the dashboard
        yaxis=dict(
        type="category",
        categoryorder="array",
        categoryarray=[12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        tickvals=list(month_map.keys()),
        ticktext=list(month_map.values())
    ),

        title_x=0.5,
        height=450
    )

    return figure

if __name__ == '__main__':
    app.run(debug=True)
