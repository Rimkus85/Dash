# 📊 Dashboard KPIs Insourcing - Vivo Fibra

Dashboard interativo para monitoramento de KPIs de operações de Insourcing B2C e B2B da Vivo.

---

## ✨ Características

- **🎨 Visual Vivo Fibra**: Design moderno com cores neon (roxo, rosa, ciano, verde, dourado)
- **📈 5 Eixos de KPIs**: Resumo, Qualidade, Produção, Negócios e Financeiro
- **🔢 38 KPIs**: Monitoramento completo de todas as métricas importantes
- **🎯 Metas Visuais**: Status de meta com cores (verde/amarelo/vermelho)
- **📊 Gráficos Interativos**: Evolução temporal com linha de meta
- **📋 Tabelas Dinâmicas**: Análise por Operação, Grupo e Gerente
- **🔍 Filtros Avançados**: Período, Operação, Grupos, Gerente e Granularidade
- **⚡ Performance**: Carregamento < 1 segundo
- **🗄️ Multi-Banco**: Suporte para SQL Server, Oracle e CSV

---

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar Dashboard (Modo CSV)

```bash
python dashboard_app_final.py
```

Acesse: **http://localhost:8050**

### 3. Configurar Banco de Dados

Veja o guia completo em: **[INSTALACAO_E_CONFIGURACAO.md](INSTALACAO_E_CONFIGURACAO.md)**

---

## 📦 Conteúdo do Projeto

```
dashboard_insourcing/
├── dashboard_app_final.py          # Aplicação principal
├── database_connector.py           # Conexão com bancos
├── kpis_completos_por_eixo.py     # Mapeamento dos 38 KPIs
├── requirements.txt                # Dependências
├── README.md                       # Este arquivo
├── INSTALACAO_E_CONFIGURACAO.md   # Guia de instalação
├── RESUMO_IMPLEMENTACAO_COMPLETA.md # Documentação técnica
│
├── assets/
│   └── logo_vivo.png              # Logo Vivo
│
├── data/
│   ├── fato_metricas_diarias.csv  # Dados (58.560 registros)
│   └── metas_kpis.csv             # Metas dos KPIs
│
└── scripts/
    ├── create_tables_sqlserver.sql # Script SQL Server
    └── create_tables_oracle.sql    # Script Oracle
```

---

## 📊 Eixos e KPIs

### 📈 Resumo Executivo (6 KPIs)
NPS • Ocupação % • Absenteísmo % • TMA (seg) • Conversão % • SLA %

### ✅ Qualidade (8 KPIs)
% Rechamadas 24hs • % Rechamadas 7 dias • % Transferência • Nota TDNA • % Falha Operacional • % Aderência Processual • Nota Monitoria Whisper • % CallBack

### ⚙️ Produção (10 KPIs)
Chamadas Atendidas • %Abandono • % RGC • TMA • % Pausa • Tempo Logado • % Abs • TO • Produtividade/HC • Margem Operacional

### 💼 Negócios (7 KPIs)
Qnt. Negócios • % Conversão • % Churn FTTH/Pós • % Cancelamento FTTH • R$ Rentabilizações • %Taxa Retenção • % arrecadação

### 💰 Financeiro (7 KPIs)
Custo PRV • Compensation • Gastos Férias • Custo HE • Custo unitário • Custo/margem HC • Valor Taxi

---

## 🔧 Configuração Rápida

### SQL Server

```python
# Editar database_connector.py
SQL_SERVER_CONFIG = {
    'server': 'seu_servidor.database.windows.net',
    'database': 'DashboardInsourcing',
    'username': 'seu_usuario',
    'password': 'sua_senha',
    'driver': '{ODBC Driver 17 for SQL Server}'
}
DATABASE_TYPE = 'sqlserver'
```

### Oracle

```python
# Editar database_connector.py
ORACLE_CONFIG = {
    'host': 'localhost',
    'port': 1521,
    'service_name': 'ORCL',
    'username': 'seu_usuario',
    'password': 'sua_senha'
}
DATABASE_TYPE = 'oracle'
```

### Testar Conexão

```bash
python database_connector.py
```

---

## 📚 Documentação

- **[INSTALACAO_E_CONFIGURACAO.md](INSTALACAO_E_CONFIGURACAO.md)** - Guia completo
- **[RESUMO_IMPLEMENTACAO_COMPLETA.md](RESUMO_IMPLEMENTACAO_COMPLETA.md)** - Documentação técnica
- **[scripts/create_tables_sqlserver.sql](scripts/create_tables_sqlserver.sql)** - SQL Server
- **[scripts/create_tables_oracle.sql](scripts/create_tables_oracle.sql)** - Oracle

---

## 🛠️ Tecnologias

- Python 3.8+ • Dash 2.14+ • Plotly 5.18+ • Pandas 2.1+ • Dash Bootstrap Components

---

## 📋 Requisitos

- Python 3.8+
- 4GB RAM
- Navegador moderno
- SQL Server 2012+ OU Oracle 11g+ (opcional)

---

## 🎯 Funcionalidades

### Filtros
Período • Operação • Grupos • Gerente • Granularidade

### Visualizações
Cards de KPI • Gráficos de Evolução • Tabelas Evolutivas (Operação/Grupo/Gerente)

### Performance
< 1s carregamento • Filtros responsivos • Queries otimizadas

---

## 📈 Roadmap

**Fase 2:** Alertas (Power Automate, Teams, WhatsApp)  
**Fase 3:** Análise Avançada (ML, Previsões, Drill-down, Export)  
**Fase 4:** Mobile (App nativo, Notificações push)

---

## 🤝 Suporte

1. Consultar **INSTALACAO_E_CONFIGURACAO.md**
2. Verificar logs em `dashboard.log`
3. Testar conexão: `python database_connector.py`

---

## 📝 Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas
- [ ] Driver de banco instalado
- [ ] `database_connector.py` configurado
- [ ] Conexão testada
- [ ] Tabelas criadas
- [ ] Dados carregados
- [ ] Dashboard executado
- [ ] Dashboard acessível

---

**Dashboard KPIs Insourcing - Vivo Fibra**  
**Versão 1.0.0 • Dezembro 2024**
