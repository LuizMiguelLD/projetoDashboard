# Para visualizar use o comando:
# streamlit run app.py
# E para parar de rodar o streamlit aperte Crtl+C

# --- Importando as bibliotecas ---

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Treino da academia",
    page_icon="📈",
    layout="wide",
)

# --- Carregamento dos Data Frame ---
df = pd.read_csv("dados-treino-final.csv")

# --- Barra Lateral (Filtros) ---
# sidebar --> barra lateral
# header --> título
st.sidebar.header("🔍 Filtros")

# Filtro de Genero
genero_disponivel = sorted(df['genero'].unique()) # sorted faz uma organização dos anos e o unique vê os valores que contem, tipo (2025, 2024, etc)
genero_selecionado = st.sidebar.multiselect("Gênero", genero_disponivel, default=genero_disponivel)

# Filtro de Periodo
periodo_disponivel = sorted(df['periodo_check_in'].unique())
periodo_selecionado = st.sidebar.multiselect("Período", periodo_disponivel, default=periodo_disponivel)

# Filtro Status
status_disponivel = sorted(df['status_presenca'].unique())
status_selecionado = st.sidebar.multiselect("Status", status_disponivel, default=status_disponivel)

# Filtro Inscrição
inscricao_disponivel = sorted(df['tipo_inscricao'].unique())
inscricao_selecionada = st.sidebar.multiselect("Tipo de inscrição", inscricao_disponivel, default=inscricao_disponivel)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
# Ou seja, a filtragem é aplicada
df_filtrado = df[
    (df['genero'].isin(genero_selecionado)) &
    (df['periodo_check_in'].isin(periodo_selecionado)) &
    (df['status_presenca'].isin(status_selecionado)) &
    (df['tipo_inscricao'].isin(inscricao_selecionada))
]

# --- Conteúdo Principal ---
st.title("🛠️ Dashboard da Análise das Atividades de Treinamento")
st.markdown("Veja pelos gráficos os principais dados das atividades de treinamento desta academia.")

# --- Métricas principais ---
st.subheader("📊 Métricas gerais da Academia")

if not df_filtrado.empty:
    total_visitas = len(df_filtrado)
    quantidade_presente = (df_filtrado['status_presenca'] == 'Presente').sum()
    taxa_comparecimento = (quantidade_presente / total_visitas) * 100

    media_caloria = df_filtrado['calorias_queimadas'].mean()
    media_tempo = df_filtrado['tempo_treino_minutos'].mean()
else:
    total_visitas, taxa_comparecimento, media_caloria, media_tempo = 0, 0, 0, 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de visitas: ", total_visitas)
col2.metric("Taxa de comparecimento", f"%{taxa_comparecimento:.2f}")
col3.metric("Média de tempo de treino", f"{media_tempo:.2f}")
col4.metric("Média de calorias queimadas", f"{media_caloria:.2f}")

st.markdown("---")

# --- Gráficos ---
st.subheader("📈 Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        df_quantidade_pessoa = df_filtrado['genero'].value_counts().reset_index()
        df_quantidade_pessoa.columns = ['genero', 'quantidade']
        df_quantidade_pessoa = df_quantidade_pessoa.sort_values(by='quantidade', ascending=False)

        grafico_genero = px.bar(df_quantidade_pessoa,
                    x='genero',
                    y='quantidade',
                    title='Distribuição de pessoas por gênero',
                    labels={'genero': 'Gênero', 'quantidade': 'Quantidade de Pessoas'},
                    color='genero',
                    color_discrete_sequence=px.colors.qualitative.Pastel
                    )

        grafico_genero.update_layout(xaxis_title='Gênero', yaxis_title='Quantidade de pessoas')
        st.plotly_chart(grafico_genero, width='stretch')
    else:
        st.warning("Não há nenhum dado para exibir")

with col_graf2:
        if not df_filtrado.empty:
            df_quantidade_idade = df_filtrado['idade'].value_counts().reset_index()
            df_quantidade_idade.columns = ['idade', 'quantidade']
            df_quantidade_idade = df_quantidade_idade.sort_values(by='quantidade', ascending=False)

            grafico_idade = px.bar(df_quantidade_idade,
                        x='idade',
                        y='quantidade',
                        title='Distribuição etária',
                        labels={'idade': 'Idade', 'quantidade': 'Quantidade de Pessoas'},
                        color='idade',
                        color_discrete_sequence=px.colors.qualitative.Pastel
                        )

            grafico_idade.update_layout(xaxis_title='Idade', yaxis_title='Quantidade de pessoas')
            st.plotly_chart(grafico_idade, width='stretch')
        else:
            st.warning("Não há nenhum dado para exibir")            

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        df_quantidade_inscricao = df_filtrado['tipo_inscricao'].value_counts().reset_index()
        df_quantidade_inscricao.columns = ['tipo_inscricao', 'quantidade']
        df_quantidade_inscricao = df_quantidade_inscricao.sort_values(by='quantidade', ascending=False)

        grafico_inscricao = px.pie(df_quantidade_inscricao,
                    names='tipo_inscricao',
                    values='quantidade',
                    title='Proporção dos tipos de inscrição',
                    color='tipo_inscricao',
                    labels={'tipo_inscricao': 'Tipo de inscrição', 'quantidade': 'Quantidade de inscrições'},
                    color_discrete_sequence=px.colors.qualitative.Pastel1
                    )

        grafico_inscricao.update_layout(xaxis_title='Idade', yaxis_title='Quantidade de pessoas')
        grafico_inscricao.update_traces(textinfo='percent+label')
        st.plotly_chart(grafico_inscricao, width='stretch')
    else:
        st.warning("Não há nenhum dado para exibir")

with col_graf4:
    if not df_filtrado.empty:
        df_quantidade_periodo = df_filtrado['periodo_check_in'].value_counts().reset_index()
        df_quantidade_periodo.columns = ['periodo', 'quantidade']
        df_quantidade_periodo = df_quantidade_periodo.sort_values(by='quantidade', ascending=False)

        grafico_periodo = px.pie(df_quantidade_periodo,
                    names='periodo',
                    values='quantidade',
                    title='Distribuição de Check-ins por Período do Dia',
                    labels={'periodo': 'Período do Dia', 'quantidade': 'Quantidade de Check-ins'},
                    color='periodo',
                    color_discrete_sequence=px.colors.qualitative.Pastel
                    )

        grafico_periodo.update_layout(xaxis_title='Período do Dia', yaxis_title='Quantidade de Check-ins')
        st.plotly_chart(grafico_periodo, width='stretch')
    else:
        st.warning("Não há nenhum dado para exibir")

if not df_filtrado.empty:
    df_quantidade_treino = df_filtrado['tipo_treino'].value_counts().reset_index()
    df_quantidade_treino.columns = ['tipo_treino', 'quantidade']
    df_quantidade_treino = df_quantidade_treino.sort_values(by='quantidade', ascending=False)

    grafico_treino = px.bar(df_quantidade_treino,
                    x='tipo_treino',
                    y='quantidade',
                    title='Distribuição de Treinos',
                    labels={'tipo_treino': 'Tipo de treino', 'quantidade': 'Quantidade de Pessoas', 'caloria_media_treino': 'Calorias queimadas em média'},
                    color='tipo_treino',
                    color_discrete_sequence=px.colors.qualitative.Pastel
                    )

    grafico_treino.update_layout(xaxis_title='Tipo de treino', yaxis_title='Quantidade de Pessoas')
    st.plotly_chart(grafico_treino, width='stretch')
else:
    st.warning("Não há nenhum dado para exibir")

# --- Base de dados ---
st.subheader("ℹ️ Dados da Academia")
st.dataframe(df)