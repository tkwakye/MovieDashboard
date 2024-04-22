import dash
from dash import dcc, html, dash_table, Input, Output
#from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

####################################################################
##################### GET THE DATA SET #############################
####################################################################
df_movies = pd.read_csv("data/cleaned_movies_data_transformed.csv")
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
# movies_per_year_genre = df_movies.groupby('release_year')[genres].sum()

movie_stats = df_moviesDT.groupby(['title', 'release_date', 'genre']).agg({'rating': ['mean', 'count']}).reset_index()
movie_stats.columns = ['Title', 'Release Year', 'Genre', 'Average Rating', 'Number of Ratings']
#######################################################################
################# SET LAYOUT FOR THE APP COMPONENTS ###################
#######################################################################
app.layout = html.Div(children=[
    html.Div([
        html.H1("Movie Analytics Console", className="mt-5 mb-4 text-center",
                style={'font-family': 'verdana', 'font-size': '45px', 'color': 'white'}),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '50px', 'backgroundColor': '#BAB0AC',
              'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),  # sets pictures of the film clappers
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),
            html.Img(src="assets/clapper.jpg", style={'height': '100px', 'width': '150px'}),
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '50px', 'backgroundColor': '#BAB0AC',
              'text-align': 'center'}),

    html.Div([
        html.H1("Top Ten And Worst Ten Rated Movies", className="mt-5 mb-4 text-center",
                style={'font-family': 'verdana', 'font-size': '30px', 'color': 'white'}),
        dcc.RadioItems( # buttons for top and worst rated movies
            id='switch-radio',
            options=[
                {'label': 'Top Rated Movies', 'value': 'top'},
                {'label': 'Worst Rated Movies', 'value': 'bottom'}
            ],
            value='top',
            labelStyle={'display': 'inline-block', 'margin-right': '20px', 'color': 'white', 'font-family': 'verdana',
                        'font-size': '15px'}
        ),
        dcc.RangeSlider( # slider for bar graph
            id='bar-graph-slider',
            min=int(df_movies['release_year'].min()),
            max=int(df_movies['release_year'].max()),
            value=[int(df_movies['release_year'].min()), int(df_movies['release_year'].max())],
            marks={year: str(year) for year in
                   range(int(df_movies['release_year'].min()), int(df_movies['release_year'].max()) + 1, 5)},
            step=1,
            className="rangeslider"
        ),
        dcc.Graph(id='top-ten-movies-bar', style={'height': '300px', 'width': '100%'}), # bar graph
        dcc.Checklist( # checklist for bar graph
            id='genre-checkboxes',
            options=[{'label': genre, 'value': genre} for genre in genres],
            value=['Action'],
            className="form-check-input",
            style={'columnCount': 3, 'color': 'white', 'font-family': 'verdana', 'font-size': '15px'}
        ),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '50px', 'backgroundColor': '#BAB0AC'}),
    html.Div([
        html.H1("Movies Genres over the Years", className="mt-5 mb-4 text-center",
                style={'font-family': 'verdana', 'font-size': '30px', 'color': 'white'}),
        html.Label("Select Genre(s):", className="font-weight-bold",
                   style={'font-family': 'verdana', 'font-size': '15px', 'color': 'white'}),
        dcc.Dropdown( # dropdown for scatterplot and heat map
            id='genre-dropdown',
            options=[{'label': genre, 'value': genre} for genre in genres],
            value=['Action'],
            multi=True,
            className="form-control"
        ),
        dcc.RangeSlider( # slider for scatterplot and heat map
            id='year-slider',
            min=int(df_movies['release_year'].min()),
            max=int(df_movies['release_year'].max()),
            value=[int(df_movies['release_year'].min()), int(df_movies['release_year'].max())],
            marks={year: str(year) for year in
                   range(int(df_movies['release_year'].min()), int(df_movies['release_year'].max()) + 1, 5)},
            step=1,
            className="rangeslider"),
        dcc.Graph(id='movies-scatter-plot', style={'height': '300px', 'width': '50%', 'display': 'inline-block'}), # scatterplot
        dcc.Graph(id='movies-heatmap', style={'height': '300px', 'width': '50%', 'display': 'inline-block'}), # heatmap
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '50px', 'backgroundColor': '#BAB0AC'}),
    html.Div([
        html.H1("Movie Statistics", className="mt-5 mb-4 text-center",
                style={'font-family': 'verdana', 'font-size': '30px', 'color': 'white'}),
        dash_table.DataTable(
            id='movie-stats-table', # make movie stat table
            columns=[{"name": i, "id": i} for i in movie_stats.columns],
            data=movie_stats.to_dict('records'),
            page_size=10,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            style_table={'overflowX': 'auto'},
        ),
        html.Button('Reset Filters', id='reset-button', n_clicks=0), # make button for reseting data table
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '50px', 'backgroundColor': '#BAB0AC'}),
    html.Div([
        html.A(
            href="https://github.com/tkwakye/MovieRatingsDashboard", # github link
            children=[
                html.Img(
                    src="assets/git.png", style={'height': '60px', 'width': '60px'},
                )
            ],
            style={'position': 'fixed', 'bottom': '20px', 'right': '20px'}
        )

    ])

], style={})

#####################################################################
###################### CREATE SCATTERPLOTC###########################
#####################################################################
@app.callback(
    Output('movies-scatter-plot', 'figure'),
    [Input('genre-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_scatter_plot(selected_genres, selected_years):
    filtered_movies = df_movies[df_movies['genre'].isin(selected_genres) &
                                (df_movies['release_year'] >= selected_years[0]) &
                                (df_movies['release_year'] <= selected_years[1])]

    movies_per_year_genre_filtered = filtered_movies.groupby(['release_year', 'genre']).size().reset_index(name='count')

    fig = px.scatter(
        movies_per_year_genre_filtered,
        x='release_year',
        y='count',
        color='genre',
        title='Number of Movies Released Over the Years by Genre',
        labels={'release_year': 'Year', 'count': 'Number of Movies Released'},
    )

    fig.update_traces(marker=dict(size=8), selector=dict(mode='markers'))

    fig.update_layout(
        plot_bgcolor='#BAB0AC',
        font=dict(color='#424242'),
        xaxis=dict(title='Year'),
        yaxis=dict(title='Number of Movies Released')

    )

    return fig
#####################################################################
###################### CREATE HEATMAP ###############################
#####################################################################

@app.callback(
    Output('movies-heatmap', 'figure'),
    [Input('genre-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_heatmap(selected_genres, selected_years):
    filtered_movies = df_movies[df_movies['genre'].isin(selected_genres) &
                                (df_movies['release_year'] >= selected_years[0]) &
                                (df_movies['release_year'] <= selected_years[1])]

    pivot_df = filtered_movies.pivot_table(index='release_year', columns='genre', aggfunc='size', fill_value=0)
    print("Data type of 'release_year' column:")
    print(filtered_movies['release_year'].dtype)

    print("\nData type of 'selected_years' variable:")
    print(type(selected_years[0]))
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Genre", y="Release Year", color="Number of Movies"),
        title="Number of Movies Released Over the Years by Genre",
        color_continuous_scale='blues'
    )

    fig.update_layout(
        plot_bgcolor='#BAB0AC',
        font=dict(family='Arial', size=12, color='black'),
        yaxis=dict(tickfont=dict(size=10)),
    )

    return fig
#####################################################################
###################### CREATE BAR GRAPH #############################
#####################################################################

@app.callback(
    Output('top-ten-movies-bar', 'figure'),
    [Input('genre-checkboxes', 'value'),
     Input('bar-graph-slider', 'value'),
     Input('switch-radio', 'value')]
)
def update_top_ten_movies_bar(selected_genres, selected_years, selected_radio):
    if selected_radio == 'top':
        top_n = 10
        order = True
    else:
        top_n = 10
        order = False

    df_moviesDT['release_date'] = pd.to_datetime(df_moviesDT['release_date'])

    filtered_movies = df_moviesDT[(df_moviesDT['genre'].isin(selected_genres)) &
                                  (df_moviesDT['release_date'].dt.year >= selected_years[0]) &
                                  (df_moviesDT['release_date'].dt.year <= selected_years[1])]

    top_movies = (filtered_movies.groupby('title')['rating']
                  .mean()
                  .nlargest(top_n, keep='all' if order else 'first')
                  if order else
                  filtered_movies.groupby('title')['rating']
                  .mean()
                  .nsmallest(top_n, keep='all' if order else 'first'))

    fig = go.Figure()
    genre_colors = px.colors.qualitative.Set3[:len(selected_genres)]

    for i, genre in enumerate(selected_genres):
        genre_movies = top_movies[top_movies.index.isin(filtered_movies[filtered_movies['genre'] == genre]['title'])]
        fig.add_trace(go.Bar(
            x=genre_movies.index,
            y=genre_movies.values,
            name=genre,
            marker=dict(color=genre_colors[i])
        ))
    fig.update_layout(
        xaxis=dict(title='Movies'),
        yaxis=dict(title='Average Rating'),
        plot_bgcolor='#BAB0AC',
        font=dict(color='#424242'),
    )
    return fig
#####################################################################
###### CREATE DATA TABLE RESET BUTTON ###############################
#####################################################################

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