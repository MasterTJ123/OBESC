import pandas as pd
from bairros import bairros_grupos, bairros_coordenadas

# Lê o CSV e monta o dataframe
df = pd.read_csv('acoes_extensao.csv')

# Encontra as coordenadas de acordo com o bairro
df['coordenada'] = None

for index, row in df.iterrows():
    bairro = row["endereco"].split(";")[0].split(",")[0]
    bairro_grupo = bairros_grupos[bairro]
    coordenada = bairros_coordenadas[bairro_grupo]
    df.at[index, 'bairro_grupo'] = bairro_grupo
    df.at[index, 'coordenada'] = coordenada

print("Coordenadas geradas com sucesso!")

df.to_csv('acoes_extensao_coordenadas.csv', index=False)

print("CSV gerado com sucesso!")