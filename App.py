import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
try:
    from langchain.agents import create_react_agent, AgentExecutor
except ImportError:
    from langchain_classic.agents import create_react_agent, AgentExecutor
from ferramentas import criar_ferramentas

# Inicia o app
st.set_page_config(
    page_title="Assistente de BPO Financeiro & Faturamento",
    layout="centered",
    page_icon="💼"
)

st.title("💼 Assistente de BPO Financeiro & Faturamento com IA")

# Descrição da ferramenta especializada
st.info("""
Este assistente foi desenvolvido especialmente para **BPO Financeiro, Gestão de Faturamento e Contas a Receber**.
Com apoio de um agente inteligente via **LangChain** e **Groq**, você pode:

- 📊 **Gerar Relatórios Executivos Automáticos**:
    - **Relatório de Faturamento e Receita**: Volume faturado, ticket médio, análise de clientes/produtos, meios de pagamento e qualidade dos dados fiscais.
    - **Relatório de Inadimplência & Aging List**: Diagnóstico de contas a receber, faixas de vencimento, concentração de risco e régua de cobrança.

- 🔎 **Realizar Consultas Financeiras em Linguagem Natural**: como *"Qual é o faturamento total do cliente X?"*, *"Qual o total de títulos vencidos há mais de 30 dias?"*, *"Quanto foi recebido via PIX vs Boleto?"*.
                
- 📈 **Gerar Gráficos Financeiros**: Curva ABC de clientes, evolução temporal de faturamento, distribuição por status de pagamento e meios de cobrança.
""")

# Upload da planilha de faturamento
st.markdown("### 📁 Faça upload da sua planilha de faturamento (CSV)")
arquivo_carregado = st.file_uploader("Selecione um arquivo CSV", type="csv", label_visibility="collapsed")

if arquivo_carregado:
    df = pd.read_csv(arquivo_carregado)
    st.success("Planilha carregada com sucesso!")

    # Visão rápida dos dados
    col1, col2 = st.columns(2)
    col1.metric("Total de Lançamentos", f"{len(df):,} linhas".replace(",", "."))
    col2.metric("Total de Colunas", f"{len(df.columns)} colunas")

    st.markdown("### 🔍 Primeiras linhas da base de faturamento")
    st.dataframe(df.head())

    # Configuração do LLM (Groq)
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192",
        temperature=0
    )

    # Criação das ferramentas especializadas em BPO Financeiro
    tools = criar_ferramentas(df)

    # Prompt ReAct especializado em finanças
    df_head = df.head().to_markdown()

    prompt_react_pt = PromptTemplate(
        input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
        partial_variables={"df_head": df_head},
        template="""
        Você é um consultor especialista em BPO Financeiro, Gestão de Faturamento e Controladoria que sempre responde em português.

        Você tem acesso a um DataFrame pandas chamado `df` com dados de faturamento e movimentações financeiras.
        Aqui estão as primeiras linhas do DataFrame, obtidas com `df.head().to_markdown()`:

        {df_head}

        Responda às solicitações e dúvidas financeiras da melhor forma possível.

        Para isso, você tem acesso às seguintes ferramentas:

        {tools}

        Use estritamente o seguinte formato de raciocínio:

        Question: a pergunta ou solicitação financeira de entrada  
        Thought: você deve sempre pensar no que fazer passo a passo  
        Action: a ação a ser tomada, deve ser uma das [{tool_names}]  
        Action Input: a entrada para a ação  
        Observation: o resultado da ação  
        ... (este Thought/Action/Action Input/Observation pode se repetir N vezes)
        Thought: Agora eu sei a resposta final  
        Final Answer: a resposta final para a solicitação original.

        Diretrizes financeiras obrigatórias:
        - Sempre formate valores monetários no padrão brasileiro de moeda (ex: R$ 1.250,50).
        - Ao responder consultas pontuais com Consultas_Financeiras_Python: apresente os resultados de forma clara, organizada em listas ou tabelas, com explicações objetivas e precisão nos cálculos.

        Comece!

        Question: {input}  
        Thought: {agent_scratchpad}"""
    )

    # Inicialização do Agente ReAct
    agente = create_react_agent(llm=llm, tools=tools, prompt=prompt_react_pt)
    orquestrador = AgentExecutor(
        agent=agente,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    # ==========================================
    # AÇÕES RÁPIDAS (RELATÓRIOS EXECUTIVOS DE BPO)
    # ==========================================
    st.markdown("---")
    st.markdown("## ⚡ Ações Rápidas de BPO Financeiro")

    col_btn1, col_btn2 = st.columns(2)

    # 1. Relatório de Faturamento e Receita
    with col_btn1:
        if st.button("📊 Relatório de Faturamento & Receita", key="botao_relatorio_faturamento", use_container_width=True):
            with st.spinner("Gerando diagnóstico de faturamento 💼"):
                resposta = orquestrador.invoke({"input": "Gere um relatório executivo completo de faturamento e receita"})
                st.session_state['relatorio_faturamento'] = resposta["output"]

    # 2. Relatório de Inadimplência e Aging List
    with col_btn2:
        if st.button("🚨 Relatório de Inadimplência & Aging", key="botao_relatorio_inadimplencia", use_container_width=True):
            with st.spinner("Gerando análise de contas a receber e aging 💼"):
                resposta = orquestrador.invoke({"input": "Gere um relatório detalhado de inadimplência, aging list e contas a receber"})
                st.session_state['relatorio_inadimplencia'] = resposta["output"]

    # Exibição dos Relatórios Salvos
    if 'relatorio_faturamento' in st.session_state:
        with st.expander("📄 Resultado: Relatório Executivo de Faturamento & Receita", expanded=True):
            st.markdown(st.session_state['relatorio_faturamento'])
            st.download_button(
                label="📥 Baixar Relatório de Faturamento (.md)",
                data=st.session_state['relatorio_faturamento'],
                file_name="relatorio_faturamento_receita.md",
                mime="text/markdown"
            )

    if 'relatorio_inadimplencia' in st.session_state:
        with st.expander("📄 Resultado: Relatório de Inadimplência & Aging List", expanded=True):
            st.markdown(st.session_state['relatorio_inadimplencia'])
            st.download_button(
                label="📥 Baixar Relatório de Inadimplência (.md)",
                data=st.session_state['relatorio_inadimplencia'],
                file_name="relatorio_inadimplencia_aging.md",
                mime="text/markdown"
            )

    # ==========================================
    # CONSULTAS EM LINGUAGEM NATURAL
    # ==========================================
    st.markdown("---")
    st.markdown("## 🔎 Consultas de Faturamento e Contas a Receber")
    pergunta_sobre_dados = st.text_input(
        "Faça uma pergunta sobre os dados financeiros:",
        placeholder="Ex: 'Qual o faturamento total por cliente?', 'Qual o valor total de títulos vencidos?', 'Qual o ticket médio?'"
    )
    if st.button("Consultar Dados", key="responder_pergunta_dados"):
        if pergunta_sobre_dados.strip():
            with st.spinner("Consultando base de faturamento 💼"):
                resposta = orquestrador.invoke({"input": pergunta_sobre_dados})
                st.markdown(resposta["output"])
        else:
            st.warning("Por favor, digite uma pergunta antes de consultar.")

    # ==========================================
    # GERAÇÃO DE GRÁFICOS FINANCEIROS
    # ==========================================
    st.markdown("---")
    st.markdown("## 📈 Gerar Gráficos Financeiros")
    pergunta_grafico = st.text_input(
        "Descreva o gráfico financeiro que deseja visualizar:",
        placeholder="Ex: 'Crie um gráfico de barras com o top 10 clientes por faturamento', 'Plote a evolução do faturamento por data', 'Gráfico de pizza dos meios de pagamento'"
    )
    if st.button("Gerar Gráfico Financeiro", key="gerar_grafico"):
        if pergunta_grafico.strip():
            with st.spinner("Gerando visualização financeira 💼"):
                orquestrador.invoke({"input": pergunta_grafico})
        else:
            st.warning("Por favor, descreva o gráfico antes de gerar.")
