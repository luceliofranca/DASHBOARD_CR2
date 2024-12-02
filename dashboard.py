import streamlit as st
import pandas as pd

# Caminho do arquivo Excel
caminho_dados = r"C:\Users\franc\OneDrive\2024\TRABALHO CR2\ARI CR2\DASHBOARD\df_consolidado.xlsx"

# Carregar os dados do Excel
try:
    df = pd.read_excel(caminho_dados)
except FileNotFoundError:
    st.error(f"Arquivo Excel não encontrado no caminho: {caminho_dados}")
    st.stop()

# Título do Dashboard
st.title("Dashboard Interativo com Streamlit")

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

# Gráfico de Dispersão (exemplo de análise adicional)
if 'HORA' in df.columns and 'TIPO DE LOCAL' in df.columns:
    st.subheader("Relação entre Hora e Tipo de Local")
    st.write("Gráfico interativo entre as colunas 'HORA' e 'TIPO DE LOCAL'.")
    st.scatter_chart(data=df, x='HORA', y='TIPO DE LOCAL')
else:
    st.warning("Colunas 'HORA' ou 'TIPO DE LOCAL' não encontradas nos dados.")

# Exibir Estatísticas Básicas
st.subheader("Estatísticas Descritivas")
st.write(df.describe())