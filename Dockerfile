# Use uma imagem base oficial do Python 3.11
FROM python:3.11-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do Python
# --no-cache-dir: Evita o cache de pacotes para reduzir o tamanho da imagem
# --upgrade pip: Garante que o pip esteja atualizado
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da sua aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que o Streamlit usa (padrão é 8501)
EXPOSE 8501

# Define o comando para iniciar o aplicativo Streamlit
# --server.port 8501: Garante que o Streamlit rode na porta esperada
# --server.enableCORS false: Desabilita CORS para evitar problemas em alguns ambientes
# --server.enableXsrfProtection false: Desabilita proteção XSRF para evitar problemas em alguns ambientes
CMD streamlit run app.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false
