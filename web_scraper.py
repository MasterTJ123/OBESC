import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Carrega as credenciais
load_dotenv()
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

# Ano dos dados (ano anterior ao atual)
ANO_ANTERIOR = str(datetime.now().year - 1)

# Cidade usada para filtrar as ações coletadas
CIDADE = "São João del-Rei"

# URL de login do SIGAA
URL_SIGAA = "https://www.sig.ufsj.edu.br/sigaa/verTelaLogin.do"

# Arquivo de saída
ARQUIVO_SAIDA = "acoes_extensao.csv"

# Ordem das colunas no CSV
HEADER = [
    "titulo",
    "tipo",
    "unidade_proponente",
    "coordenador",
    "equipe",
    "area_principal",
    "ods",
    "periodo_realizacao",
    "endereco",
]

# Campos coletados na tela "Imprimir": texto do <th> -> chave no dicionário
CAMPOS_IMPRIMIR = {
    "Título:": "titulo",
    "Tipo:": "tipo",
    "Unidade Proponente:": "unidade_proponente",
    "Coordenação:": "coordenador",
    "Área Principal:": "area_principal",
}


def fazer_login(page):
    """Faz login no SIGAA com as credenciais do .env."""
    page.goto(URL_SIGAA)
    page.fill("input[name='user.login']", LOGIN)
    page.fill("input[name='user.senha']", PASSWORD)
    page.click("input[type=submit]")


def buscar_acoes_do_ano(page):
    """Navega até 'Consultar Ações' e busca as ações do ano configurado."""
    page.hover("td.ThemeOfficeMainItem:nth-child(3) > span:nth-child(2)")
    page.click("text='Consultar Ações'")
    page.click("input[id='formBuscaAtividade:selectBuscaAno']")
    page.fill("input[id='formBuscaAtividade:buscaAno']", ANO_ANTERIOR)
    page.click("input[id='formBuscaAtividade:btBuscar']")
    page.wait_for_selector("table#listagem tbody tr")


def coletar_endereco(page):
    """Coleta os endereços da tela 'Visualizar' como 'bairro,municipio,estado' separados por ';'."""
    enderecos = []
    linhas = page.locator("table[id='tbLocaisRealizacao'] tbody tr:nth-child(n+2)")
    for linha in linhas.all():
        estado = linha.locator("td").nth(0).inner_text()
        municipio = linha.locator("td").nth(1).inner_text()
        bairro = linha.locator("td").nth(2).inner_text()
        enderecos.append(f"{bairro},{municipio},{estado}")
    return ";".join(enderecos)


def coletar_linhas_tabela(page, sufixo_id, formata):
    """Aplica `formata(linha)` em cada <tr> de um tbody cujo id termina em `sufixo_id`."""
    linhas = page.locator(f"tbody[id$='{sufixo_id}'] tr")
    return [formata(linha) for linha in linhas.all()]


def coletar_equipe(page):
    """Coleta os nomes da equipe separados por ';'."""
    nomes = coletar_linhas_tabela(
        page,
        ":tbEquipe:tbody_element",
        lambda linha: linha.locator("td").nth(0).inner_text(),
    )
    return ";".join(nomes)


def coletar_ods(page):
    """Coleta os ODS no formato 'numero - descrição' separados por ';'."""
    ods = coletar_linhas_tabela(
        page,
        ":tbOds:tbody_element",
        lambda linha: f'{linha.locator("td").nth(0).inner_text()} - {linha.locator("td").nth(1).inner_text()}',
    )
    return ";".join(ods)


def coletar_acao(page, linha_tabela):
    """Coleta todos os dados de uma ação a partir da sua linha na listagem."""
    acao = {}

    # Tela "Visualizar": período de realização e endereço
    linha_tabela.locator("img[src='/sigaa/img/view.gif']").click()
    tr_periodo = page.locator("tr:has(th:has-text('Período de Realização:'))")
    acao["periodo_realizacao"] = tr_periodo.locator("td").nth(1).inner_text()
    acao["endereco"] = coletar_endereco(page)
    page.click("input[value='<< Voltar']")

    # Tela "Imprimir": campos simples, equipe e ODS
    linha_tabela.locator("img[src='/sigaa/img/extensao/printer.png']").click()
    for th_texto, chave in CAMPOS_IMPRIMIR.items():
        tr = page.locator(f"tr:has(th:has-text('{th_texto}'))")
        acao[chave] = tr.locator("td").inner_text()
    acao["unidade_proponente"] = acao["unidade_proponente"].replace(" /", "")
    acao["equipe"] = coletar_equipe(page)
    acao["ods"] = coletar_ods(page)
    page.click("a[href='javascript:history.back();']")

    return acao


def coletar_todas_acoes(page):
    """Coleta os dados de todas as ações listadas."""
    buscar_acoes_do_ano(page)
    linhas = page.locator("table#listagem tbody tr")
    dados = []
    for i, linha in enumerate(linhas.all(), start=1):
        dados.append(coletar_acao(page, linha))
        print(f"Ação {i} coletada!")
    return dados


def filtrar_por_cidade(dados):
    """Mantém só as ações realizadas na CIDADE, descartando os demais endereços."""
    filtrados = []
    for dado in dados:
        enderecos = [e for e in dado["endereco"].split(";") if CIDADE in e]
        if enderecos:
            filtrados.append({**dado, "endereco": ";".join(enderecos)})
    return filtrados


def salvar_csv(dados, arquivo):
    """Grava os dados coletados em um CSV."""
    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(dados)


def main():
    with sync_playwright() as p:
        # Inicializa o Firefox headless
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        fazer_login(page)

        dados = coletar_todas_acoes(page)
        print("Ações coletadas com sucesso!")

        dados = filtrar_por_cidade(dados)
        print("Ações filtradas com sucesso!")

        salvar_csv(dados, ARQUIVO_SAIDA)
        print("CSV gerado com sucesso!")

        browser.close()


if __name__ == "__main__":
    main()
