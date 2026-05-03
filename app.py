from dash import Dash, html
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

    #most popular movie right now
    html.Div([html.H2("Current Most Popular Movie"),

    html.Img(
        src=movie["poster_url"],
        style={'width': '200px'}
    ),

    html.H3(movie["title"]),

    html.P(f"Average Rating: {movie['rating']}"),

    html.P(f"Last updated: {movie['last_updated']}")
    ], 
    style={
    'backgroundColor': '#2a2a2a',
    'padding': '10px',
    'borderRadius': '6px',
    'textAlign': 'center',
    'width': '250px',
    'margin': '20px auto'
    })
])

if __name__ == '__main__':
    app.run(debug=True)
