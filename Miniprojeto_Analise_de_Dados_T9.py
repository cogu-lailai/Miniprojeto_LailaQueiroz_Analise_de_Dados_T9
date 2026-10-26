# Mini-Projeto Avaliativo - Análise de Dados com Python
#
# Para executar:
# 1. Instale o pandas: pip install pandas
# 2. Deixe este arquivo e "Base_Varejo.csv" na mesma pasta.
# 3. Execute no terminal: python Miniprojeto_Analise_de_Dados_T9.py

import csv
from pathlib import Path

import pandas as pd


# Caminhos dos arquivos. Assim o programa procura o CSV na mesma pasta
# em que este código está salvo.
pasta_do_projeto = Path(__file__).resolve().parent
arquivo_csv = pasta_do_projeto / "Base_Varejo.csv"
arquivo_saida = pasta_do_projeto / "df_limpo.csv"

# Estas são as colunas que vamos usar na análise.
colunas_usadas = [
    "DATA", "CO_ID", "CL_ID", "CL_GENERO", "CL_EC",
    "CL_FHL", "CL_SEG", "PR_ID", "PR_CAT", "PR_NOME"
]


# A base é grande, então vou ler o arquivo em grupos de 50 mil linhas.
# csv.DictReader permite acessar cada informação pelo nome da coluna.
def carregar_arquivo(caminho):
    partes = []
    linhas = []

    with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")

        # Verifica se as colunas necessárias existem no arquivo.
        if not leitor.fieldnames:
            raise ValueError("O arquivo CSV está vazio.")

        for coluna in colunas_usadas:
            if coluna not in leitor.fieldnames:
                raise ValueError("Não encontrei a coluna: " + coluna)

        for linha in leitor:
            # Guarda apenas as colunas que vamos usar.
            linhas.append({coluna: linha.get(coluna) for coluna in colunas_usadas})

            # Quando juntamos 50 mil linhas, transformamos em uma tabela pandas.
            if len(linhas) == 50000:
                partes.append(pd.DataFrame(linhas))
                linhas = []

    # Guarda as linhas que sobraram no último grupo.
    if linhas:
        partes.append(pd.DataFrame(linhas))

    # Junta todos os grupos em uma tabela só.
    return pd.concat(partes, ignore_index=True)


def main():
    # Primeiro, verifico se o arquivo existe.
    if not arquivo_csv.exists():
        print("Não encontrei Base Varejo.csv.")
        print("Coloque o arquivo CSV na mesma pasta deste programa.")
        return

    # 1. IMPORTAÇÃO E PRIMEIRA OBSERVAÇÃO
    dados = carregar_arquivo(arquivo_csv)

    print("\nETAPA 1 - CONHECENDO A BASE")
    print("Quantidade de registros:", len(dados))
    print("Quantidade de colunas:", len(dados.columns))
    print("\nNomes das colunas:")
    print(list(dados.columns))
    print("\nTipos de dados antes da limpeza:")
    print(dados.dtypes)

    # 2. VERIFICAÇÃO DE PROBLEMAS
    print("\nETAPA 2 - PROCURANDO PROBLEMAS")
    print("\nValores vazios em cada coluna:")
    print(dados.isna().sum())
    print("\nLinhas totalmente repetidas:")
    print(dados.duplicated().sum())

    # 3. LIMPEZA DOS DADOS
    # Retiro espaços extras dos textos e transformo textos vazios em valores ausentes.
    colunas_de_texto = ["DATA", "CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]

    for coluna in colunas_de_texto:
        dados[coluna] = dados[coluna].astype("string").str.strip()
        dados[coluna] = dados[coluna].replace("", pd.NA)

    # Converto a data para um formato que o Python reconhece como data.
    # Se uma data não puder ser convertida, ela ficará como valor ausente.
    dados["DATA"] = pd.to_datetime(
        dados["DATA"], format="%d/%m/%Y", errors="coerce"
    )

    # Converto os campos numéricos. Se um valor estiver incorreto,
    # ele vira ausente em vez de inventarmos um número.
    colunas_numericas = ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]

    for coluna in colunas_numericas:
        dados[coluna] = pd.to_numeric(dados[coluna], errors="coerce")

    print("\nDatas inválidas depois da conversão:", dados["DATA"].isna().sum())

    # Uso if/else para preencher categorias vazias ou marcadas como #N/D.
    categorias_corrigidas = []

    for categoria in dados["PR_CAT"]:
        if pd.isna(categoria) or str(categoria).upper() in ["#N/D", "N/D", "NAN"]:
            categorias_corrigidas.append("Sem Categoria")
        else:
            categorias_corrigidas.append(str(categoria).upper())

    dados["PR_CAT"] = categorias_corrigidas

    # Removo linhas totalmente iguais. Não removo apenas pelo número da compra,
    # porque uma compra pode conter mais de um produto.
    repetidas = dados.duplicated().sum()
    dados = dados.drop_duplicates().copy()

    print("\nLinhas totalmente repetidas removidas:", repetidas)

    # Para as análises principais, preciso que data, compra, cliente,
    # número de filhos e produto estejam preenchidos.
    # Por isso, retiro somente as linhas sem esses campos.
    quantidade_antes = len(dados)
    dados = dados.dropna(subset=["DATA", "CO_ID", "CL_ID", "CL_FHL", "PR_ID"]).copy()
    quantidade_removida = quantidade_antes - len(dados)

    print("Linhas removidas por falta de informação essencial:", quantidade_removida)
    print("Registros depois da limpeza:", len(dados))
    print("\nTipos de dados depois da limpeza:")
    print(dados.dtypes)

    # 4. ESTATÍSTICAS DO NÚMERO DE FILHOS
    print("\nETAPA 3 - ESTATÍSTICAS DO NÚMERO DE FILHOS")
    filhos = dados["CL_FHL"]

    print("Contagem:", filhos.count())
    print("Média:", round(filhos.mean(), 2))
    print("Mediana:", filhos.median())
    print("Desvio padrão:", round(filhos.std(), 2))
    print("Moda:", filhos.mode().tolist())
    print("Mínimo:", filhos.min())
    print("Máximo:", filhos.max())
    print("\nQuartis:")
    print(filhos.quantile([0.25, 0.50, 0.75]))

    # 5. AGRUPAMENTOS
    # Como o arquivo não tem preço, vou contar registros, não valores de venda.
    print("\nETAPA 4 - AGRUPAMENTO POR GÊNERO")
    por_genero = dados.groupby("CL_GENERO").agg(
        registros_de_produtos=("PR_ID", "count"),
        compras_diferentes=("CO_ID", "nunique")
    )
    print(por_genero)

    print("\nETAPA 5 - AGRUPAMENTO POR CATEGORIA")
    por_categoria = dados.groupby("PR_CAT").agg(
        registros_de_produtos=("PR_ID", "count"),
        compras_diferentes=("CO_ID", "nunique")
    ).sort_values("registros_de_produtos", ascending=False)
    print(por_categoria)

    print("\nAGRUPAMENTO POR ANO")
    por_ano = dados.groupby(dados["DATA"].dt.year).agg(
        registros_de_produtos=("PR_ID", "count"),
        compras_diferentes=("CO_ID", "nunique")
    )
    print(por_ano)

    # Salvo uma cópia tratada para usar depois, se necessário.
    dados.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")
    print("\nArquivo limpo salvo como:", arquivo_saida.name)

    # 6. CONCLUSÕES
    print("\nETAPA 6 - CONCLUSÕES")
    print("- A categoria com mais registros é:", por_categoria.index[0])
    print("- O gênero com mais registros é:", por_genero["registros_de_produtos"].idxmax())
    print("- A base limpa tem", len(dados), "registros.")
    print("- O número de filhos tem média de", round(filhos.mean(), 2),
          "e mediana de", filhos.median(), ".")
    print("- Categorias ausentes foram identificadas como 'Sem Categoria'.")
    print("- O arquivo não tem preço ou valor de venda, então não consigo calcular faturamento.")
    print("- É importante confirmar com a fonte se todas as linhas repetidas são erros.")


# Esta linha faz a função principal ser executada quando eu rodo o arquivo.
if __name__ == "__main__":
    main()
