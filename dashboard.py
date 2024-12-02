import pandas as pd
import streamlit as st
import requests
from io import BytesIO
import plotly.express as px

# URL do arquivo no GitHub
url_dados = r"https://raw.githubusercontent.com/luceliofranca/DASHBOARD_CR2/8d499ab07ec35590da94c2f289a14b92ae3f5082/df_consolidado.xlsx"

# Tentar carregar o arquivo Excel
try:
    # Fazer o download do arquivo
    response = requests.get(url_dados)
    response.raise_for_status()  # Verificar erros no download

    # Abrir o arquivo com Pandas
    df = pd.read_excel(BytesIO(response.content), engine="openpyxl")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# Título do Dashboard
st.title("DASHBOARD CR 2 PMMT")

# Exibir os Dados
st.subheader("Dados Carregados")
st.dataframe(df)

# Gráfico de Barras: Distribuição por Tipo de Veículo
if 'TIPO DO VEICULO' in df.columns:
    st.subheader("Distribuição por Tipo de Veículo")
    tipo_veiculo_contagem = df['TIPO DO VEICULO'].value_counts()
    st.bar_chart(tipo_veiculo_contagem)
else:
    st.warning("Coluna 'TIPO DO VEICULO' não encontrada nos dados.")

# Gráfico de Linha: Tendência Temporal
if 'DATA' in df.columns:
    # Converter a coluna de data para datetime
    df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')
    tendencia = df.groupby(df['DATA'].dt.to_period('M')).size()

    st.subheader("Tendência Temporal")
    st.line_chart(tendencia)
else:
    st.warning("Coluna 'DATA' não encontrada nos dados.")

# Gráfico de "FURTO POR DIA DA SEMANA"
if 'DIA DA SEMANA' in df.columns and 'TIPIFICAÇÃO' in df.columns:
    st.subheader("Furto por Dia da Semana")
    df_furto_roubo = df[df['TIPIFICAÇÃO'].isin(['FURTO', 'ROUBO'])]
    furto_roubo_semana = df_furto_roubo.groupby(['DIA DA SEMANA', 'TIPIFICAÇÃO']).size().reset_index(name='Quantidade')

    # Gráfico interativo
    fig = px.bar(
        furto_roubo_semana,
        x='DIA DA SEMANA',
        y='Quantidade',
        color='TIPIFICAÇÃO',
        barmode='group',
        title="Roubos e Furtos por Dia da Semana",
        labels={'DIA DA SEMANA': 'Dia da Semana', 'Quantidade': 'Quantidade'}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Colunas 'DIA DA SEMANA' ou 'TIPIFICAÇÃO' não encontradas nos dados.")

# Gráfico de "ROUBO E FURTO POR MÊS"
if 'DATA' in df.columns and 'CIDADE' in df.columns and 'TIPIFICAÇÃO' in df.columns:
    st.subheader("Roubos e Furtos por Mês")
    df['MES'] = df['DATA'].dt.to_period('M').astype(str)
    furto_roubo_mes = df[df['TIPIFICAÇÃO'].isin(['FURTO', 'ROUBO'])].groupby(['MES', 'CIDADE', 'TIPIFICAÇÃO']).size().reset_index(name='Quantidade')

    # Gráfico de barras
    fig_bar = px.bar(
        furto_roubo_mes,
        x='MES',
        y='Quantidade',
        color='TIPIFICAÇÃO',
        facet_col='CIDADE',
        title="Roubos e Furtos por Mês (Barras)",
        labels={'MES': 'Mês', 'Quantidade': 'Quantidade'},
        height=600
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico de linha
    fig_line = px.line(
        furto_roubo_mes,
        x='MES',
        y='Quantidade',
        color='TIPIFICAÇÃO',
        line_group='CIDADE',
        title="Roubos e Furtos por Mês (Linhas)",
        labels={'MES': 'Mês', 'Quantidade': 'Quantidade'},
        height=600
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Minha sugestão: Heatmap
    heatmap_data = furto_roubo_mes.pivot_table(values='Quantidade', index='MES', columns='CIDADE', aggfunc='sum', fill_value=0)
    fig_heatmap = px.imshow(
        heatmap_data,
        aspect='auto',
        title="Roubos e Furtos por Mês (Heatmap)",
        labels={'color': 'Quantidade'},
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
else:
    st.warning("Colunas 'DATA', 'CIDADE' ou 'TIPIFICAÇÃO' não encontradas nos dados.")

# Exibir Estatísticas Básicas
st.subheader("Estatísticas Descritivas")
st.write(df.describe())

