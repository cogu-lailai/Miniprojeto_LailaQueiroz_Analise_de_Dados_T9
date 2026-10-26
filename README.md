# Mini-Projeto — Minha primeira análise de dados de varejo

## 1. Sobre o projeto

Este é meu mini projeto de análise de dados com Python. O objetivo é conhecer uma base de compras de varejo, procurar problemas nos dados, fazer uma limpeza inicial e observar algumas informações simples.

Usei Python, `csv.DictReader` e `pandas`. Tentei deixar o código comentado para explicar o que cada parte faz.

## 2. Arquivos do projeto

- `Miniprojeto_Analise_de_Dados_T9.py`: código Python.
- `Base_Varejo.csv`: arquivo original usado na análise.
- `df_limpo.csv`: arquivo que o programa cria depois da limpeza.
- `README.md`: explicação do projeto.
- `README_Laila_Queiroz_T9.md`: instruções para executar o trabalho.

## 3. Como executar

1. Instale o Python e a biblioteca pandas com `pip install pandas`.
2. Coloque o código e `Base_Varejo.csv` na mesma pasta.
3. Abra o terminal nessa pasta.
4. Execute `python Miniprojeto_Analise_de_Dados_T9.py`.
5. Veja os resultados no terminal. O programa também vai criar `df_limpo.csv`.

## 4. O que eu fiz

Primeiro, li o arquivo CSV usando `csv.DictReader`. Como a base é grande, o código lê os dados em grupos menores e depois junta tudo em uma tabela pandas.

Depois, observei quantos registros e colunas existem, quais são os tipos de dados, quantos valores estão vazios e quantas linhas são totalmente repetidas.

Na limpeza, retirei espaços extras, converti a coluna `DATA` para data e transformei algumas colunas em números. Também usei `if/else` para substituir categorias vazias ou marcadas como `#N/D` por `Sem Categoria`.

Removi as linhas totalmente duplicadas. Em seguida, retirei linhas sem data, compra, cliente, número de filhos ou produto, porque esses campos são necessários para as análises feitas neste projeto. Essa decisão pode ser revista se a fonte dos dados indicar outra regra.

Também usei uma expressão regular para trocar vários espaços seguidos por um só nos textos, e conferi a regra do número da compra (`CO_ID`): nenhuma compra tem mais de uma data ou mais de um cliente.

Por fim, calculei estatísticas para o número de filhos e fiz agrupamentos por gênero, categoria e ano.

## 5. O que é ETL?

ETL é uma sigla em inglês para Extrair, Transformar e Carregar.

- **Extrair:** obter os dados de um arquivo ou sistema. Neste projeto, extraí os dados do CSV.
- **Transformar:** organizar e corrigir os dados. Aqui, converti datas, tratei categorias vazias e removi duplicatas.
- **Carregar:** salvar os dados prontos para serem usados. Neste projeto, salvei a tabela limpa no arquivo `df_limpo.csv`.

## 6. O que entendi sobre qualidade dos dados

A qualidade dos dados é importante porque informações vazias, datas incorretas, textos diferentes para a mesma categoria ou linhas repetidas podem atrapalhar uma análise. Mesmo assim, não devemos apagar dados sem pensar: é importante entender o que cada coluna significa e explicar as decisões tomadas.

Neste projeto, tratei alguns problemas básicos, mas sei que uma limpeza inicial não garante que todos os dados estejam corretos.

## 7. Insights da análise

Os resultados abaixo foram observados na base enviada, após os tratamentos descritos:

1. A base original tem 830.000 registros.
2. Foram identificadas 96.553 linhas totalmente repetidas antes da limpeza.
3. A categoria com mais registros é `ALIMENTOS`, com 384.197 registros na base após a remoção de duplicatas.
4. O gênero `F` aparece em 382.427 registros, enquanto o gênero `M` aparece em 351.020.
5. O número de filhos tem média aproximada de 1,15; a mediana e a moda são 0.
6. A base não tem coluna de preço ou valor de venda. Por isso, os resultados mostram contagens de registros, não qual categoria vendeu mais em dinheiro.

**Observação:** os números de insights são resultados da execução anterior da análise. Se o código ou os critérios de limpeza forem alterados, execute novamente e confira se os valores continuam iguais.

## 8. Limitações e próximos passos

Este foi um primeiro exercício, então a análise é simples. Eu ainda precisaria conferir com a origem da base se as linhas repetidas são erros ou se algumas representam itens legítimos. Também seria interessante entender melhor o significado de cada coluna e confirmar se os valores ausentes devem ser excluídos ou preenchidos.

O arquivo não tem preços nem dimensões físicas, então não foi possível analisar faturamento ou dimensões de produtos.

## 9. Versionamento no GitHub

O projeto deve ser enviado para um repositório público com um nome parecido com `Miniprojeto_NomeAluno_Analise_de_Dados_T1`.

Para mostrar o desenvolvimento, posso fazer commits separados conforme avanço, por exemplo:
- `Adiciona arquivos iniciais do projeto`
- `Adiciona leitura e diagnóstico da base`
- `Adiciona limpeza e estatísticas`
- `Finaliza README e conclusões`

Os commits devem refletir as alterações feitas de verdade. Antes de entregar, preciso confirmar que o repositório está público e enviar o link no AVA.
