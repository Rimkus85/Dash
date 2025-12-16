# 🚀 Guia de Início Rápido
## Dashboard KPIs Insourcing - Vivo Fibra

---

## ⏱️ Em 5 Minutos

### 1. Extrair o Projeto

```bash
unzip dashboard_insourcing_completo.zip
cd dashboard_insourcing
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar Dashboard

```bash
python dashboard_app_final.py
```

### 4. Acessar no Navegador

Abra: **http://localhost:8050**

✅ **Pronto!** O dashboard está rodando com dados de exemplo.

---

## 🗄️ Conectar ao Seu Banco de Dados

### SQL Server

1. **Abrir** `database_connector.py`

2. **Editar configurações:**

```python
SQL_SERVER_CONFIG = {
    'server': 'seu_servidor.database.windows.net',
    'database': 'DashboardInsourcing',
    'username': 'seu_usuario',
    'password': 'sua_senha',
    'driver': '{ODBC Driver 17 for SQL Server}'
}

DATABASE_TYPE = 'sqlserver'  # Mudar de 'csv' para 'sqlserver'
```

3. **Criar tabelas:**

```bash
# Executar script SQL no seu banco
# Arquivo: scripts/create_tables_sqlserver.sql
```

4. **Testar conexão:**

```bash
python database_connector.py
```

5. **Reiniciar dashboard:**

```bash
python dashboard_app_final.py
```

### Oracle

1. **Abrir** `database_connector.py`

2. **Editar configurações:**

```python
ORACLE_CONFIG = {
    'host': 'localhost',
    'port': 1521,
    'service_name': 'ORCL',
    'username': 'seu_usuario',
    'password': 'sua_senha'
}

DATABASE_TYPE = 'oracle'  # Mudar de 'csv' para 'oracle'
```

3. **Criar tabelas:**

```bash
# Executar script SQL no seu banco
# Arquivo: scripts/create_tables_oracle.sql
```

4. **Testar conexão:**

```bash
python database_connector.py
```

5. **Reiniciar dashboard:**

```bash
python dashboard_app_final.py
```

---

## 📊 Estrutura de Dados

### Tabela Principal: `fato_metricas_diarias`

**Colunas obrigatórias:**
- `Data` (DATE)
- `Operacao` (VARCHAR) - 'B2C' ou 'B2B'
- `Cidade` (VARCHAR)
- `Gerente` (VARCHAR)

**Colunas de KPIs:** (38 colunas - ver scripts SQL)

### Tabela de Metas: `metas_kpis`

**Colunas:**
- `kpi_id` (VARCHAR) - Identificador único
- `kpi_nome` (VARCHAR) - Nome do KPI
- `meta_valor` (DECIMAL) - Valor da meta
- `inverter` (BIT) - 1 se menor é melhor

---

## 🔧 Solução Rápida de Problemas

### Erro: "Module not found"

```bash
pip install nome_do_modulo
```

### Erro: "Unable to connect to database"

1. Verificar credenciais em `database_connector.py`
2. Testar: `python database_connector.py`
3. Verificar firewall/VPN

### Erro: "Port 8050 already in use"

```bash
# Parar processo anterior
pkill -f dashboard_app_final

# OU alterar porta em dashboard_app_final.py (linha final)
app.run_server(debug=False, host='0.0.0.0', port=8051)
```

---

## 📚 Documentação Completa

Para mais detalhes, consulte:

- **[INSTALACAO_E_CONFIGURACAO.md](INSTALACAO_E_CONFIGURACAO.md)** - Guia completo
- **[RESUMO_IMPLEMENTACAO_COMPLETA.md](RESUMO_IMPLEMENTACAO_COMPLETA.md)** - Documentação técnica
- **[README.md](README.md)** - Visão geral do projeto

---

## ✅ Checklist Rápido

- [ ] Projeto extraído
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Dashboard executado (`python dashboard_app_final.py`)
- [ ] Dashboard acessível em http://localhost:8050
- [ ] (Opcional) Banco de dados configurado
- [ ] (Opcional) Tabelas criadas
- [ ] (Opcional) Dados carregados

---

## 🎯 Próximos Passos

1. ✅ **Explorar o dashboard** com dados de exemplo
2. 📊 **Criar tabelas** no seu banco de dados
3. 🔗 **Configurar conexão** em `database_connector.py`
4. 📥 **Carregar seus dados** nas tabelas
5. 🚀 **Executar em produção**

---

**Dúvidas?** Consulte **INSTALACAO_E_CONFIGURACAO.md**

**Dashboard KPIs Insourcing - Vivo Fibra**  
**Versão 1.0.0 • Dezembro 2024**
