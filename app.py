from dash import Dash, dcc, html, Input, Output, callback 
import base64
from dash.dependencies import Input, Output, State
import pandas as pd
import folium
from keplergl import *
import dash
import dash_bootstrap_components as dbc
import geopandas as gpd
import folium
from folium import plugins
from fun_style import * 

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP], suppress_callback_exceptions = True) 

sidebar = html.Div(
    [
        html.Div(
            children = [
                html.Img(src = "/assets/Logo.PNG", height = 150, style = {"width": "100%"}),
            ]
        ),
        html.Hr(),
        html.Div([
            dbc.Button("Limpiar filtros", outline = True, id = "f5-button", color = "primary", className = "me-1", n_clicks = 0),
                    ], className = "d-grid gap-2"),
        html.Hr(),
        html.H3('Clasificación',                                                
            style = CONTENT_BOX_TITLES ),        
        html.Div(
                dcc.Checklist(
                    id = "classification",
                    options = [
                        {'label': 'Bares', 'value': 'Bares'},
                        {'label': 'Centros nocturnos', 'value': 'Centros nocturnos'},                        
                    ],
                    inputStyle = {'margin-right': '4px'},                      
                ),
                style = {
                    'background-color': '#F1F2F2',
                    'border-radius': '15px',
                    'margin': '5px',
                    'padding': '7px',
                    'position': 'relative',
                    'overflow-y': 'auto',
                },
            ),         
        html.Hr(),
        html.H3('Alcaldía',                
                style = CONTENT_BOX_TITLES 
                    ),
        dcc.Dropdown(id = "alcaldias",                     
            options = [
                {'label': 'AZCAPOTZALCO', 'value': 'AZCAPOTZALCO'},
                {'label': 'ÁLVARO OBREGÓN', 'value': 'ÁLVARO OBREGÓN'},
                {'label': 'BENITO JUÁREZ', 'value': 'BENITO JUÁREZ'},
                {'label': 'COYOACÁN', 'value': 'COYOACÁN'},
                {'label': 'CUAJIMALPA', 'value': 'CUAJIMALPA'},
                {'label': 'CUAUHTÉMOC', 'value': 'CUAUHTÉMOC'},
                {'label': 'GUSTAVO A. MADERO', 'value': 'GUSTAVO A. MADERO'},
                {'label': 'IZTACALCO', 'value': 'IZTACALCO'},
                {'label': 'IZTAPALAPA', 'value': 'IZTAPALAPA'},
                {'label': 'MAGDALENA CONTRERAS', 'value': 'MAGDALENA CONTRERAS'},
                {'label': 'MIGUEL HIDALGO', 'value': 'MIGUEL HIDALGO'},
                {'label': 'MILPA ALTA', 'value': 'MILPA ALTA'},
                {'label': 'TLÁHUAC', 'value': 'TLÁHUAC'},
                {'label': 'TLALPAN', 'value': 'TLALPAN'},
                {'label': 'VENUSTIANO CARRANZA', 'value': 'VENUSTIANO CARRANZA'},
                {'label': 'XOCHIMILCO', 'value': 'XOCHIMILCO'},
            ],multi = True,
            placeholder = "Seleccione el tipo de capa",
        ),     
        html.Hr(),
        html.H3('Colonia',
                style = CONTENT_BOX_TITLES),                
        html.Div([
            dcc.Dropdown(
                id = "colonia-dropdown",
                multi = True,
                placeholder = "Ingrese una colonia",
                style = {
                        'width': '275px',  
                        'height': '40px', 
                        'margin': '0 auto',
                    }
            ),
        ]),
        html.Hr(),        
        html.H3('Capas',                                    
                    style = CONTENT_BOX_TITLES),
        dcc.Dropdown(id = "capas",                                         
                    options = [
                        {'label': 'Satelite', 'value': '6'},
                        {'label': 'Dark', 'value': '4'},
                        {'label': 'Positron', 'value': '2'},
                        {'label': 'StreetMap', 'value': '1'},                                    
                        {'label': 'Metro CDMX', 'value': '5'},                                    
                        {'label': 'Google', 'value': '7'},
                        ],
                    placeholder = "Seleccione el tipo de capa",
                ),
        html.Hr(),                                                
        html.H3('Poligonos',
                style = CONTENT_BOX_TITLES),                              
        dcc.Dropdown(id = "poligonos-carga", 
            options = [
                    {'label': 'Alcaldía', 'value': 'Alcal'},
                    {'label': 'Colonia', 'value': 'Colonia'},
                    
                ],multi = True,
                placeholder = "Seleccione uno o más póligonos"
                ),
        html.Hr(),
        html.Div(
            children = [                        
                html.Div([
                    dbc.Button(
                    "Descargue el mapa en HTML",
                    id = "open-lg",

                    outline = True,
                    color = "primary",
                    n_clicks = 0,
                    ),
                ],className = "d-grid"),                
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Mapa HTML")),
                        dbc.ModalBody(
                        "Deberá presionar el botón \"Generar archivo HTML\" cada vez que haya realizado una actualización en algún filtro del mapa principal. Luego podrá descargar el archivo a través del enlace generado en la sección \"Descargue el mapa\"."
                        ),                         
                        html.Hr(),
                        html.Div([
                            dbc.Button("Genere archivo HTML", outline = True, id = "btn_map", color = "primary", className = "me-1", n_clicks = 0),
                                    ], className = "d-grid gap-2 col-6 mx-auto"),
                        html.Hr(),
                        html.Div([
                            html.A('Descargue el mapa', id = 'download-map', download = 'mapa.html', target = '_blank'),
                        ], className = "d-grid gap-2 col-6 mx-auto"),
                        
                        html.Hr(),
                    ],
                    id = "modal-lg",
                    size = "sm",
                    is_open = False,
                    keyboard = False,
                    backdrop = "static",
                ),                                                     
            ],
        ),
    ],style = SIDEBAR_STYLE,
)

@callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([            
            html.Div(
                children=[                        
                    html.Div(
                        style = {
                            'background-color': '#FFFFFF',
                            'margin': '15px',
                            'padding': '0px', 
                            'position': 'relative',
                            'box-shadow': '4px 4px 4px 4px lightgrey',
                            'width': '100vw',
                            'height': '55vh'
                        },
                        children = [
                            html.Div(id = 'right-column_map'),                            
                        ]
                    )            
                ],
                style = CONTENT_STYLE 
            ),               
        ])

app.layout = html.Div([sidebar,                       
                       html.Div([
                            dcc.Tabs(id = "tabs-styled-with-inline", value = 'tab-1', children = [
                                dcc.Tab(label = 'CONSUMO DE ALCOHOL', value = 'tab-1', style = style_tabs, selected_style = tab_selected_style),
                                dcc.Tab(label = 'VENTA DE ALCOHOL', value = 'tab-2', style = style_tabs, selected_style = tab_selected_style),
                            ], style = CONTENT_STYLE,
                                    ),  
                            html.Div(id = 'tabs-content-inline'),    
                        ])
                ])

@app.callback(
    Output('right-column_map', 'children'),
    [Input('alcaldias', 'value'), 
     Input('classification', 'value'),    
     Input('capas', 'value'),
     Input('poligonos-carga','value'), 
     Input('colonia-dropdown','value'),    
     ]     
)
def generate_map(selected_location,selected_classification,
                 selected_capas,poli,selected_colonia):    
    data = pd.read_csv("assets/BASES/BASE.csv", encoding = 'latin-1',  low_memory = False)

    if selected_location is None:
        selected_location = []
    if selected_location:
        data = data[data['municipio'].isin(selected_location)]
    if selected_classification is None:
        selected_classification = []
    if selected_classification:
        data = data[data['nombre_act'].isin(selected_classification)]

    if selected_colonia is None:
        selected_colonia = [] 
    if selected_colonia:
        data = data[data['nomb_asent'].isin(selected_colonia)]

    if selected_capas == "1":
        m = folium.Map(tiles="OpenStreetMap")
    elif selected_capas == "2":
        m = folium.Map(tiles="Cartodb Positron")
    elif selected_capas == "4":
        m = folium.Map(tiles="Cartodb dark_matter")
    elif selected_capas == "5":
        m = folium.Map()
        opnvkarte_layer = folium.TileLayer(
            tiles='https://tileserver.memomaps.de/tilegen/{z}/{x}/{y}.png',
            max_zoom = 18,
            attr = 'Map <a href="https://memomaps.de/">memomaps.de</a> <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            name = 'OPNVKarte',
            overlay = True,
            control = True,
            )
        opnvkarte_layer.add_to(m)
    elif selected_capas == "6":
        m = folium.Map()
        esri_world_imagery_layer = folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            name = 'Esri World Imagery',
            overlay = True,
            control = True
            )
        esri_world_imagery_layer.add_to(m)
    elif selected_capas == "7":
        m = folium.Map()
        folium.raster_layers.TileLayer(
            tiles = "http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attr = "google",
            subdomains = ["mt0", "mt1", "mt2", "mt3"],
            overlay = False,
            control = True,
        ).add_to(m)
    else:
        m = folium.Map(tiles = "Cartodb Positron")

    if poli is not None and len(poli) > 0:

        if 'Colonia' in poli:
            shapefile_path_03 = 'assets/Poligonos/colonias.shp'
            gdf_03 = gpd.read_file(shapefile_path_03)

            if len(selected_colonia) > 0:
                alcaldias_gdf_03 = gdf_03[gdf_03['NOM_ASENTA'].isin(selected_colonia)]
            else:
                if selected_location is None or selected_location == []:
                    alcaldias_gdf_03 = gdf_03
                else:
                    alcaldias_gdf_03 = gdf_03[gdf_03['NOM_MUNICI'].isin(selected_location)]

            for idx, row in alcaldias_gdf_03.iterrows():
                sector = row['NOM_ASENTA']
                geojson_data_03 = row.geometry.__geo_interface__
                folium.GeoJson(geojson_data_03, name = sector, style_function = style_COLONIAS).add_to(m)
        
        if 'Alcal' in poli:
            shapefile_path = 'assets/Poligonos/alcaldias.shp'
            gdf = gpd.read_file(shapefile_path)

            if selected_location is None or selected_location == []:
                alcaldias_gdf = gdf
            if selected_location:
                alcaldias_gdf = gdf[gdf['ALCALDIA'].isin(selected_location)]
            
            for idx, row in alcaldias_gdf.iterrows():
                alcaldia = row['ALCALDIA']
                geojson_data = row.geometry.__geo_interface__
                folium.GeoJson(geojson_data, name=alcaldia,style_function=style_alcaldias).add_to(m)                
 
    camras_count = dict(data['nombre_act'].value_counts())

    for index, row in data.iterrows():
        longitude = row['longitud']
        latitude = row['latitud']

        especialidad = row['nombre_act']
        id_bct_o = row['nom_estab']
        web_df = row['www_2']



        ## Add these columns using the R program "API.r".
        #imagen_url = row['IMAGEN ']  
        #link_url = row['MAPS']  
        color = tipo_poste_colors.get(especialidad, 'gray')

        popup_content = f'<a href="{link_url}" target="_blank">' \
                        f'<img src="{imagen_url}" alt="{especialidad}" width="200" height="150"></a><br>' \
                        f'Clasificación: {especialidad}<br>' \
                        f'Nom. establecimiento: {id_bct_o}<br>'\
                        f'Sitio Web: <a href="{web_df}" target="_blank">{web_df}</a><br>'
        
        tooltip_content = f'Clasificación: {especialidad}<br>' \
                         f'Nom. establecimiento: {id_bct_o}<br>'\
                         f'Sitio Web: <a href="{web_df}" target="_blank">{web_df}</a><br>'

        folium.CircleMarker(
            [latitude, longitude],
            radius = 4,
            color = color,
            fill = True,
            fill_opacity = 1,
            weight = 1,
            popup = folium.Popup(tooltip_content, max_width = 300),
            tooltip = folium.Tooltip(tooltip_content),
        ).add_to(m)

    legend_html = '<div style="position: fixed; bottom: 20px; left: 20px; width: 250px; height: auto; background-color: white; z-index: 9999; padding: 10px; border: 2px solid grey;">' \
                '<table style="width:100%;">' \
                '<tr><th>Clasificación</th><th>Cantidad </th></tr>'

    for camra_type, count in camras_count.items():
        color = tipo_poste_colors.get(camra_type, 'gray')
        legend_html += f'<tr><td><span style="background-color:{color}; padding: 6px; border-radius: 50%; display: inline-block;"></span> {camra_type}</td><td>{count}</td></tr>'

    legend_html += '</table></div>'
    m.get_root().html.add_child(folium.Element(legend_html))
    
    plugins.Fullscreen(
        position = "topright",
        title = "Expand me",
        title_cancel = "Exit me",
        force_separate_button = True,
    ).add_to(m)

    sw = data[['latitud', 'longitud']].min().values.tolist()
    ne = data[['latitud', 'longitud']].max().values.tolist()
    m.fit_bounds([sw, ne])
    
    map_html = m.get_root().render()
    return html.Iframe(srcDoc = map_html, style = {'width': '100%', 'height': '600px'})

@app.callback(
    Output('download-map', 'href'),  
    Input('btn_map', 'n_clicks'),
    State('alcaldias', 'value'),
    State('classification', 'value'),
    State('capas', 'value'), 
    State('poligonos-carga','value'), 
    State('colonia-dropdown','value'),
    prevent_initial_call=True,
)
def download_map(n_clicks,selected_location,selected_classification,  
                 selected_capas,poli,selected_colonia):
    
    map_iframe = generate_map(selected_location,selected_classification,
                 selected_capas,poli,selected_colonia)
    map_html = map_iframe.srcDoc
    encoded_map = base64.b64encode(map_html.encode()).decode()
    href = f"data:text/html;charset=utf-8;base64,{encoded_map}"

    if n_clicks:
        return href

    return dash.no_update

def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open
app.callback(
    Output("modal-lg", "is_open"),
    Input("open-lg", "n_clicks"),
    State("modal-lg", "is_open"),
)(toggle_modal)

@app.callback(
    [Output('alcaldias', 'value'), 
     Output('classification', 'value'),    
     Output('capas', 'value'), 
     Output('poligonos-carga','value'), 
     Output('colonia-dropdown','value'),      
     ], 
    Input("f5-button", "n_clicks"),
    prevent_initial_call=True,
)
def redirect_to_self(n):
    selected_location = []
    selected_classification = []
    selected_colonia = []
    selected_capas = []
    poli = []
    return (selected_location,selected_classification,
                 selected_capas,poli,selected_colonia)

@app.callback(
    Output("colonia-dropdown", "options"),
    Input("alcaldias", "value")     
)
def update_sector_dropdown_02(selected_location):
    data = pd.read_csv("assets/BASES/BASE.csv", encoding='latin-1', low_memory=False)

    if selected_location is None or selected_location == []:
        unique_colonias = data['nomb_asent'].unique()
    else:
        data = data[data['municipio'].isin(selected_location)]
 
        unique_colonias = data['nomb_asent'].unique()
    options = [{'label': colonia, 'value': colonia} for colonia in unique_colonias]
    return options

if __name__ == "__main__":
    app.run_server(debug=True, port = 9050)