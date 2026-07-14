import branca
import folium
import pandas as pd
import streamlit
from bairros import bairros_coordenadas
from folium.plugins import Geocoder, OverlappingMarkerSpiderfier
from streamlit_folium import st_folium


def parse_ods(texto):
    """Separa a coluna 'ods' (lista separada por ';') nos ODS individuais."""
    if pd.isna(texto):
        return []
    return [ods.strip() for ods in texto.split(";") if ods.strip()]


# Obs: Os ícones vem do Glyphicons ou do Font Awesome, o Font Awesome precisa de prefix="fa"

# Configuração da página: layout largo para o mapa aproveitar a tela
streamlit.set_page_config(page_title="Extensão em São João del-Rei", layout="wide")

# Lê o CSV e monta o dataframe
df = pd.read_csv('acoes_extensao_coordenadas.csv')

streamlit.title("Extensão em São João del-Rei")

# Filtros do Streamlit
streamlit.sidebar.header("Filtros")

bairros_selecionados = streamlit.sidebar.multiselect(
    "Bairro",
    options=sorted(df['bairro_grupo'].dropna().unique(), key=str.lower),
    placeholder="Selecione um ou mais bairros",
)

unidades_selecionadas = streamlit.sidebar.multiselect(
    "Unidade Proponente",
    options=sorted(df['unidade_proponente'].dropna().unique(), key=str.lower),
    placeholder="Selecione uma ou mais unidades",
)

areas_selecionadas = streamlit.sidebar.multiselect(
    "Área Principal",
    options=sorted(df['area_principal'].dropna().unique(), key=str.lower),
    placeholder="Selecione uma ou mais áreas",
)

ods_disponiveis = sorted(
    {ods for lista in df['ods'].dropna().map(parse_ods) for ods in lista},
    key=lambda o: int(o.split(" - ")[0]),
)
ods_selecionados = streamlit.sidebar.multiselect(
    "ODS",
    options=ods_disponiveis,
    placeholder="Selecione um ou mais ODS",
)

if bairros_selecionados:
    df = df[df['bairro_grupo'].isin(bairros_selecionados)]

if unidades_selecionadas:
    df = df[df['unidade_proponente'].isin(unidades_selecionadas)]

if areas_selecionadas:
    df = df[df['area_principal'].isin(areas_selecionadas)]

if ods_selecionados:
    selecionados = set(ods_selecionados)
    df = df[df['ods'].map(lambda t: bool(selecionados & set(parse_ods(t))))]

# Cria o mapa
m = folium.Map(location=(-21.1311, -44.2588), zoom_start=12, min_zoom=12, tiles="OpenStreetMap")

# Botão de tela cheia
folium.plugins.Fullscreen(
    position="topleft",
    force_separate_button=False,
).add_to(m)

# Markers
for _, acao in df.iterrows():
    equipe_lista = acao['equipe'].split(";")

    ods_lista = parse_ods(acao['ods'])

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

        <p><strong>Unidade Proponente:</strong><br>
            {acao['unidade_proponente']}
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
    ).add_to(m)

# OverlappingMarkerSpiderfier
oms = OverlappingMarkerSpiderfier()
oms.add_to(m)

# Renderiza o mapa
st_folium(m, use_container_width=True, height=600)