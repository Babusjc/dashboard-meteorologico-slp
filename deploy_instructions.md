# 🚀 Instruções de Deploy - Dashboard Meteorológico

## 📋 Pré-requisitos

1. Conta no GitHub
2. Conta no Streamlit Cloud (gratuita)
3. Projeto funcionando localmente

## 🔧 Passo a Passo para Deploy no GitHub

### 1. Preparar o Repositório Local

```bash
# Inicializar repositório Git (se ainda não foi feito)
git init

# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "Initial commit: Dashboard Meteorológico São José dos Campos"
```

### 2. Criar Repositório no GitHub

1. Acesse [GitHub.com](https://github.com)
2. Clique em "New repository"
3. Nome sugerido: `dashboard-meteorologico-sjc`
4. Descrição: "Dashboard interativo para análise de dados meteorológicos de São José dos Campos-SP"
5. Marque como "Public" (necessário para Streamlit Cloud gratuito)
6. **NÃO** inicialize com README (já temos um)
7. Clique em "Create repository"

### 3. Conectar Repositório Local ao GitHub

```bash
# Adicionar origem remota (substitua SEU_USUARIO pelo seu username)
git remote add origin https://github.com/SEU_USUARIO/dashboard-meteorologico-sjc.git

# Fazer push para o GitHub
git branch -M main
git push -u origin main
```

### 4. Verificar Upload

- Acesse seu repositório no GitHub
- Verifique se todos os arquivos foram enviados:
  - `app.py`
  - `requirements.txt`
  - `README.md`
  - `data/` (com arquivos CSV)
  - `.streamlit/config.toml`

## ☁️ Deploy no Streamlit Cloud

### 1. Acessar Streamlit Cloud

1. Vá para [share.streamlit.io](https://share.streamlit.io)
2. Clique em "Sign up" ou "Sign in"
3. Use sua conta do GitHub para fazer login

### 2. Criar Nova Aplicação

1. Clique em "New app"
2. Selecione "From existing repo"
3. Preencha os campos:
   - **Repository**: `SEU_USUARIO/dashboard-meteorologico-sjc`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: `dashboard-meteorologico-sjc` (ou outro nome de sua escolha)

### 3. Configurações Avançadas (Opcional)

Clique em "Advanced settings" se necessário:

```toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

### 4. Deploy

1. Clique em "Deploy!"
2. Aguarde o processo de build (pode levar alguns minutos)
3. Sua aplicação estará disponível em: `https://SEU_APP.streamlit.app`

## 🔄 Atualizações Automáticas

Após o deploy inicial, qualquer push para o branch `main` do GitHub irá automaticamente atualizar a aplicação no Streamlit Cloud.

```bash
# Para fazer atualizações
git add .
git commit -m "Descrição da atualização"
git push origin main
```

## 🛠️ Comandos Úteis

### Verificar Status do Git
```bash
git status
```

### Ver Histórico de Commits
```bash
git log --oneline
```

### Criar Nova Branch para Desenvolvimento
```bash
git checkout -b desenvolvimento
# Fazer alterações...
git add .
git commit -m "Nova funcionalidade"
git push origin desenvolvimento
```

### Fazer Merge da Branch de Desenvolvimento
```bash
git checkout main
git merge desenvolvimento
git push origin main
```

## 🐛 Solução de Problemas

### Erro: "Requirements file not found"
- Verifique se `requirements.txt` está na raiz do projeto
- Confirme que o arquivo foi enviado para o GitHub

### Erro: "Module not found"
- Adicione a dependência faltante no `requirements.txt`
- Faça commit e push das alterações

### Erro: "File not found"
- Verifique se todos os arquivos necessários estão no repositório
- Confirme os caminhos dos arquivos no código

### App não carrega dados
- Verifique se a pasta `data/` e os arquivos CSV estão no repositório
- Execute `generate_sample_data.py` localmente antes do deploy

## 📊 Monitoramento

### Logs da Aplicação
1. Acesse o painel do Streamlit Cloud
2. Clique na sua aplicação
3. Vá para a aba "Logs" para ver erros e debug

### Métricas de Uso
- O Streamlit Cloud fornece métricas básicas de uso
- Acesse através do painel de controle da aplicação

## 🔒 Segurança

### Dados Sensíveis
- **NUNCA** commite senhas ou chaves de API
- Use variáveis de ambiente para informações sensíveis
- Configure secrets no Streamlit Cloud se necessário

### Configuração de Secrets (se necessário)
1. No painel do Streamlit Cloud
2. Vá para "Settings" > "Secrets"
3. Adicione variáveis no formato:
```toml
API_KEY = "sua_chave_aqui"
DATABASE_URL = "sua_url_aqui"
```

## 🎉 Pronto!

Após seguir estes passos, seu dashboard estará disponível publicamente na internet e será atualizado automaticamente a cada push no GitHub.

**URL da aplicação**: `https://SEU_APP.streamlit.app`

---

**Dica**: Salve a URL da sua aplicação e compartilhe com outros usuários!

