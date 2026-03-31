import os
import csv
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Carrega as credenciais
load_dotenv()
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

# Ano dos dados
ANO_ANTERIOR = str(datetime.now().year - 1)

# Cidade
CIDADE = "São João del-Rei"

# URL do Sigaa
URL_SIGAA = "https://www.sig.ufsj.edu.br/sigaa/verTelaLogin.do;jsessionid=808CDC0D2B0FC6975A2FFF3FE0916219.sigaa06"

header = [
    "titulo",
    "tipo",
    "departamento_proponente",
    "coordenador",
    "equipe",
    "area_principal",
    "ods",
    "periodo_realizacao",
    "endereco"
]

dados = []

with sync_playwright() as p:
    # Inicializa o Firefox headless
    browser = p.firefox.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    # Vai para a página de login
    page.goto(URL_SIGAA)

    # Realiza o login
    page.fill("input[name='user.login']", LOGIN)
    page.fill("input[name='user.senha']", PASSWORD)
    page.click("input[type=submit]")

    # Entra no "Consultar Ações"
    page.hover("td.ThemeOfficeMainItem:nth-child(3) > span:nth-child(2)")
    page.click("text='Consultar Ações'")

    # Aplica o filtro de ano e clica em "Buscar"
    page.click("input[id='formBuscaAtividade:selectBuscaAno']")
    page.fill("input[id='formBuscaAtividade:buscaAno']", ANO_ANTERIOR)
    page.click("input[id='formBuscaAtividade:btBuscar']")

    # Itera sobre as linhas da tabela de ações de extensão
    page.wait_for_selector("table#listagem tbody tr")
    linhas = page.locator("table#listagem tbody tr")
    for i in range(linhas.count()):
        acao = {}
        linha_tabela = linhas.nth(i)

        # Clica no "Visualizar"
        visualizar = linha_tabela.locator("img[src='/sigaa/img/view.gif']")
        visualizar.click()

        # Período de Realização
        tr = page.locator("tr:has(th:has-text('Período de Realização:'))")
        td = tr.locator("td").nth(1)
        acao["periodo_realizacao"] = td.inner_text()

        # Endereço
        enderecos = []
        tbody_linhas = page.locator("table[id='tbLocaisRealizacao'] tbody tr:nth-child(n+2)")
        for j in range(tbody_linhas.count()):
            linha = tbody_linhas.nth(j)
            estado = linha.locator("td").nth(0).inner_text()
            municipio = linha.locator("td").nth(1).inner_text()
            bairro = linha.locator("td").nth(2).inner_text()
            enderecos.append(f"{bairro},{municipio},{estado}")
        acao["endereco"] = ";".join(enderecos)

        # Retorna para a página anterior
        page.click("input[value='<< Voltar']")

        # Clica no "Imprimir"
        imprimir = linha_tabela.locator("img[src='/sigaa/img/extensao/printer.png']")
        imprimir.click()

        # Coleta os dados disponíveis no "Imprimir"
        campos_imprimir = {
            "Título:": "titulo",
            "Tipo:": "tipo",
            "Unidade Proponente:": "departamento_proponente",
            "Coordenação:": "coordenador",
            "Área Principal:": "area_principal"
        }

        for th_texto, chave in campos_imprimir.items():
            tr = page.locator(f"tr:has(th:has-text('{th_texto}'))")
            td = tr.locator("td")
            acao[chave] = td.inner_text()

        acao["departamento_proponente"] = acao["departamento_proponente"].replace(' /', '')

        # Equipe
        equipes = []
        tbody_linhas = page.locator("tbody[id$=':tbEquipe:tbody_element'] tr")
        for k in range(tbody_linhas.count()):
            linha = tbody_linhas.nth(k)
            nome = linha.locator("td").nth(0).inner_text()
            equipes.append(nome)
        acao["equipe"] = ",".join(equipes)

        # ODS
        ods_lista = []
        tbody_linhas = page.locator("tbody[id$=':tbOds:tbody_element'] tr")
        for l in range(tbody_linhas.count()):
            linha = tbody_linhas.nth(l)
            numero = linha.locator("td").nth(0).inner_text()
            descricao = linha.locator("td").nth(1).inner_text()
            ods = numero + " - " + descricao
            ods_lista.append(ods)
        acao["ods"] = ",".join(ods_lista)

        # Retorna para a página anterior
        page.click("a[href='javascript:history.back();']")

        dados.append(acao)

        print(f"Ação {i+1} coletada!")

    print("Ações coletadas com sucesso!")

    # Filtra o município das ações coletadas
    dados_filtrados = []
    for dado in dados:
        endereco_filtrado = []
        for endereco in dado["endereco"].split(";"):
            if CIDADE in endereco:
                endereco_filtrado.append(endereco)
        endereco_filtrado = ";".join(endereco_filtrado)
        if endereco_filtrado != "":
            dado_filtrado = { **dado, "endereco": endereco_filtrado }
            dados_filtrados.append(dado_filtrado)

    print("Ações filtradas com sucesso!")

    with open("acoes_extensao.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(dados_filtrados)

    print("CSV gerado com sucesso!")

    browser.close()