# 🚀 Instruções de Deploy - Vercel + Neon + Streamlit Cloud

## 📋 Visão Geral da Arquitetura

Esta solução utiliza:
- **Neon**: Banco de dados PostgreSQL para armazenar dados meteorológicos
- **Vercel**: Serverless Functions para coleta automática de dados do INMET
- **Streamlit Cloud**: Dashboard interativo que lê dados do Neon

## 🗄️ Parte 1: Configuração do Banco de Dados Neon

### 1.1 Preparar o Banco de Dados

1. **Acesse o Console Neon**: [https://console.neon.tech](https://console.neon.tech)
2. **Selecione seu projeto** ou crie um novo
3. **Copie sua string de conexão** (algo como: `postgresql://user:pass@host:port/db`)

### 1.2 Configurar o Banco Localmente

1. **Instale as dependências**:
```bash
pip install psycopg2-binary pandas numpy
```

2. **Configure a variável de ambiente**:
```bash
# Linux/macOS
export DATABASE_URL="sua_string_de_conexao_aqui"

# Windows
set DATABASE_URL=sua_string_de_conexao_aqui
```

3. **Execute o script de configuração**:
```bash
python setup_database.py
```

Este script irá:
- Criar a tabela `dados_meteorologicos`
- Inserir dados de exemplo dos últimos 2 anos
- Criar índices para melhor performance

## ⚡ Parte 2: Deploy da Função de Coleta no Vercel

### 2.1 Preparar os Arquivos

Certifique-se de que você tem estes arquivos no seu repositório:
- `api/collect-data.py` (função serverless)
- `vercel.json` (configuração do Vercel)
- `requirements-vercel.txt` (dependências)

### 2.2 Deploy no Vercel

1. **Acesse o Vercel**: [https://vercel.com](https://vercel.com)
2. **Faça login** com sua conta GitHub
3. **Clique em "New Project"**
4. **Selecione seu repositório** `dashboard-meteorologico-sjc`
5. **Configure as variáveis de ambiente**:
   - Vá para "Settings" > "Environment Variables"
   - Adicione: `DATABASE_URL` = `sua_string_de_conexao_neon`
6. **Clique em "Deploy"**

### 2.3 Configurar Cron Job (Coleta Automática)

O arquivo `vercel.json` já está configurado para executar a coleta diariamente às 6h da manhã:

```json
{
  "crons": [
    {
      "path": "/api/collect-data",
      "schedule": "0 6 * * *"
    }
  ]
}
```

### 2.4 Testar a Função

Após o deploy, teste a função acessando:
`https://seu-projeto.vercel.app/api/collect-data`

## ☁️ Parte 3: Deploy do Dashboard no Streamlit Cloud

### 3.1 Atualizar o Repositório GitHub

1. **Substitua o `app.py`** pelo `app_neon.py`:
```bash
# No seu repositório local
mv app_neon.py app.py
git add app.py
git commit -m "Atualiza dashboard para usar Neon"
git push origin main
```

2. **Atualize o `requirements.txt`**:
```txt
pandas
streamlit
scikit-learn
matplotlib
seaborn
plotly
psycopg2-binary
```

### 3.2 Configurar Secrets no Streamlit Cloud

1. **Acesse o Streamlit Cloud**: [https://share.streamlit.io](https://share.streamlit.io)
2. **Vá para sua aplicação** (ou crie uma nova)
3. **Clique em "Settings" > "Secrets"**
4. **Adicione o secret**:
```toml
DATABASE_URL = "sua_string_de_conexao_neon"
```

### 3.3 Deploy/Redeploy

1. Se é uma nova aplicação:
   - Repository: `seu-usuario/dashboard-meteorologico-sjc`
   - Branch: `main`
   - Main file: `app.py`

2. Se já existe, ela será atualizada automaticamente após o push

## 🔄 Parte 4: Fluxo de Funcionamento

### Coleta Automática de Dados
1. **Diariamente às 6h**: Vercel executa `/api/collect-data`
2. **Script baixa dados** do INMET do ano atual
3. **Filtra dados** de São José dos Campos
4. **Salva no Neon** (evita duplicatas)

### Dashboard em Tempo Real
1. **Usuário acessa** o dashboard Streamlit
2. **App conecta ao Neon** e carrega dados atualizados
3. **Exibe métricas** e gráficos em tempo real
4. **Cache de 1 hora** para melhor performance

## 🛠️ Parte 5: Comandos Úteis

### Verificar Dados no Neon
```sql
-- Contar registros
SELECT COUNT(*) FROM dados_meteorologicos;

-- Últimos 10 registros
SELECT * FROM dados_meteorologicos 
ORDER BY data DESC 
LIMIT 10;

-- Dados por ano
SELECT EXTRACT(YEAR FROM data) as ano, COUNT(*) 
FROM dados_meteorologicos 
GROUP BY ano 
ORDER BY ano;
```

### Logs do Vercel
1. Acesse o dashboard do Vercel
2. Vá para "Functions" > "collect-data"
3. Veja logs de execução e erros

### Atualizar Dados Manualmente
Acesse: `https://seu-projeto.vercel.app/api/collect-data`

## 🐛 Solução de Problemas

### Erro de Conexão com Neon
- Verifique se a string de conexão está correta
- Confirme que o banco está ativo (Neon hiberna após inatividade)
- Teste a conexão localmente primeiro

### Função Vercel não Executa
- Verifique os logs no dashboard do Vercel
- Confirme que `DATABASE_URL` está configurada
- Teste a função manualmente via URL

### Dashboard não Carrega Dados
- Verifique se `DATABASE_URL` está nos secrets do Streamlit
- Confirme que a tabela existe e tem dados
- Use o botão "Atualizar Dados" no dashboard

### Timeout na Coleta
- A coleta pode demorar alguns minutos
- Vercel tem limite de 10s para hobby plan
- Considere upgrade ou otimização do script

## 📊 Monitoramento

### Métricas Importantes
- **Registros no banco**: Quantos dados foram coletados
- **Última atualização**: Quando foi a última coleta
- **Erros de coleta**: Falhas na função Vercel
- **Performance do dashboard**: Tempo de carregamento

### Alertas Recomendados
- Falha na coleta diária
- Banco de dados offline
- Dashboard com erro

## 🎉 Resultado Final

Após seguir todos os passos, você terá:

✅ **Coleta automática** de dados do INMET diariamente  
✅ **Banco de dados** robusto e escalável no Neon  
✅ **Dashboard interativo** sempre atualizado  
✅ **Arquitetura serverless** sem custos de servidor  
✅ **Dados históricos** desde 2000 (conforme disponibilidade)  

**URLs Finais:**
- Dashboard: `https://seu-app.streamlit.app`
- API de Coleta: `https://seu-projeto.vercel.app/api/collect-data`
- Banco de Dados: Console Neon

---

**Dica**: Salve todas as URLs e credenciais em um local seguro!

