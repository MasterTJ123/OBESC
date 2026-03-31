import branca
import folium
import pandas as pd
import streamlit
from bairros import bairros_coordenadas
from folium.plugins import Geocoder, OverlappingMarkerSpiderfier, TagFilterButton
from streamlit_folium import st_folium

# Obs: Os ícones vem do Glyphicons ou do Font Awesome, o Font Awesome precisa de prefix="fa"

# Lê o CSV e monta o dataframe
df = pd.read_csv('acoes_extensao_coordenadas.csv')

# Cria o mapa
m = folium.Map(location=(-21.1311, -44.2588), zoom_start=12, min_zoom=12, tiles="OpenStreetMap")

# Botão de tela cheia
folium.plugins.Fullscreen(
    position="topleft",
    force_separate_button=False,
).add_to(m)

# Grupos e Markers
groups = list(bairros_coordenadas.keys())

for _, acao in df.iterrows():
    equipe_lista = acao['equipe'].split(",")

    ods_lista = acao['ods'].split(",")

    enderecos_lista = []
    enderecos = acao['endereco'].split(";")
    for endereco in enderecos:
        endereco_split = endereco.split(",")
        bairro = endereco_split[0]
        cidade = endereco_split[1]
        estado = endereco_split[2]
        if bairro == "":
            enderecos_lista.append(f"{cidade}, {estado}")
        else:
            enderecos_lista.append(f"{bairro}, {cidade}, {estado}")

    html = f"""
    <div style="font-family: Arial, sans-serif; font-size: 14px; max-height: 280px; overflow-y: auto;">

        <h2 style="color:#2c3e50; margin-bottom:5px;">
            {acao['titulo']}
        </h2>

        <p><strong>Tipo:</strong>
            {acao['tipo']}
        </p>

        <p><strong>Departamento do Proponente:</strong><br>
            {acao['departamento_proponente']}
        </p>

        <p><strong>Coordenador:</strong><br>
            {acao['coordenador']}
        </p>

        <p><strong>Equipe:</strong><br>
            {"<br>".join(equipe_lista)}
        </p>

        <p><strong>Área Principal:</strong><br>
            {acao['area_principal']}
        </p>

        <p><strong>ODS Relacionados:</strong><br>
            {"<br>".join(ods_lista)}
        </p>

        <p><strong>Período de Realização:</strong><br>
            {acao['periodo_realizacao']}
        </p>

        <p><strong>Local de Realização:</strong><br>
            {"<br>".join(enderecos_lista)}
        </p>

    </div>
    """

    iframe = branca.element.IFrame(html=html, width='500', height='300')
    popup = folium.Popup(iframe, max_width=500)

    folium.Marker(
        location=bairros_coordenadas[acao['bairro_grupo']],
        popup=popup,
        lazy=True,
        icon=folium.Icon(icon="university", prefix="fa", color="blue"),
        tags=[acao['bairro_grupo']]
    ).add_to(m)

# OverlappingMarkerSpiderfier
oms = OverlappingMarkerSpiderfier()
oms.add_to(m)

# TagFilterButton
TagFilterButton(data=groups, clear_text="Limpar").add_to(m)

# Streamlit
streamlit.title("Extensão em São João del-Rei")
st_folium(m, width=700, height=500)