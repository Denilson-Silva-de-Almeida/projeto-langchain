import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool, Tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from langchain_experimental.tools import PythonAstREPLTool

def get_groq_llm():
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        try:
            if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                key = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass
    if not key:
        key = "gsk_placeholder"
    return ChatGroq(
        api_key=key,
        model_name="llama3-70b-8192",
        temperature=0
    )


# 1. Relatório Executivo de Faturamento e Receita
@tool
def relatorio_faturamento_receita(pergunta: str, df: pd.DataFrame) -> str:
    """
    Utilize esta ferramenta sempre que o usuário solicitar um relatório executivo de faturamento,
    visão geral da receita, faturamento por cliente/produto/serviço, análise de meios de pagamento
    ou saúde cadastral e volumetria da base de faturamento.
    """
    # Coleta de métricas e estrutura dos dados
    shape = df.shape
    columns = df.dtypes.to_dict()
    nulos = df.isnull().sum().to_dict()
    duplicados = int(df.duplicated().sum())
    
    # Estatísticas de colunas numéricas (valores, quantidades, etc.)
    describe_num = df.describe(include=[np.number]).transpose().to_string() if not df.select_dtypes(include=np.number).empty else "Nenhuma coluna numérica identificada"
    amostra = df.head(3).to_dict(orient='records')

    # Prompt especializado em BPO Financeiro e Faturamento
    template_resposta = PromptTemplate(
        template="""
        Você é um Consultor Sênior de BPO Financeiro e Controladoria encarregado de emitir um
        Relatório Executivo de Faturamento a partir da solicitação: "{pergunta}".

        Abaixo estão as informações e métricas extraídas da planilha de faturamento:

        ================= DADOS E ESTRUTURA DO FATURAMENTO =================
        - Dimensões da base: {shape} (linhas x colunas)
        - Colunas e tipos: {columns}
        - Lançamentos duplicados: {duplicados}
        - Campos vazios / inconsistências: {nulos}
        - Estatísticas descritivas das colunas numéricas:
{describe_num}

        - Amostra dos registros (3 primeiras linhas):
{amostra}
        ===================================================================

        Elabore um relatório executivo profissional, claro, estratégico e em linguagem financeira formal contendo:

        1. Título: ## 📊 Relatório Executivo de Faturamento e Receita
        2. **Visão Geral do Faturamento**: Volume total de notas/faturas emitidas, médias de valores identificados (ticket médio) e dispersão de valores.
        3. **Estrutura dos Dados e Lançamentos**: Descrição das principais colunas financeiras (identificação de datas, clientes, valores brutos/líquidos, impostos ou status).
        4. **Qualidade dos Dados Contábeis/Fiscais**: Apontamento de campos nulos ou duplicidades que possam impactar o fechamento contábil.
        5. **Destaques e Concentração de Receita**: Padrões observados nas faturas (ex: concentração em clientes, sazonalidade ou métodos de cobrança).
        6. **Recomendações Práticas de BPO**: Sugestões para otimização do processo de faturamento, mitigação de riscos operacionais e melhoria de fluxo de caixa.

        Formate valores monetários no padrão brasileiro (R$ X.XXX,XX).
        """,
        input_variables=["pergunta", "shape", "columns", "duplicados", "nulos", "describe_num", "amostra"]
    )

    cadeia = template_resposta | get_groq_llm() | StrOutputParser()

    resposta = cadeia.invoke({
        "pergunta": pergunta,
        "shape": shape,
        "columns": columns,
        "duplicados": duplicados,
        "nulos": nulos,
        "describe_num": describe_num,
        "amostra": amostra
    })

    return resposta


# 2. Relatório de Inadimplência, Aging List e Contas a Receber
@tool
def relatorio_inadimplencia_aging(pergunta: str, df: pd.DataFrame) -> str:
    """
    Utilize esta ferramenta sempre que o usuário solicitar uma análise de inadimplência,
    contas a receber, aging list (faixas de atraso), faturas pendentes/vencidas,
    avaliação de clientes devedores ou estratégias para régua de cobrança.
    """
    # Coleta de métricas financeiras
    colunas = df.dtypes.to_dict()
    describe_num = df.describe(include=[np.number]).transpose().to_string() if not df.select_dtypes(include=np.number).empty else "Nenhuma coluna numérica identificada"
    amostra = df.head(3).to_dict(orient='records')

    # Prompt especializado em Contas a Receber e Cobrança
    template_resposta = PromptTemplate(
        template="""
        Você é um Especialista em BPO Financeiro com foco em Gestão de Contas a Receber, Crédito e Cobrança.
        Sua missão é gerar um diagnóstico detalhado da carteira de recebíveis com base na solicitação: "{pergunta}".

        Dados da carteira de recebíveis:
        ================= ESTATÍSTICAS E ESTRUTURA DA CARTEIRA =================
        Colunas disponíveis: {colunas}
        Estatísticas numéricas:
{describe_num}

        Amostra dos registros:
{amostra}
        ========================================================================

        Elabore um diagnóstico financeiro estratégico contendo:

        1. Título: ## 🚨 Relatório de Inadimplência, Aging List e Contas a Receber
        2. **Diagnóstico da Carteira**: Análise da distribuição dos valores das faturas, prazos de vencimento e identificação dos status de pagamento.
        3. **Faixas de Vencimento (Aging List) e Inadimplência**: Análise dos títulos em aberto, vencidos e liquidados, apontando os maiores impactos no fluxo de caixa.
        4. **Concentração de Risco de Crédito**: Alerta sobre potenciais clientes críticos, valores atípicos (outliers) ou acúmulo de duplicatas não liquidadas.
        5. **Plano de Ação e Régua de Cobrança**: Recomendações práticas para recuperação de crédito, ações preventivas pré-vencimento e medidas corretivas para títulos em atraso.

        Utilize termos do mercado financeiro e formate todos os valores monetários no padrão brasileiro (R$ X.XXX,XX).
        """,
        input_variables=["pergunta", "colunas", "describe_num", "amostra"]
    )

    cadeia = template_resposta | get_groq_llm() | StrOutputParser()

    resposta = cadeia.invoke({
        "pergunta": pergunta,
        "colunas": colunas,
        "describe_num": describe_num,
        "amostra": amostra
    })

    return resposta


# 3. Gerador de Gráficos Financeiros
@tool
def gerar_grafico_financeiro(pergunta: str, df: pd.DataFrame) -> str:
    """
    Utilize esta ferramenta sempre que o usuário solicitar a criação de gráficos ou visualizações financeiras
    a partir da base de dados de faturamento e contas a receber.
    Exemplos: 'Crie um gráfico de faturamento por cliente', 'Plote a distribuição das faturas por status de pagamento',
    'Faça um gráfico da evolução do faturamento', 'Gráfico de barras dos maiores clientes', 'Curva ABC de faturamento'.
    """
    colunas_info = "\n".join([f"- {col} ({dtype})" for col, dtype in df.dtypes.items()])
    amostra_dados = df.head(3).to_dict(orient='records')

    template_resposta = PromptTemplate(
        template="""
        Você é um especialista em visualização de dados financeiros e BI para BPO Financeiro.
        Sua tarefa é gerar **apenas o código Python** para plotar um gráfico financeiro profissional baseado na solicitação:
        "{pergunta}"

        ## Metadados do DataFrame:
        {colunas}

        ## Amostra dos dados (3 primeiras linhas):
        {amostra}

        ## Diretrizes obrigatórias de visualização financeira:
        1. Use as bibliotecas `matplotlib.pyplot` (como `plt`) e `seaborn` (como `sns`).
        2. Defina o tema moderno com `sns.set_theme(style="whitegrid")`.
        3. Verifique com atenção os nomes exatos das colunas existentes no DataFrame `df`.
        4. Escolha o tipo de gráfico adequado para o contexto financeiro:
           - **Evolução de faturamento / Tendência temporal**: `lineplot` com datas ordenadas no eixo X.
           - **Top Clientes / Produtos / Vendedores**: `barplot` horizontal (ex: `y='cliente', x='valor'`) ordenado por valor decrescente.
           - **Distribuição de status (Pago, Pendente, Atrasado, Meios de Pagamento)**: `countplot` ou gráfico de pizza/rosca.
           - **Distribuição de valores de notas/faturas**: `histplot` ou `boxplot` para identificar outliers.
        5. Configure tamanho adequado com `figsize=(9, 4.5)`.
        6. Adicione título descritivo e corporativo alinhado à esquerda com `loc='left'`, `pad=15` e `fontsize=13`.
        7. Adicione rótulos claros nos eixos X e Y.
        8. Se o eixo X tiver muitas categorias ou datas, rotacione as legendas com `plt.xticks(rotation=45, ha='right')`.
        9. Se o eixo representar valores monetários, formate adequadamente.
        10. Remova bordas desnecessárias com `sns.despine()`.
        11. Finalize com `plt.tight_layout()` e `plt.show()`.

        Retorne APENAS o código Python executável, sem markdown explicativo em volta.

        Código Python:
        """,
        input_variables=["pergunta", "colunas", "amostra"]
    )

    cadeia = template_resposta | get_groq_llm() | StrOutputParser()
    codigo_bruto = cadeia.invoke({
        "pergunta": pergunta,
        "colunas": colunas_info,
        "amostra": amostra_dados
    })

    # Limpeza de blocos markdown caso o LLM inclua
    codigo_limpo = codigo_bruto.replace("```python", "").replace("```", "").strip()

    # Execução do código gerado
    exec_globals = {'df': df, 'plt': plt, 'sns': sns, 'pd': pd}
    exec_locals = {}
    exec(codigo_limpo, exec_globals, exec_locals)

    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)

    return ""


# 4. Fábrica de Ferramentas para o Agente ReAct
def criar_ferramentas(df):
    ferramenta_faturamento = Tool(
        name="Relatorio_Faturamento_Receita",
        func=lambda pergunta: relatorio_faturamento_receita.run({"pergunta": pergunta, "df": df}),
        description="""Utilize esta ferramenta sempre que o usuário solicitar um relatório geral de faturamento,
        análise de receita, visão geral das faturas emitidas, ticket médio, dados cadastrais e fiscais da base.""",
        return_direct=True
    )

    ferramenta_inadimplencia = Tool(
        name="Relatorio_Inadimplencia_Aging",
        func=lambda pergunta: relatorio_inadimplencia_aging.run({"pergunta": pergunta, "df": df}),
        description="""Utilize esta ferramenta sempre que o usuário solicitar um relatório ou diagnóstico sobre inadimplência,
        contas a receber, aging list (títulos vencidos por faixas de dias), títulos pendentes e estratégias de régua de cobrança.""",
        return_direct=True
    )

    ferramenta_graficos = Tool(
        name="Gerar_Grafico_Financeiro",
        func=lambda pergunta: gerar_grafico_financeiro.run({"pergunta": pergunta, "df": df}),
        description="""Utilize esta ferramenta sempre que o usuário solicitar qualquer visualização, gráfico ou plotagem
        sobre dados de faturamento, evolução de receitas, comparativo de clientes, formas de pagamento ou status de títulos.
        Palavras-chave: 'gráfico', 'plote', 'visualize', 'faça um gráfico de', 'evolução de faturamento', 'curva ABC'.""",
        return_direct=True
    )

    python_repl = PythonAstREPLTool(locals={"df": df})
    ferramenta_python = Tool(
        name="Consultas_Financeiras_Python",
        func=python_repl.run,
        description="""Utilize esta ferramenta para calcular métricas financeiras pontuais, filtros específicos e consultas detalhadas
        em Python no DataFrame `df`. Exemplos: 'Qual o faturamento total em Março?', 'Quais clientes estão com faturas acima de R$ 5.000?',
        'Qual o valor total recebido via PIX?', 'Quantas faturas estão com status vencido?'.
        Não use esta ferramenta para relatórios completos ou geração de gráficos."""
    )

    return [
        ferramenta_faturamento,
        ferramenta_inadimplencia,
        ferramenta_graficos,
        ferramenta_python
    ]
