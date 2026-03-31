bairros_grupos = {
    # Todos
    '': 'Todos',
    'não se aplica': 'Todos',
    'todos': 'Todos',
    'todos que possuem UBS': 'Todos',
    'virtualmente todos': 'Todos',
    'vários': 'Todos',
    'Todos': 'Todos',
    'Todos os bairros': 'Todos',
    'Diversos bairros da cidade e região.': 'Todos',
    'Vila Teixeira': 'Todos',
    'FUNCIONÁRIOS': 'Todos',

    # Centro
    'centro': 'Centro',
    'área central': 'Centro',
    'Centro': 'Centro',

    # Senhor dos Montes
    'Senhor dos Montes': 'Senhor dos Montes',
    'Araçá': 'Senhor dos Montes',

    # Fábricas
    'Fabricas': 'Fábricas',
    'Fábricas': 'Fábricas',
    'Fábricas e outros interessados em receber': 'Fábricas',

    # Dom Bosco
    'DOM BOSCO': 'Dom Bosco',
    'Dom Bosco': 'Dom Bosco',

    # Tejuco
    'Tejuco': 'Tejuco',
    'Tijuco': 'Tejuco',
    'Águas Férreas (Tejuco)': 'Tejuco',

    # Matozinhos
    'Matosinhos': 'Matozinhos',
    'Matozinhos': 'Matozinhos',

    # Colônia do Marçal
    'Colônia do Marçal': 'Colônia do Marçal',
    'COLONIA DO MARÇAL': 'Colônia do Marçal',
    'São Pedro (Colônia do Marçal)': 'Colônia do Marçal',

    # Cidade Verde
    'Cidade Verde': 'Cidade Verde',

    # Bela Vista
    'Bela Vista': 'Bela Vista',

    # São Dimas
    'São Dimas': 'São Dimas',

    # CTAN
    'Bengo (CTAN)': 'CTAN',
    'CTan': 'CTAN',
    'Campus Trancredo Neves': 'CTAN',

    # Colônia do Bengo
    'Colônia do Bengo': 'Colônia do Bengo',

    # Rio das Mortes
    'Rio das Mortes': 'Rio das Mortes',

    # Pio XII
    'Pio XII': 'Pio XII',

    # Guarda-Mor
    'Guarda-Mor': 'Guarda-Mor',
    'Bairros Guarda-Mor e Jardim das Acácias': 'Guarda-Mor',

    # Jardim das Acácias
    'Jardim das Acácias': 'Jardim das Acácias',

    # Jardim São José
    'Jardim São José': 'Jardim São José',
    'Vila Jardim São José': 'Jardim São José',

    # Colônia do Felizardo
    'Colônia do Felizardo.': 'Colônia do Felizardo'
}

bairros_coordenadas = {
    'Todos': (-21.13286, -44.25859),
    'Centro': (-21.13623, -44.25636),
    'Senhor dos Montes': (-21.12518, -44.26151),
    'Fábricas': (-21.12311, -44.25001),
    'Dom Bosco': (-21.12165, -44.25108),
    'Tejuco': (-21.14087, -44.27147),
    'Matozinhos': (-21.13046, -44.23473),
    'Colônia do Marçal': (-21.09859, -44.22701),
    'Cidade Verde': (-21.11333, -44.25053),
    'Bela Vista': (-21.11925, -44.22083),
    'São Dimas': (-21.11971, -44.25386),
    'CTAN': (-21.10308, -44.24932),
    'Colônia do Bengo': (-21.09507, -44.26048),
    'Rio das Mortes': (-21.18761, -44.32262),
    'Pio XII': (-21.14055, -44.22855),
    'Guarda-Mor': (-21.14135, -44.26598),
    'Jardim das Acácias': (-21.14603, -44.26576),
    'Jardim São José': (-21.15128, -44.27902),
    'Colônia do Felizardo': (-21.08586, -44.24053)
}

if __name__ == "__main__":
    import pandas as pd

    # Lê o CSV e monta o dataframe
    acoes = 'acoes_extensao.csv'

    df = pd.read_csv(acoes)

    # Descobre bairros únicos na coluna "endereco"
    bairros_unicos = set()
    for enderecos in df["endereco"]:
        for endereco in enderecos.split(";"):
            bairros_unicos.add(endereco.split(",")[0])

    # Remove os bairros já adicionados ao dicionário
    bairros_keys = bairros_grupos.keys()
    bairros_nao_adicionados = set()
    for bairro in bairros_unicos:
        if bairro not in bairros_keys:
            bairros_nao_adicionados.add(bairro)

    # Imprime os bairros únicos não adicionados ainda ao dicionário
    for bairro in bairros_nao_adicionados:
        print(bairro)