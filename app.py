from dash import Dash, html, dcc, callback, Output, Input
from ingestion import fetch_popular

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
    
    #most popular movie right now
    html.Div(id="movie-card")
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

if __name__ == '__main__':
    app.run(debug=True)
