import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

df_movies = pd.read_csv("data/cleaned_movies_data.csv")
df_moviesDT = pd.read_csv("data/cleaned_movies_table_data.csv")

external_stylesheets = ['MDstyle.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

genres = [
    'unknown', 'Action', 'Adventure', 'Animation', 'Children',
    'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
    'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance',
    'Sci-Fi', 'Thriller', 'War', 'Western'
]
movies_per_year_genre = df_movies.groupby('release_year')[genres].sum()
movie_stats = df_moviesDT.groupby(['title', 'release_date', 'genre']).agg({'rating': ['mean', 'count']}).reset_index()
movie_stats.columns = ['Title', 'Release Date', 'Genre', 'Average Rating', 'Number of Ratings']
movie_stats['Release Date'] = pd.to_datetime(movie_stats['Release Date'], format="%d-%b-%Y")
movie_stats['Release Date'] = movie_stats['Release Date'].dt.strftime('%Y-%m-%d')

app.layout = html.Div(children=[
    html.Div([
        html.H1("Movie Ratings Through the Years", className="mt-5 mb-4 text-center",
                style={'font-family': 'verdana', 'font-size': '20px', 'color': 'white'}),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '50px', 'backgroundColor': '#BAB0AC',
              'text-align': 'center'}),
    html.Div([
        html.H1("Top Ten Rated Movies and Their Average Ratings", className="mt-5 mb-4 text-center",
                style={'font-family': 'verdana', 'font-size': '15px', 'color': 'white'}),
        dcc.RadioItems(
            id='switch-radio',
            options=[
                {'label': 'Top Rated Movies', 'value': 'top'},
                {'label': 'Lowest Rated Movies', 'value': 'bottom'}
            ],
            value='top',
            labelStyle={'display': 'inline-block', 'margin-right': '20px'}
        ),
        dcc.RangeSlider(
            id='bar-graph-slider',
            min=int(df_movies['release_year'].min()),
            max=int(df_movies['release_year'].max()),
            value=[int(df_movies['release_year'].min()), int(df_movies['release_year'].max())],
            marks={year: str(year) for year in
                   range(int(df_movies['release_year'].min()), int(df_movies['release_year'].max()) + 1, 5)},
            step=1,
            className="rangeslider"
        ),
        dcc.Graph(id='top-ten-movies-bar', style={'height': '300px', 'width': '100%'}),
        dcc.Checklist(
            id='genre-checkboxes',
            options=[{'label': genre, 'value': genre} for genre in genres],
            value=['Action'],
            className="form-check-input",
            style={'columnCount': 3}
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '50px', 'backgroundColor': '#BAB0AC'}),
    html.Div([
        html.H1("Movies Genres over the Years", className="mt-5 mb-4 text-center",
                style={'font-family': 'verdana', 'font-size': '15px', 'color': 'white'}),
        html.Label("Select Genre(s):", className="font-weight-bold",
                   style={'font-family': 'Arial', 'font-size': '15px', 'color': 'white'}),
        dcc.Dropdown(
            id='genre-dropdown',
            options=[{'label': genre, 'value': genre} for genre in genres],
            value=['Action'],
            multi=True,
            className="form-control"
        ),
        dcc.RangeSlider(
            id='year-slider',
            min=int(df_movies['release_year'].min()),
            max=int(df_movies['release_year'].max()),
            value=[int(df_movies['release_year'].min()), int(df_movies['release_year'].max())],
            marks={year: str(year) for year in
                   range(int(df_movies['release_year'].min()), int(df_movies['release_year'].max()) + 1, 5)},
            step=1,
            className="rangeslider"),
        dcc.Graph(id='movies-scatter-plot', style={'height': '300px', 'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='movies-heatmap', style={'height': '300px', 'width': '50%', 'display': 'inline-block'}),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '50px', 'backgroundColor': '#BAB0AC'}),
    html.Div([
        html.H1("Movie Statistics Data Table", className="mt-5 mb-4 text-center",
                style={'font-family': 'verdana', 'font-size': '15px', 'color': 'white'}),
        dash_table.DataTable(
            id='movie-stats-table',
            columns=[{"name": i, "id": i} for i in movie_stats.columns],
            data=movie_stats.to_dict('records'),
            page_size=10,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            style_table={'overflowX': 'auto'},
        ),
        html.Button('Reset Filters', id='reset-button', n_clicks=0),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '50px', 'backgroundColor': '#BAB0AC'}),
], style={})


@app.callback(
    Output('movies-scatter-plot', 'figure'),
    [Input('genre-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_scatter_plot(selected_genres, selected_years):
    filtered_movies_per_year_genre = movies_per_year_genre.loc[selected_years[0]:selected_years[1]]
    filtered_movies_per_year_genre.reset_index(inplace=True)
    fig = px.scatter(
        filtered_movies_per_year_genre.reset_index(),
        x='release_year',
        y=selected_genres,

        title="",
        trendline="ols",
        labels={'release_year': 'Year', 'value': 'Number of Movies Released Per Year'}
    )
    fig.update_traces(marker=dict(size=5))
    fig.update_traces(mode='lines+markers', selector=dict(name='Trendline'))
    fig.update_layout(
        plot_bgcolor='#BAB0AC',
        font=dict(color='#424242'),
        xaxis=dict(title_font=dict(family='Arial', size=13, color='black')),
        yaxis=dict(title_font=dict(family='Arial', size=13, color='black')),
        title=""
    )
    return fig


@app.callback(
    Output('movies-heatmap', 'figure'),
    [Input('genre-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_heatmap(selected_genres, selected_years):
    filtered_movies_per_year_genre = movies_per_year_genre.loc[selected_years[0]:selected_years[1]]
    filtered_movies_per_year_genre.reset_index(inplace=True)

    pivot_df = filtered_movies_per_year_genre.pivot_table(index='release_year', values=selected_genres)

    fig = px.imshow(
        pivot_df,
        labels=dict(x="Genre", y="Release Year", color="Number of Movies"),
        title="",
        color_continuous_scale='blues'
    )

    fig.update_layout(
        plot_bgcolor='brown',
        font=dict(family='Arial', size=12, color='black'),
        yaxis=dict(tickfont=dict(size=10)),
    )

    return fig


@app.callback(
    Output('top-ten-movies-bar', 'figure'),
    [Input('genre-checkboxes', 'value'),
     Input('bar-graph-slider', 'value'),
     Input('switch-radio', 'value')]
)
def update_top_ten_movies_bar(selected_genres, selected_years, selected_radio):
    if selected_radio == 'top':
        filtered_movies = df_moviesDT[(df_moviesDT['genre'].isin(selected_genres)) &
                                      (pd.to_datetime(df_moviesDT['release_date']).dt.year >= selected_years[0]) &
                                      (pd.to_datetime(df_moviesDT['release_date']).dt.year <= selected_years[1])]
        top_ten_movies = filtered_movies.groupby('title')['rating'].mean().nlargest(10)
    else:
        filtered_movies = df_moviesDT[(df_moviesDT['genre'].isin(selected_genres)) &
                                      (pd.to_datetime(df_moviesDT['release_date']).dt.year >= selected_years[0]) &
                                      (pd.to_datetime(df_moviesDT['release_date']).dt.year <= selected_years[1])]

        top_ten_movies = filtered_movies.groupby('title')['rating'].mean().nsmallest(10)

    top_ten_movies_df = top_ten_movies.to_frame().reset_index()

    min_rating = top_ten_movies_df['rating'].min()
    max_rating = top_ten_movies_df['rating'].max()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=top_ten_movies.index, y=top_ten_movies.values,
                         marker=dict(color='rgb(158,202,225)', line=dict(color='rgb(8,48,107)', width=1.5))))
    fig.update_layout(
        xaxis=dict(title='Movies'),
        yaxis=dict(title='Average Rating'),
        yaxis_range=[min_rating - 0.3, max_rating],
        plot_bgcolor='#BAB0AC',
        font=dict(color='#424242'),
    )
    return fig


@app.callback(
    Output('movie-stats-table', 'filter_query'),
    [Input('reset-button', 'n_clicks')]
)
def reset_filters(n_clicks):
    if n_clicks > 0:
        return ''
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
