# 🌤️ Dashboard Meteorológico - São José dos Campos-SP

## Descrição do Projeto

Este projeto desenvolve uma análise de dados meteorológicos em escala utilizando dados do INMET (Instituto Nacional de Meteorologia) para o município de São José dos Campos-SP. O projeto inclui coleta automatizada de dados, análise com machine learning e uma interface web interativa para visualização dos resultados.

## 🎯 Objetivos

- Coletar e processar dados meteorológicos históricos
- Implementar análises estatísticas e modelos de machine learning
- Criar um dashboard interativo para visualização dos dados
- Preparar o projeto para deploy em produção

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Streamlit** - Framework para criação do dashboard
- **Pandas** - Manipulação e análise de dados
- **Scikit-learn** - Machine learning
- **Plotly** - Visualizações interativas
- **Matplotlib/Seaborn** - Gráficos estáticos

## 📁 Estrutura do Projeto

```
projeto-meteorologia-sjc/
├── app.py                      # Aplicação principal do Streamlit
├── data_collector.py           # Script para coleta de dados do INMET
├── generate_sample_data.py     # Gerador de dados de exemplo
├── data_analysis.py           # Análises e machine learning
├── requirements.txt           # Dependências do projeto
├── README.md                 # Este arquivo
├── data/                     # Diretório de dados
│   ├── *.csv                # Arquivos CSV com dados meteorológicos
│   └── *.png                # Gráficos gerados
└── .streamlit/              # Configurações do Streamlit (opcional)
```

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd projeto-meteorologia-sjc

# Instale as dependências
pip install -r requirements.txt
```

### 3. Geração de Dados (Exemplo)

```bash
# Execute o script para gerar dados de exemplo
python generate_sample_data.py
```

### 4. Executar o Dashboard

```bash
# Execute o dashboard Streamlit
streamlit run app.py
```

O dashboard estará disponível em `http://localhost:8501`

## 📊 Funcionalidades do Dashboard

### Métricas Principais
- Temperatura média, máxima e mínima
- Umidade relativa média
- Precipitação total acumulada
- Velocidade média do vento

### Visualizações Interativas
- Gráfico temporal de temperaturas
- Análise de precipitação diária
- Evolução da umidade relativa
- Distribuições estatísticas

### Machine Learning
- Modelo de regressão linear para previsão de temperatura
- Métricas de avaliação (MSE, R²)
- Visualização de predições vs. valores reais

### Filtros e Interatividade
- Filtro por período de datas
- Seleção de variáveis para análise
- Download de dados em CSV
- Interface responsiva

## 🔬 Análise de Dados

O projeto implementa as seguintes análises:

1. **Estatísticas Descritivas**: Média, mediana, desvio padrão, quartis
2. **Análise Temporal**: Tendências e sazonalidade
3. **Machine Learning**: Modelo preditivo para temperatura
4. **Visualizações**: Gráficos interativos e estáticos

## 📈 Modelo de Machine Learning

- **Algoritmo**: Regressão Linear
- **Features**: Mês e dia do ano
- **Target**: Temperatura média
- **Métricas**: MSE (Erro Quadrático Médio) e R² Score

## 🌐 Deploy

### Streamlit Cloud

1. Faça upload do projeto para o GitHub
2. Conecte sua conta do Streamlit Cloud ao GitHub
3. Selecione o repositório e o arquivo `app.py`
4. Configure as variáveis de ambiente se necessário
5. Deploy automático!

### Outras Plataformas

O projeto também pode ser deployado em:
- Heroku
- Railway
- Render
- Google Cloud Platform
- AWS

## 📝 Coleta de Dados Reais

Para usar dados reais do INMET:

1. Execute o script `data_collector.py`
2. Os dados serão baixados automaticamente do portal do INMET
3. Os arquivos CSV serão processados e filtrados para São José dos Campos
4. Substitua os dados de exemplo pelos dados reais no dashboard

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- Seu Nome - Desenvolvimento inicial

## 🙏 Agradecimentos

- INMET - Instituto Nacional de Meteorologia pelos dados
- Streamlit - Framework para criação do dashboard
- Comunidade Python - Pelas bibliotecas utilizadas

---

**Nota**: Este projeto foi desenvolvido para fins educacionais e de demonstração. Os dados de exemplo são simulados e não representam medições reais.

