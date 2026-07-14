import pandas as pd
from bairros import bairros_coordenadas, bairros_grupos

ARQUIVO_ENTRADA = "acoes_extensao.csv"
ARQUIVO_SAIDA = "acoes_extensao_coordenadas.csv"


def adicionar_coordenadas(df):
    """Adiciona as colunas 'bairro_grupo' e 'coordenada' com base no endereço."""
    df["bairro_grupo"] = None
    df["coordenada"] = None

    for index, row in df.iterrows():
        bairro = row["endereco"].split(";")[0].split(",")[0]
        if bairro not in bairros_grupos:
            raise KeyError(
                f"Bairro '{bairro}' não está mapeado em bairros.py. "
                "Rode 'python bairros.py' para listar os bairros faltantes e adicione-os."
            )
        grupo = bairros_grupos[bairro]
        df.at[index, "bairro_grupo"] = grupo
        df.at[index, "coordenada"] = bairros_coordenadas[grupo]

    return df


def main():
    df = pd.read_csv(ARQUIVO_ENTRADA)
    df = adicionar_coordenadas(df)
    print("Coordenadas geradas com sucesso!")

    df.to_csv(ARQUIVO_SAIDA, index=False)
    print("CSV gerado com sucesso!")


if __name__ == "__main__":
    main()
