import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import os
import pathlib
plik_csv = pathlib.Path(__file__).parent / 'athlete_events.csv'


# Wczytanie pliku CSV
df = pd.read_csv(plik_csv)


#gotowy styl CSS 
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Tworzenie aplikacji Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])
load_figure_template("SLATE")

#tekst wykorzystany w app layout
tekst="Same igrzyska, choć kojarzą się z młodością, z racji wielu dyscyplin obejmują różne podejścia do sportu, a mimo nacisku na konkurencje fizyczne, szeroki jest również przekrój wieku uczestników. Najmłodszym odnotowanym uczestnikiem igrzysk olimpijskich jest Dimitrios Loundras z Grecji, który współzawodniczył w gimnastyce na pierwszych igrzyskach w 1896 r. mając 10 lat. Najmłodszą zdobywczynią złotego medalu olimpijskiego (w konkurencjach indywidualnych) jest Marjorie Gestring, reprezentantka USA w skokach do wody, zdobyła złoty medal w skokach z trampoliny na igrzyskach w Berlinie w 1936 roku (mając 13 lat i 9 miesięcy). Podobnie szeroki przekrój jest wśród masy i wzrostu zawodników (zawodniczek) – kulomioci i kulomiotki osiągając masę powyżej 140 kg i 200 cm wzrostu, z kolei inni lekkoatleci, startujący w tym samym czasie, na tym samym stadionie (zwykle olimpijskim) mają dużo mniejszą masę i wzrost – np. złota medalistka, biegaczka Florence Griffith-Joyner miała 169 cm wzrostu i ważyła 59 kg.Zwycięstwo na igrzyskach olimpijskich uznawane jest przez sportowców większości dyscyplin za najbardziej prestiżowe osiągnięcie."

#stworzenie pierwszego layoutu
layout1 = html.Div([
    html.H2('Suma zdobytych medali w zależności od kraju i roku'),
    dcc.Graph(id='choropleth1'),
    html.Label('Wybierz rok:'),
    # element interaktywny z biliotki dash - suwak
    dcc.Slider(
        id='year-slider1',
        min=1924,
        max=2020,
        value=2000,
        marks={str(year): str(year) for year in range(1924, 2020, 4)},
        step=None,
        className="dbc" 
    )
])

layout2 = html.Div([
    html.H2('Wykres dla liczby zawodników w danych latach w zależności od dyscypliny'),
    html.Label('Wybierz dyscyplinę:'),
    html.Div(
        #element interaktywny z biliotki dash - lista opcji
        dcc.Checklist(
            id="filter1",
            options=df["Sport"].unique(),
            value=["Diving","Swimming","Volleyball"],
            labelStyle={'display': 'inline-block', 'margin-right': '10px'} #żeby dyscypliny do wyboru były ułożone w linii
        ),
        style={'display': 'flex', 'flex-wrap': 'wrap'} # jeśli nie ma miejsca w linii to przesuwane do kolejnej
    ),
    html.Br(),
    dcc.Graph(id='scatter1')
])


layout3 = html.Div([
    html.H2('Wzrost u kobiet i mężczyzn, a dyscyplina'),
    html.Label('Wybierz dyscyplinę:'),
    html.Br(),
    html.Div(
        #element inteakrywny - rozwijana lista do wyboru (może być wielokrotnego wyboru)
        dcc.Dropdown( 
            id="dyscyplina1",
            options=df["Sport"].unique(),
            value=["Diving","Basketball","Volleyball","Ski Jumping"],
            multi=True, #wielokrotny wybór włączony
            className="dbc"
        ),      
    ),
    html.Br(),
    dcc.Graph(id='scatter2')
])

layout4 = html.Div([
    html.H2('Liczba zawodników w zależności od płci, narodowości, dyscypliny i roku'),
    html.Div([
        html.Label('Wpisz kraj: '),
        #element interaktywny - wpisywanie (tutaj tekstu)
        dcc.Input(id='kraj-input', type='text', value='China', className="dbc"),
    ]),
    html.Div([
        html.Label('Wybierz dyscyplinę:'),
        #element interaktywny
        dcc.Dropdown(
            id='dyscyplina-dropdown',
            options=df["Sport"].unique(),
            value='Judo', 
            className="dbc"
        ),
    ]),
    html.Div([
        html.Label('Wybierz rok:'),
        #element interaktywny
        dcc.Dropdown(
            id='year2',
            options=sorted(df["Year"].unique(), reverse=True),
            value="",
            className="dbc"
        ),
        html.Br(),
    ]),
    dcc.Graph(id='wykres-kolowy'),
])

layout5 = html.Div([
        html.Label('Wybierz dyscyplinę:'),
        #element interaktywny
        dcc.Dropdown(
            id='dyscyplina2-dropdown',
            options=df["Sport"].unique(),
            value='Volleyball', 
            className="dbc"
        ),
        html.Br(),
        dcc.Graph(id='wykres2')
])

layout6 = html.Div([
    dcc.Tabs([ #zakładki
        dcc.Tab([html.Br(),html.Br(), #pierwsza zakładka
            dbc.Row([html.Br(),
                dbc.Col(
                    #element interaktywny
                    dcc.Dropdown(
                       options=df["Team"].unique(),
                        value="Poland",
                        className="dbc",
                        id="Country3"
                    ),width=2),
                dbc.Col([
                    dbc.Row(dcc.Graph(id="tab-1"),)
                ])      
            ])
        ],label="Ilość zawodników w danym kraju"),
        dcc.Tab([html.Br(), #druga zakładka
                html.Br(),
                dbc.Row([
                dbc.Col(
                    #element interaktywny
                    dcc.RadioItems(
                        options=df["Sport"].unique(),
                        value="Swimming",
                        className="dbc",
                        id="Sport4",
                        labelStyle={'display': 'inline-block', 'margin-right': '10px'} #żeby dyscypliny do wyboru były ułożone w linii
                    ),style={'display': 'flex', 'flex-wrap': 'wrap'},width=4),
                    html.Br(),
                    html.Br(),
                dbc.Col([
                    dbc.Row(dcc.Graph(id="tab-2"),)
                ])      
            ])
    ],label="Ilość zawodników w danym sporcie")
])
], className="dbc")

#wygląd aplikacji
app.layout = dbc.Container([
    html.H1("Dashboard w Olimpiadzie", style={"text-align": "center", "font-weight": "bold"}), # tekst wyśrodkowany i pogrubiony
    html.Hr(),
    html.Br(),
    dbc.Row([ #wiersze 
        dbc.Col(layout1 ,width=12), #kolumny, layout1 o szerokości 12 (maksymalnej)
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(layout3,width=6,),
        dbc.Col(layout4,width=6),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(layout2, width=12)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(layout5,width=8),
        dbc.Col(dbc.Card(dbc.CardBody(html.Div(tekst)))) #Card - tworzy kartę (ramkę), a Cardbody jest elementem, który zawiera główną treść karty (teskt, rysunek) 
    ]),
    html.Br(),
    html.Hr(),
    html.Br(),
    dbc.Row([
        dbc.Col(layout6, width=12)
    ])
])



#pierwszy callback
@app.callback(
    Output('choropleth1', 'figure'),
    Input('year-slider1', 'value'),
)
def wykres_mapa(year): 
    #wybranie tylko wierszy z medalami i danym rokiem 
    filtr1 = df[(df['Year'] == year) & ((df['Medal'] == "Gold") | (df['Medal'] == "Silver") | (df['Medal'] == "Bronze"))]

    #porzucanie duplikatów pod względem tego samego medalu, kraju i konkurencji (z uwagi na sporty drużynowe np. siatkówka)
    bezpowt = filtr1.drop_duplicates(subset=['Year', 'Medal','Event', 'Season', 'NOC']).reset_index()
    #zliczenie liczby medali względem drużyny
    segregacja = bezpowt.groupby('NOC').size().reset_index(name='Medals')
 
    fig = px.choropleth(
        segregacja,
        locations='NOC',
        color='Medals',
        color_continuous_scale='Reds',
        hover_name='NOC',
        title='Suma zdobytych medali na Letnich Igrzyskach Olimpijskich w roku {}'.format(year)
    )
    fig.update_layout(geo=dict(showframe=False),
    height=550)
    return fig

#drugi callback
@app.callback(
    Output('scatter1', 'figure'),
    Input('filter1', 'value'),
)

def wykres_kropkowy(sport):
    #grupowanie względem sportu, roku i ID zawodnika
    df1 = df.groupby(['Sport','Year','ID']).size()
    #grupowanie względem sportu i roku, zliczenie rozmiaru i wpisanie wyniku do kolumny NO_AThletes
    grupowane = df1.groupby(['Sport','Year']).size().reset_index(name='NO_Athletes')
    #wybranie kolumn z danego sportu
    filtr2 = grupowane.query('Sport == @sport')
    fig=px.scatter(
        filtr2,
        x="Year",
        y="NO_Athletes",
        color="Sport",
        title="Liczba zawodników w danych latach w zależności od dyscypliny"
    )
    return fig


#trzeci callback
@app.callback(
    Output('scatter2', 'figure'),
    Input('dyscyplina1', 'value'),
)

def wykres_slupkowy(sport):
    #pogrupowanie względem płci i sportu i obliczenie dla tych danych średniej wzrostu
    df4=df.groupby(["Sex","Sport"])[["Height"]].mean().reset_index()
    df4 = df4.query('Sport == @sport')
    fig = px.bar(
        df4,
        x="Sport",
        y="Height",
        color="Sex",
        barmode="group",
        title="Wzrost zawodników w zależności od dyscypliny i płci"
    ).update_layout(
        legend_title={
        "text":"Płeć"
        }
    )
    return fig


#czwarty callback
@app.callback(
    Output('wykres-kolowy', 'figure'),
    Input('kraj-input', 'value'),
    Input('dyscyplina-dropdown', 'value'),
    Input('year2', 'value')
)
def wykres_kolo(kraj, dyscyplina, rok):
    #wybranie danych dotyczących danego kraju, dyscypliny i roku
    filtered_df = df[(df['Team'] == kraj) & (df['Sport'] == dyscyplina) & (df['Year'] == rok)]
    #grupowanie względem płci i ID zawodnika
    segregacja = filtered_df.groupby(['ID','Sex']).size().reset_index()
    #grupowanie względem płci i zwrócenie rozmiaru
    segr2 = segregacja.groupby("Sex").size().reset_index(name="liczba")

    fig = px.pie(
        segr2,
        values="liczba",
        names="Sex",
        title='Podział płci dla {} w {} dla roku {}'.format(dyscyplina, kraj, rok)
    )
    
    return fig

#piąty callback
@app.callback(
    Output('wykres2', 'figure'),
    Input('dyscyplina2-dropdown', 'value'),
)

def wykres_liniowy2(sport):
    #usuwanie dupliaktów (jeden zawdonik może startować kilka razy w różnych konkurencjach w tym samym roku)
    bezpowt = df.drop_duplicates(subset=['Year','ID']).reset_index()
    #grupowanie względem sportu, roku i płci i obliczenie dla tych danych średniej wagi
    df1 = bezpowt.groupby(['Sport','Year','Sex'])['Weight'].mean().reset_index(name='średnia')
    filtr2 = df1.query('Sport == @sport')
    fig=px.line(
        filtr2,
        x="Year",
        y="średnia",
        color="Sex",
        title="Średnia waga zawodników w zależności od płci i dyscypliny na przestrzeni lat"
    )
    return fig


#6 callback
@app.callback(
              Output("tab-1","figure"),
              Output("tab-2","figure"),
              Input('Country3', 'value'),
              Input('Sport4','value')
              )

def tabsy(country, sport):
    #wybrany dany kraj
    filtr1 = df.query('Team == @country')
    bezpowt = filtr1.drop_duplicates(subset=['Year', 'ID']).reset_index()
    filtr2 = bezpowt.groupby(["Year"]).size().reset_index(name='Number of Athletes')
    line = px.line(
        filtr2,
        x="Year",
        y="Number of Athletes",
        title="Liczba zawodników w danym kraju na przestrzeni lat - {}".format(country)
        )
    filtr1 = df.query('Sport == @sport')
    bezpowt = filtr1.drop_duplicates(subset=['Year', 'ID']).reset_index()
    filtr2 = bezpowt.groupby(["Year"]).size().reset_index(name='Number of Athletes')
    line1 = px.line(
        filtr2,
        x="Year",
        y="Number of Athletes",
        title="Liczba zawodników w danym sporcie na przestrzeni lat - {}".format(sport)
        )
    return line, line1

if __name__ == '__main__':
    app.run_server(debug=True)