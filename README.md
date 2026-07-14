# OBESC

Projeto de extensão da UFSJ que permite localizar, filtrar e detalhar as
atividades de extensão em um mapa interativo da cidade de São João del-Rei.

Os dados são coletados do SIGAA por um web scraper, enriquecidos com as
coordenadas de cada bairro e exibidos em um mapa Folium dentro de um app
Streamlit, com filtros por bairro, unidade proponente, área principal e ODS.

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) para gerenciar o ambiente

## Instalação

```bash
uv sync
uv run playwright install firefox
```

O scraper faz login no SIGAA, então crie um arquivo `.env` na raiz com as
credenciais:

```env
LOGIN=seu_login
PASSWORD=sua_senha
```

## Uso

O pipeline tem três etapas, executadas nesta ordem:

```bash
# 1. Coleta as ações do SIGAA -> acoes_extensao.csv
uv run python web_scraper.py

# 2. Adiciona bairro_grupo e coordenadas -> acoes_extensao_coordenadas.csv
uv run python coordenadas.py

# 3. Sobe o app do mapa
uv run streamlit run main.py
```

Se o passo 2 acusar um bairro não mapeado, rode `uv run python bairros.py`
para listar os bairros que ainda faltam em `bairros.py` e adicione-os ao
dicionário `bairros_grupos` (e, se for um bairro/grupo novo, a coordenada
correspondente em `bairros_coordenadas`).

## Estrutura

| Arquivo | Responsabilidade |
| --- | --- |
| `web_scraper.py` | Coleta as ações de extensão do SIGAA e gera `acoes_extensao.csv`. |
| `coordenadas.py` | Mapeia cada ação a um bairro/coordenada e gera `acoes_extensao_coordenadas.csv`. |
| `bairros.py` | Dicionários de bairros → grupo e grupo → coordenada; e um utilitário para achar bairros não mapeados. |
| `main.py` | App Streamlit com o mapa e os filtros. |

## Formato dos dados

Colunas do tipo lista usam `;` como separador (`equipe`, `ods`). O campo
`endereco` separa cada endereço por `;` e, dentro de cada um, usa `,` para
`bairro,municipio,estado`.
