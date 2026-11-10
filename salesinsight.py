import pandas as pd
import random,
from datetime import datetime, timedelta

def gerar_dataset_vendas(n_registros=200, seed=42):
    random.seed(seed)

    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor",
                "Teclado", "Mouse", "Headset"]

    categorias = {
        "Notebook": "Computadores",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Computadores",
        "Teclado": "Perifericos",
        "Mouse": "Perifericos",
        "Headset": "Perifericos"
    }

    precos = {
        "Notebook": 3500,
        "Smartphone": 2200,
        "Tablet": 1800,
        "Monitor": 1200,
        "Teclado": 250,
        "Mouse": 120,
        "Headset": 350
    }

    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    dados = []

    for i in range(n_registros):
        produto = random.choice(produtos)
        quantidade = random.randint(1, 10)
        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))
        data_txt = data.strftime("%Y-%m-%d")

        # Alguns registros terão uma data inválida para praticarmos a limpeza.
        if random.random() < 0.03:
            data_txt = "DATA INVALIDA"

        dados.append({
            "id_venda": i + 1,
            "data_venda": data_txt,
            "cliente": f"Cliente_{random.randint(1, 50):03d}",
            "produto": produto,
            "categoria": categorias[produto],
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco
        })

    return pd.DataFrame(dados)


df_bruto = gerar_dataset_vendas()
df_bruto.to_csv("vendas.csv", index=False)

print("Quantidade de registros:", len(df_bruto))
display(df_bruto.head())

import pandas as pd

# Abre o arquivo CSV que criamos na etapa anterior
df_bruto = pd.read_csv("vendas.csv")

print("Tamanho da tabela (linhas, colunas):")
print(df_bruto.shape)

print("\nNomes das colunas:")
print(df_bruto.columns.tolist())

print("\nTipos de dados de cada coluna:")
print(df_bruto.dtypes)

print("\nValores ausentes em cada coluna:")
print(df_bruto.isnull().sum())

print("\nCinco primeiras vendas:")
display(df_bruto.head())

import pandas as pd

# Abre o arquivo CSV que criamos na etapa anterior
df_bruto = pd.read_csv("vendas.csv")

print("Tamanho da tabela (linhas, colunas):")
print(df_bruto.shape)

print("\nNomes das colunas:")
print(df_bruto.columns.tolist())

print("\nTipos de dados de cada coluna:")
print(df_bruto.dtypes)

print("\nValores ausentes em cada coluna:")
print(df_bruto.isnull().sum())

print("\nCinco primeiras vendas:")
display(df_bruto.head())

# Converte datas inválidas em valores vazios (NaT)
df_bruto["data_venda"] = pd.to_datetime(
    df_bruto["data_venda"],
    errors="coerce"
)

# Conta quantas datas não puderam ser convertidas
datas_invalidas = df_bruto["data_venda"].isna().sum()
print("Vendas com data inválida:", datas_invalidas)

# Cria uma tabela limpa, mantendo a tabela original
df_limpo = df_bruto.dropna(subset=["data_venda"]).copy()

print("Vendas antes da limpeza:", len(df_bruto))
print("Vendas após a limpeza:", len(df_limpo))

display(df_limpo.head())

# Fazemos uma cópia para preservar df_limpo
df_analise = df_limpo.copy()

# Receita gerada por cada venda: quantidade × preço unitário
df_analise["receita_total"] = (
    df_analise["quantidade"] * df_analise["preco_unitario"]
)

# Extraímos mês, trimestre e ano da data
df_analise["mes"] = df_analise["data_venda"].dt.month
df_analise["trimestre"] = "Q" + df_analise["data_venda"].dt.quarter.astype(str)
df_analise["ano"] = df_analise["data_venda"].dt.year

# Traduzimos o número do mês para o nome em português
nomes_meses = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março",
    4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro",
    10: "Outubro", 11: "Novembro", 12: "Dezembro"
}
df_analise["mes_nome"] = df_analise["mes"].map(nomes_meses)

# Classificamos cada venda pelo valor da receita
df_analise["faixa_receita_item"] = "Baixo Valor"
df_analise.loc[df_analise["receita_total"] >= 500, "faixa_receita_item"] = "Médio Valor"
df_analise.loc[df_analise["receita_total"] >= 5000, "faixa_receita_item"] = "Alto Valor"

# Conferimos as novas colunas
display(df_analise[
    ["data_venda", "quantidade", "preco_unitario",
     "receita_total", "mes_nome", "trimestre", "ano",
     "faixa_receita_item"]
].head())

display(
    df_analise[["receita_total", "faixa_receita_item"]]
    .sort_values("receita_total")
    .head(10)
)
display(
    df_analise.groupby("faixa_receita_item")["receita_total"].agg(["min", "max"])
)

# Vendas agrupadas por mês
por_mes = (
    df_analise.groupby("mes")
    .agg(
        receita_total=("receita_total", "sum"),
        quantidade=("quantidade", "sum"),
        n_vendas=("id_venda", "count")
    )
    .reset_index()
    .sort_values("mes")
)

# Cinco produtos com maior receita
top_produtos = (
    df_analise.groupby("produto")
    .agg(receita_total=("receita_total", "sum"))
    .sort_values("receita_total", ascending=False)
    .head(5)
    .reset_index()
)

# Receita por categoria
por_categoria = (
    df_analise.groupby("categoria")
    .agg(receita_total=("receita_total", "sum"))
    .sort_values("receita_total", ascending=False)
    .reset_index()
)

# Receita total e média por venda em cada região
por_regiao = (
    df_analise.groupby("regiao")
    .agg(
        receita_total=("receita_total", "sum"),
        ticket_medio=("receita_total", "mean")
    )
    .sort_values("receita_total", ascending=False)
    .reset_index()
)

# Exibe os quatro resumos
print("=== VENDAS POR MÊS ===")
display(por_mes)

print("=== TOP 5 PRODUTOS ===")
display(top_produtos)

print("=== RECEITA POR CATEGORIA ===")
display(por_categoria)

print("=== RESULTADOS POR REGIÃO ===")
display(por_regiao)

# Soma quanto cada cliente gastou e conta suas vendas
clientes_resumo = (
    df_analise.groupby("cliente")
    .agg(
        gasto_total=("receita_total", "sum"),
        n_vendas=("id_venda", "count")
    )
    .reset_index()
)

# Divide os clientes em três grupos, do menor para o maior gasto
ordem_gastos = clientes_resumo["gasto_total"].rank(method="first")

clientes_resumo["classificacao_cliente"] = pd.qcut(
    ordem_gastos,
    q=3,
    labels=["Bronze", "Prata", "Ouro"]
)

# Mostra os clientes que mais gastaram primeiro
display(
    clientes_resumo.sort_values("gasto_total", ascending=False)
)

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Formata os valores como reais
formato_reais = FuncFormatter(lambda valor, pos: f"R$ {valor:,.0f}")

fig, eixos = plt.subplots(2, 2, figsize=(14, 10))

# 1. Receita por mês
eixos[0, 0].bar(por_mes["mes"], por_mes["receita_total"], color="steelblue")
eixos[0, 0].set_title("Receita total por mês")
eixos[0, 0].set_xlabel("Mês")
eixos[0, 0].set_ylabel("Receita")
eixos[0, 0].set_xticks(range(1, 13))
eixos[0, 0].yaxis.set_major_formatter(formato_reais)

# 2. Receita dos cinco produtos com maior venda
eixos[0, 1].bar(top_produtos["produto"], top_produtos["receita_total"], color="seagreen")
eixos[0, 1].set_title("Top 5 produtos por receita")
eixos[0, 1].set_xlabel("Produto")
eixos[0, 1].set_ylabel("Receita")
eixos[0, 1].tick_params(axis="x", rotation=30)
eixos[0, 1].yaxis.set_major_formatter(formato_reais)

# 3. Receita por categoria
eixos[1, 0].bar(por_categoria["categoria"], por_categoria["receita_total"], color="darkorange")
eixos[1, 0].set_title("Receita por categoria")
eixos[1, 0].set_xlabel("Categoria")
eixos[1, 0].set_ylabel("Receita")
eixos[1, 0].tick_params(axis="x", rotation=30)
eixos[1, 0].yaxis.set_major_formatter(formato_reais)

# 4. Receita por região
eixos[1, 1].bar(por_regiao["regiao"], por_regiao["receita_total"], color="mediumpurple")
eixos[1, 1].set_title("Receita por região")
eixos[1, 1].set_xlabel("Região")
eixos[1, 1].set_ylabel("Receita")
eixos[1, 1].tick_params(axis="x", rotation=30)
eixos[1, 1].yaxis.set_major_formatter(formato_reais)

plt.tight_layout()
plt.show()

# Função: resume as vendas por mês
def resumo_mensal(dados):
    return (
        dados.groupby("mes")
        .agg(
            receita_total=("receita_total", "sum"),
            quantidade=("quantidade", "sum"),
            n_vendas=("id_venda", "count")
        )
        .reset_index()
        .sort_values("mes")
    )

# Função: encontra os cinco produtos com maior receita
def resumo_produtos(dados):
    return (
        dados.groupby("produto")
        .agg(receita_total=("receita_total", "sum"))
        .sort_values("receita_total", ascending=False)
        .head(5)
        .reset_index()
    )

# Função: resume a receita por categoria
def resumo_categorias(dados):
    return (
        dados.groupby("categoria")
        .agg(receita_total=("receita_total", "sum"))
        .sort_values("receita_total", ascending=False)
        .reset_index()
    )

# Função: resume a receita e o ticket médio por região
def resumo_regioes(dados):
    return (
        dados.groupby("regiao")
        .agg(
            receita_total=("receita_total", "sum"),
            ticket_medio=("receita_total", "mean")
        )
        .sort_values("receita_total", ascending=False)
        .reset_index()
    )

# Classe: reúne os resumos da análise de vendas
class SalesInsight:
    def __init__(self, dados):
        self.dados = dados.copy()

    def gerar_resumos(self):
        return {
            "por_mes": resumo_mensal(self.dados),
            "top_produtos": resumo_produtos(self.dados),
            "por_categoria": resumo_categorias(self.dados),
            "por_regiao": resumo_regioes(self.dados)
        }

# Cria o analisador e gera novamente os resumos
analisador = SalesInsight(df_analise)
metricas_refatoradas = analisador.gerar_resumos()

# Mantém os mesmos nomes usados nos gráficos anteriores
por_mes = metricas_refatoradas["por_mes"]
top_produtos = metricas_refatoradas["top_produtos"]
por_categoria = metricas_refatoradas["por_categoria"]
por_regiao = metricas_refatoradas["por_regiao"]

print("Resumos gerados pela classe SalesInsight:")
display(por_mes.head())
display(top_produtos)
display(por_categoria)
display(por_regiao)

import json
import zipfile
from google.colab import files

# Tabelas que serão exportadas
tabelas = {
    "vendas_por_mes": por_mes,
    "top_produtos": top_produtos,
    "receita_por_categoria": por_categoria,
    "receita_por_regiao": por_regiao,
    "resumo_clientes": clientes_resumo
}

# Salva cada tabela em CSV e prepara os dados para o JSON
dados_json = {}

for nome, tabela in tabelas.items():
    tabela.to_csv(f"{nome}.csv", index=False, encoding="utf-8-sig")
    dados_json[nome] = tabela.to_dict(orient="records")

# Salva todos os resumos em um único arquivo JSON
with open("resumos_vendas.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)

# Reúne os CSVs e o JSON em um arquivo ZIP
with zipfile.ZipFile("resultados_salesinsight.zip", "w") as zip:
    for nome in tabelas:
        zip.write(f"{nome}.csv")
    zip.write("resumos_vendas.json")

# Inicia o download para o computador
files.download("resultados_salesinsight.zip")

from google.colab import files

conteudo = """# SalesInsight PY

Projeto avaliativo de análise de vendas desenvolvido em Python para a disciplina
Fundamentos de Dados: Programação e Análise Preditiva com Python.

## Objetivo

Explorar dados fictícios de vendas, realizar a limpeza e a preparação dos dados,
calcular indicadores e apresentar os resultados em tabelas e gráficos.

## Dados

O projeto utiliza dados fictícios de vendas, com informações como data, produto,
quantidade, preço, cliente e região. Algumas datas inválidas foram incluídas
intencionalmente para praticar a limpeza dos dados.

## Etapas realizadas

- Inspeção e limpeza dos dados;
- Cálculo da receita por venda;
- Criação de informações de mês, trimestre e ano;
- Classificação das vendas por faixa de receita;
- Análise de vendas por mês, produto, categoria e região;
- Classificação de clientes em Bronze, Prata e Ouro;
- Criação de gráficos;
- Organização da análise em funções e na classe `SalesInsight`;
- Exportação dos resumos em CSV e JSON.

## Como executar

1. Abra o notebook do projeto no Google Colab.
2. Execute as células na ordem, do início ao fim.
3. Para gerar os arquivos de resultados, execute também a célula de exportação.

## Tecnologias utilizadas

- Python
- pandas
- matplotlib
- Google Colab

## Resultados

Os resultados incluem tabelas-resumo, gráficos e arquivos exportados em CSV e JSON.

## Autora

Raquel
"""

with open("README.md", "w", encoding="utf-8") as arquivo:
    arquivo.write(conteudo)

files.download("README.md")