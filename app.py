import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard Meteorológico - São Luiz do Paraitinga",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🌤️ Dashboard Meteorológico - São Luiz do Paraitinga-SP")
st.markdown("---")

# Função para carregar dados
@st.cache_data
def load_data():
    """Carrega os dados meteorológicos"""
    file_path = "data/inmet_data_sao_luiz_do_paraitinga_combined.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['DATA'] = pd.to_datetime(df['DATA'])
        return df
    else:
        st.error("Arquivo de dados não encontrado!")
        return None

# Função para análise de machine learning
@st.cache_data
def run_ml_analysis(df):
    """Executa análise de machine learning"""
    df_ml = df.copy()
    df_ml['MES'] = df_ml['DATA'].dt.month
    df_ml['DIA_DO_ANO'] = df_ml['DATA'].dt.dayofyear
    
    features = ['MES', 'DIA_DO_ANO']
    target = 'TEMPERATURA_MEDIA'
    
    df_ml = df_ml.dropna(subset=features + [target])
    
    X = df_ml[features]
    y = df_ml[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return model, mse, r2, X_test, y_test, y_pred

# Carregar dados
df = load_data()

if df is not None:
    # Sidebar com filtros
    st.sidebar.header("🔧 Filtros")
    
    # Filtro de data
    min_date = df['DATA'].min().date()
    max_date = df['DATA'].max().date()
    
    date_range = st.sidebar.date_input(
        "Selecione o período:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Aplicar filtro de data
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['DATA'].dt.date >= start_date) & (df['DATA'].dt.date <= end_date)]
    else:
        df_filtered = df
    
    # Métricas principais
    st.header("📊 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp_media = df_filtered['TEMPERATURA_MEDIA'].mean()
        st.metric("Temperatura Média", f"{temp_media:.1f}°C")
    
    with col2:
        umidade_media = df_filtered['UMIDADE_RELATIVA'].mean()
        st.metric("Umidade Média", f"{umidade_media:.1f}%")
    
    with col3:
        precip_total = df_filtered['PRECIPITACAO'].sum()
        st.metric("Precipitação Total", f"{precip_total:.1f}mm")
    
    with col4:
        vento_medio = df_filtered['VELOCIDADE_VENTO'].mean()
        st.metric("Velocidade do Vento", f"{vento_medio:.1f}m/s")
    
    st.markdown("---")
    
    # Gráficos principais
    st.header("📈 Análise Temporal")
    
    # Gráfico de temperatura ao longo do tempo
    fig_temp = px.line(
        df_filtered, 
        x='DATA', 
        y=['TEMPERATURA_MAXIMA', 'TEMPERATURA_MINIMA', 'TEMPERATURA_MEDIA'],
        title="Evolução da Temperatura ao Longo do Tempo",
        labels={'value': 'Temperatura (°C)', 'DATA': 'Data'}
    )
    fig_temp.update_layout(height=400)
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Gráficos em duas colunas
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de precipitação
        fig_precip = px.bar(
            df_filtered, 
            x='DATA', 
            y='PRECIPITACAO',
            title="Precipitação Diária",
            labels={'PRECIPITACAO': 'Precipitação (mm)', 'DATA': 'Data'}
        )
        fig_precip.update_layout(height=400)
        st.plotly_chart(fig_precip, use_container_width=True)
    
    with col2:
        # Gráfico de umidade
        fig_umidade = px.line(
            df_filtered, 
            x='DATA', 
            y='UMIDADE_RELATIVA',
            title="Umidade Relativa ao Longo do Tempo",
            labels={'UMIDADE_RELATIVA': 'Umidade (%)', 'DATA': 'Data'}
        )
        fig_umidade.update_layout(height=400)
        st.plotly_chart(fig_umidade, use_container_width=True)
    
    st.markdown("---")
    
    # Análise de Machine Learning
    st.header("🤖 Análise de Machine Learning")
    
    if st.button("Executar Análise de ML"):
        with st.spinner("Executando análise..."):
            model, mse, r2, X_test, y_test, y_pred = run_ml_analysis(df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Erro Quadrático Médio (MSE)", f"{mse:.2f}")
                st.metric("R² Score", f"{r2:.3f}")
            
            with col2:
                # Gráfico de predição vs real
                fig_ml = go.Figure()
                fig_ml.add_trace(go.Scatter(
                    x=y_test, 
                    y=y_pred,
                    mode='markers',
                    name='Predições',
                    marker=dict(color='blue', opacity=0.6)
                ))
                
                # Linha de referência (predição perfeita)
                min_val = min(y_test.min(), y_pred.min())
                max_val = max(y_test.max(), y_pred.max())
                fig_ml.add_trace(go.Scatter(
                    x=[min_val, max_val], 
                    y=[min_val, max_val],
                    mode='lines',
                    name='Predição Perfeita',
                    line=dict(color='red', dash='dash')
                ))
                
                fig_ml.update_layout(
                    title="Predição vs. Temperatura Real",
                    xaxis_title="Temperatura Real (°C)",
                    yaxis_title="Temperatura Predita (°C)",
                    height=400
                )
                
                st.plotly_chart(fig_ml, use_container_width=True)
    
    st.markdown("---")
    
    # Estatísticas descritivas
    st.header("📋 Estatísticas Descritivas")
    
    # Seletor de variável
    variavel = st.selectbox(
        "Selecione a variável para análise:",
        ['TEMPERATURA_MEDIA', 'TEMPERATURA_MAXIMA', 'TEMPERATURA_MINIMA', 
         'UMIDADE_RELATIVA', 'PRECIPITACAO', 'VELOCIDADE_VENTO', 'PRESSAO_ATMOSFERICA']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Estatísticas básicas
        st.subheader("Estatísticas Básicas")
        stats = df_filtered[variavel].describe()
        st.dataframe(stats)
    
    with col2:
        # Histograma
        fig_hist = px.histogram(
            df_filtered, 
            x=variavel,
            title=f"Distribuição de {variavel}",
            nbins=30
        )
        fig_hist.update_layout(height=300)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("---")
    
    # Dados brutos
    st.header("📄 Dados Brutos")
    
    if st.checkbox("Mostrar dados brutos"):
        st.dataframe(df_filtered)
        
        # Download dos dados
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Baixar dados como CSV",
            data=csv,
            file_name=f"dados_meteorologicos_slp_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

else:
    st.error("Não foi possível carregar os dados. Verifique se o arquivo existe no diretório 'data/'.")
    st.info("Execute primeiro o script 'generate_sample_data.py' para gerar os dados de exemplo.")

