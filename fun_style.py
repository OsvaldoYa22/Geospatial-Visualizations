
color_box = 'black'

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "0.5rem 1rem",
    "background-color": "#F1F2F2", 
}
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "0rem",
    "padding": "0.5rem 1rem",
    "display": "flex",  
    "flexDirection": "row", 
}
CONTENT_BOX_TITLES = {
    'height': '40px', 
    'font-size': '21px',  
    'background-color': color_box,
    'border-radius': '15px',
    'margin': '5px',
    'padding': '7px',
    'position': 'relative',
    'overflow-y': 'auto',
    'text-align': 'center', 
    'color': 'white', 
}
def style_COLONIAS(feature):
    return {
        'fillColor': None,   
        'color': '#00A322',      
        'weight': 1,           
        'fillOpacity': 0   
    }
def style_alcaldias(feature):
    return{
        'color': 'red',      
        'weight': 2.5,           
        'fillOpacity': 0,
        'dashArray': '5, 5'
    }

style_tabs = {
            'font-size': '16px', 
            'border-bottom': '1px outset #ccc',  
            'margin-bottom': '5px',  
            'backgroundColor': '#FFFFFF',  
            'color': 'black', 
            'padding': '3px'
        } 
tab_selected_style = {
    'font-size': '18px',  
    'borderTop': '2.4px solid #119DFF', 
    'borderBottom': '0px outset #d6d6d6',
    'backgroundColor': '#f8f9fa' , 
    'color': 'black', 
    'padding': '5px', 
}
tipo_colors = {
        'Bares' : '#FF0000',
        'Centros nocturnos' : '#FF6E00',
    }
