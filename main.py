import branca
import folium
import streamlit
from folium.plugins import Geocoder, MousePosition
from streamlit_folium import st_folium

# Obs: Os ícones vem do Glyphicons ou do Font Awesome, o Font Awesome precisa de prefix="fa"

m = folium.Map(location=(-21.1388, -44.2588), zoom_start=15, tiles="OpenStreetMap")

# Barra de pesquisa

folium.plugins.Geocoder().add_to(m)

# Posição do mouse

MousePosition().add_to(m)

# Botão de tela cheia

folium.plugins.Fullscreen(
    position="topleft",
    force_separate_button=False,
).add_to(m)

# Ajusta o zoom de acordo com o que foi marcado no LayerControl

folium.FitOverlays().add_to(m)

# Grupo de markers e LayerControl

group = folium.FeatureGroup("group").add_to(m)

html = """
<div style="font-family: Arial, sans-serif; font-size: 14px; max-height: 280px; overflow-y: auto;">

    <h2 style="color:#2c3e50; margin-bottom:5px;">
        Observatório da Saúde Coletiva: Cuidando de quem cuida
    </h2>

    <p><strong>Tipo:</strong>
        Programa
    </p>

    <p><strong>Departamento do Proponente:</strong><br>
        Departamento de Geociências 
    </p>

    <p><strong>Coordenador:</strong><br>
        Marcio Roberto Toledo
    </p>

    <p><strong>Equipe:</strong><br>
        Marcio Roberto Toledo<br>
        Cassia Beatriz Batista e Silva<br>
        Tais de Lacerda Gonçalves<br>
        Amanda Valiengo<br>
        Carolina Ribeiro Xavier
    </p>

    <p><strong>Área Principal:</strong><br>
        Saúde
    </p>

    <p><strong>ODS Relacionados:</strong><br>
        3 - Saúde e Bem-Estar
    </p>

    <p><strong>Período de Realização:</strong><br>
        01/04/2024 a 31/03/2026 
    </p>

    <p><strong>Local de Realização:</strong><br>
        Praça Dom Helvécio, Dom Bosco, São João del-Rei, MG
    </p>

</div>
"""

iframe = branca.element.IFrame(html=html, width='500', height='300')

popup = folium.Popup(iframe, max_width=500)

folium.Marker(
    location=[-21.1388, -44.2588],
    # tooltip="Observatório da Saúde Coletiva: Cuidando de quem cuida",
    popup=popup,
    lazy=True,
    icon=folium.Icon(icon="university", prefix="fa", color="blue"),
).add_to(group)

folium.LayerControl().add_to(m)

streamlit.title("Extensão em São João del-Rei")
st_folium(m, width=700, height=500)

# Plugin GroupedLayerControl?
# Plugin OverlappingMarkerSpiderfier?
# Plugin TagFilterButton?
# Plugin TreeLayerControl?
