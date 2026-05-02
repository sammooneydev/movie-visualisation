from dash import Dash, html

app = Dash()

app.layout = html.Div([

    #application header
    html.Div([
        html.H1(
            'TMDB Visualisation Dashboard',
            style={'textAlign': 'center'}
        )
    ]),

    #content could go here (undecided)
    html.Div([])
])

if __name__ == '__main__':
    app.run(debug=True)
