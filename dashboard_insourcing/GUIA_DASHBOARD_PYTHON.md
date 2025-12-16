# 🚀 GUIA DO DASHBOARD PYTHON - Plug and Play!

## ✅ DASHBOARD PRONTO PARA USAR!

Criei um **dashboard interativo completo** em Python com Plotly Dash. Ele já está funcionando com os dados fictícios carregados!

---

## 🎯 O QUE VOCÊ TEM

### ✅ **Dashboard Completo com 5 Páginas**

1. **📈 Resumo Executivo**
   - 9 cards de KPIs principais
   - Gráfico de evolução temporal
   - Comparativo B2C vs B2B
   - Tabela de performance por gerente

2. **✅ Qualidade**
   - 5 KPIs de qualidade
   - 4 gráficos de evolução
   - Top 10 cidades por qualidade

3. **⚙️ Produção**
   - 6 KPIs de produção
   - Gráfico de evolução TMA e Ocupação
   - Gauge de ocupação

4. **💼 Negócios**
   - 5 KPIs de negócios
   - Funil de conversão
   - Evolução de conversão e instalações

5. **💰 Financeiro**
   - 5 KPIs financeiros
   - Evolução Receita vs Custo
   - Composição de custos (pizza)
   - Margem por operação

### ✅ **Filtros Interativos Globais**

- **Período:** Seletor de data (início e fim)
- **Operação:** B2C, B2B ou Todas
- **Cidade:** Filtro por cidade específica ou todas
- **Gerente:** Filtro por gerente específico ou todos
- **Granularidade:** Diário, Semanal ou Mensal

### ✅ **Recursos**

- ✅ Responsivo (funciona em mobile)
- ✅ Interativo (clique, zoom, hover)
- ✅ Dados fictícios já carregados (64.000+ registros)
- ✅ Atualização em tempo real ao mudar filtros
- ✅ Design profissional com Bootstrap
- ✅ Gráficos de alta qualidade com Plotly

---

## 🌐 ACESSAR O DASHBOARD

### **OPÇÃO 1: Acesso Online (Recomendado)**

**URL Pública:**
```
https://8050-ida9u9oq3h63xa2eo6g41-e7df869f.manusvm.computer
```

✅ Acesse agora mesmo no seu navegador!  
✅ Funciona em qualquer dispositivo (PC, tablet, celular)  
✅ Não precisa instalar nada

### **OPÇÃO 2: Rodar Localmente**

Se quiser rodar no seu computador:

**1. Instalar dependências:**
```bash
pip install dash dash-bootstrap-components plotly pandas
```

**2. Executar o dashboard:**
```bash
cd dashboard_insourcing
python dashboard_app.py
```

**3. Acessar no navegador:**
```
http://localhost:8050
```

---

## 📊 COMO USAR O DASHBOARD

### **1. Navegar entre as Páginas**

Clique nas abas no topo:
- 📈 Resumo Executivo
- ✅ Qualidade
- ⚙️ Produção
- 💼 Negócios
- 💰 Financeiro

### **2. Aplicar Filtros**

Use os filtros no topo da página:

**Exemplo 1: Ver apenas B2C de São Paulo**
- Operação: B2C
- Cidade: São Paulo
- Deixe os outros filtros como estão

**Exemplo 2: Ver último mês**
- Período: Selecione o último mês
- Granularidade: Diário

**Exemplo 3: Ver performance de um gerente**
- Gerente: Selecione o nome do gerente
- Granularidade: Mensal

### **3. Interagir com os Gráficos**

- **Hover:** Passe o mouse sobre os gráficos para ver detalhes
- **Zoom:** Clique e arraste para dar zoom
- **Pan:** Segure Shift e arraste para mover
- **Reset:** Clique duas vezes para resetar o zoom
- **Download:** Clique no ícone de câmera para baixar como PNG

### **4. Analisar os KPIs**

- **Verde:** Meta atingida ✅
- **Laranja:** Atenção necessária ⚠️
- **Vermelho:** Crítico 🚨

---

## 🎨 PERSONALIZAR O DASHBOARD

### **Alterar Cores**

Edite o arquivo `dashboard_app.py`, seção `COLORS`:

```python
COLORS = {
    'primary': '#0078d4',     # Azul principal
    'secondary': '#1e3a5f',   # Azul escuro
    'success': '#28a745',     # Verde
    'warning': '#fd7e14',     # Laranja
    'danger': '#dc3545',      # Vermelho
    'light': '#f5f5f5',       # Cinza claro
    'dark': '#333333',        # Cinza escuro
    'text': '#666666'         # Texto
}
```

### **Adicionar Novos KPIs**

1. Abra `dashboard_app.py`
2. Localize a função da página (ex: `criar_pagina_resumo`)
3. Adicione um novo card:

```python
dbc.Col(criar_card_kpi("Novo KPI", valor, meta, 'percentual'), width=2)
```

### **Adicionar Novos Gráficos**

Exemplo de gráfico de barras:

```python
fig = go.Figure(data=[
    go.Bar(x=df['Categoria'], y=df['Valor'], marker_color=COLORS['primary'])
])
fig.update_layout(title='Meu Gráfico', template=PLOTLY_TEMPLATE)
```

Adicione ao layout:

```python
dbc.Col([
    dcc.Graph(figure=fig)
], width=6)
```

---

## 🔄 CONECTAR AOS DADOS REAIS

### **Opção 1: Substituir os CSVs**

1. Substitua os arquivos na pasta `data/` pelos seus dados reais
2. Mantenha os mesmos nomes de arquivo e estrutura de colunas
3. Reinicie o dashboard

### **Opção 2: Conectar ao Banco de Dados**

Edite a seção `CARREGAR DADOS` em `dashboard_app.py`:

```python
import sqlalchemy

# Criar conexão
engine = sqlalchemy.create_engine('postgresql://user:pass@host:port/db')

# Carregar dados
df_fato = pd.read_sql('SELECT * FROM fato_metricas_diarias', engine)
df_calendario = pd.read_sql('SELECT * FROM dim_calendario', engine)
# ... outros
```

### **Opção 3: Atualização Automática**

Adicione um intervalo de atualização:

```python
app.layout = dbc.Container([
    # ... layout existente ...
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Atualiza a cada 60 segundos
        n_intervals=0
    )
])

@callback(
    Output('conteudo-pagina', 'children'),
    Input('interval-component', 'n_intervals')
)
def atualizar_automatico(n):
    # Recarregar dados
    df = carregar_dados()
    return criar_pagina_atual(df)
```

---

## 📤 PUBLICAR O DASHBOARD

### **Opção 1: Heroku (Gratuito)**

1. Crie uma conta no Heroku
2. Instale o Heroku CLI
3. Crie um arquivo `requirements.txt`:
```
dash
dash-bootstrap-components
plotly
pandas
gunicorn
```

4. Crie um arquivo `Procfile`:
```
web: gunicorn dashboard_app:server
```

5. Deploy:
```bash
heroku create meu-dashboard-kpis
git push heroku main
```

### **Opção 2: Render (Gratuito)**

1. Crie uma conta no Render
2. Conecte seu repositório GitHub
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn dashboard_app:server`

### **Opção 3: AWS/Azure/GCP**

Use serviços como:
- AWS Elastic Beanstalk
- Azure App Service
- Google Cloud Run

---

## 🔧 SOLUÇÃO DE PROBLEMAS

### "Erro ao carregar dados"

**Causa:** Arquivos CSV não encontrados

**Solução:**
- Verifique se a pasta `data/` está no mesmo diretório do `dashboard_app.py`
- Verifique se todos os 8 arquivos CSV estão presentes

### "Dashboard não inicia"

**Causa:** Dependências não instaladas

**Solução:**
```bash
pip install dash dash-bootstrap-components plotly pandas
```

### "Gráficos não aparecem"

**Causa:** Dados vazios após filtros

**Solução:**
- Limpe os filtros (selecione "Todas/Todos")
- Verifique se há dados no período selecionado

### "Erro de porta já em uso"

**Causa:** Porta 8050 ocupada

**Solução:**
- Mude a porta em `dashboard_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8051)
```

---

## 📊 ESTRUTURA DO CÓDIGO

```
dashboard_app.py
├── Importações
├── Carregar Dados (linhas 20-40)
├── Configurações de Estilo (linhas 45-70)
├── Funções Auxiliares (linhas 75-120)
│   ├── calcular_kpi()
│   ├── criar_card_kpi()
│   └── status_kpi()
├── Inicializar App (linha 125)
├── Layout Principal (linhas 130-200)
│   ├── Header
│   ├── Filtros Globais
│   ├── Tabs
│   └── Footer
├── Callbacks (linhas 205-250)
│   └── atualizar_pagina()
└── Páginas (linhas 255-680)
    ├── criar_pagina_resumo()
    ├── criar_pagina_qualidade()
    ├── criar_pagina_producao()
    ├── criar_pagina_negocios()
    └── criar_pagina_financeiro()
```

---

## 💡 DICAS AVANÇADAS

### **1. Adicionar Autenticação**

Use `dash-auth`:

```python
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'senha123'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
```

### **2. Adicionar Cache**

Use `flask-caching`:

```python
from flask_caching import Cache

cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple'
})

@cache.memoize(timeout=300)
def carregar_dados():
    # ... código de carregamento
```

### **3. Adicionar Exportação**

Adicione botões de download:

```python
html.Button("Download CSV", id="btn-download"),
dcc.Download(id="download-dataframe-csv")

@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def download_csv(n_clicks):
    return dcc.send_data_frame(df.to_csv, "dados.csv")
```

---

## 🎉 PRONTO PARA USAR!

O dashboard está **100% funcional** e pronto para uso!

**Acesse agora:**
```
https://8050-ida9u9oq3h63xa2eo6g41-e7df869f.manusvm.computer
```

**Recursos disponíveis:**
- ✅ 5 páginas completas
- ✅ 25+ KPIs monitorados
- ✅ 15+ gráficos interativos
- ✅ Filtros globais funcionando
- ✅ Dados fictícios carregados (64.000+ registros)
- ✅ Design profissional
- ✅ Responsivo (mobile-friendly)

**Próximos passos:**
1. Acesse o dashboard e explore
2. Teste os filtros e navegação
3. Quando estiver satisfeito, substitua pelos dados reais
4. Publique em produção (Heroku, Render, etc.)

---

**Boa análise! 📊✨**
