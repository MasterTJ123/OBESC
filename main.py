import branca
import folium
import pandas as pd
import streamlit as st
from bairros import bairros_coordenadas
from folium.plugins import Fullscreen, OverlappingMarkerSpiderfier
from streamlit_folium import st_folium

# Obs: Os ícones vêm do Glyphicons ou do Font Awesome; o Font Awesome precisa de prefix="fa".

CSV_ACOES = "acoes_extensao_coordenadas.csv"
MAPA_CENTRO = (-21.1311, -44.2588)
MAPA_ZOOM = 12

# Filtros de colunas com um valor por linha: (rótulo, coluna, placeholder).
FILTROS_SIMPLES = [
    ("Bairro", "bairro_grupo", "Selecione um ou mais bairros"),
    ("Unidade Proponente", "unidade_proponente", "Selecione uma ou mais unidades"),
    ("Área Principal", "area_principal", "Selecione uma ou mais áreas"),
]


def parse_ods(texto):
    """Separa a coluna 'ods' (lista separada por ';') nos ODS individuais."""
    if pd.isna(texto):
        return []
    return [ods.strip() for ods in texto.split(";") if ods.strip()]


@st.cache_data
def carregar_dados():
    """Lê o CSV das ações de extensão (cacheado entre reruns)."""
    return pd.read_csv(CSV_ACOES)


def aplicar_filtros(df):
    """Desenha os filtros na sidebar e devolve o dataframe filtrado.

    Convenção: filtro vazio não filtra (mostra tudo). Filtros diferentes
    combinam com E (todas as condições ao mesmo tempo).
    """
    st.sidebar.header("Filtros")

    selecoes = {}
    for label, coluna, placeholder in FILTROS_SIMPLES:
        selecoes[coluna] = st.sidebar.multiselect(
            label,
            options=sorted(df[coluna].dropna().unique(), key=str.lower),
            placeholder=placeholder,
        )

    ods_disponiveis = sorted(
        {ods for lista in df["ods"].dropna().map(parse_ods) for ods in lista},
        key=lambda o: int(o.split(" - ")[0]),
    )
    ods_selecionados = st.sidebar.multiselect(
        "ODS",
        options=ods_disponiveis,
        placeholder="Selecione um ou mais ODS",
    )

    for coluna, escolhidos in selecoes.items():
        if escolhidos:
            df = df[df[coluna].isin(escolhidos)]

    if ods_selecionados:
        selecionados = set(ods_selecionados)
        df = df[df["ods"].map(lambda t: bool(selecionados & set(parse_ods(t))))]

    return df


def construir_popup(acao):
    """Monta o HTML do popup de uma ação."""
    equipe_lista = acao["equipe"].split(";")
    ods_lista = parse_ods(acao["ods"])

    enderecos_lista = []
    for endereco in acao["endereco"].split(";"):
        partes = endereco.split(",")
        bairro, cidade, estado = partes[0], partes[1], partes[2]
        if bairro == "":
            enderecos_lista.append(f"{cidade}, {estado}")
        else:
            enderecos_lista.append(f"{bairro}, {cidade}, {estado}")

    return f"""
    <div style="font-family: Arial, sans-serif; font-size: 14px; max-height: 280px; overflow-y: auto;">

        <h2 style="color:#2c3e50; margin-bottom:5px;">
            {acao['titulo']}
        </h2>

        <p><strong>Tipo:</strong><br>
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


def construir_mapa(df):
    """Cria o mapa Folium com um marcador por ação."""
    m = folium.Map(
        location=MAPA_CENTRO,
        zoom_start=MAPA_ZOOM,
        min_zoom=MAPA_ZOOM,
        tiles="OpenStreetMap",
    )

    Fullscreen(position="topleft", force_separate_button=False).add_to(m)

    for _, acao in df.iterrows():
        iframe = branca.element.IFrame(html=construir_popup(acao), width="500", height="300")
        popup = folium.Popup(iframe, max_width=500)
        folium.Marker(
            location=bairros_coordenadas[acao["bairro_grupo"]],
            popup=popup,
            lazy=True,
            icon=folium.Icon(icon="university", prefix="fa", color="blue"),
        ).add_to(m)

    OverlappingMarkerSpiderfier().add_to(m)
    return m


st.set_page_config(page_title="Extensão em São João del-Rei", layout="wide")
st.title("Extensão em São João del-Rei")

df = carregar_dados()
df = aplicar_filtros(df)
st_folium(construir_mapa(df), use_container_width=True, height=600)
