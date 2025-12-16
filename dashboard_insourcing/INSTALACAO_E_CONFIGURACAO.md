# 📘 Guia de Instalação e Configuração
## Dashboard KPIs Insourcing - Vivo Fibra

---

## 📋 Índice

1. [Requisitos do Sistema](#requisitos-do-sistema)
2. [Instalação](#instalação)
3. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
4. [Estrutura de Dados Necessária](#estrutura-de-dados-necessária)
5. [Execução do Dashboard](#execução-do-dashboard)
6. [Solução de Problemas](#solução-de-problemas)
7. [Manutenção e Atualização](#manutenção-e-atualização)

---

## 🖥️ Requisitos do Sistema

### Software Necessário

- **Python 3.8 ou superior**
- **pip** (gerenciador de pacotes Python)
- **Navegador web** (Chrome, Firefox, Edge ou Safari)

### Banco de Dados (escolha um)

- **SQL Server** (2012 ou superior) OU
- **Oracle Database** (11g ou superior) OU
- **Arquivos CSV** (para desenvolvimento/teste)

### Drivers de Banco de Dados

#### Para SQL Server:
- **Windows**: ODBC Driver 17 for SQL Server (geralmente já instalado)
- **Linux/Mac**: 
  ```bash
  # Ubuntu/Debian
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
  curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
  apt-get update
  ACCEPT_EULA=Y apt-get install -y msodbcsql17
  
  # macOS
  brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
  brew update
  HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql17
  ```

#### Para Oracle:
- **Oracle Instant Client** (versão compatível com seu banco)
- Download: https://www.oracle.com/database/technologies/instant-client/downloads.html

---

## 🚀 Instalação

### Passo 1: Extrair o Projeto

```bash
# Extrair o arquivo ZIP para um diretório de sua escolha
unzip dashboard_insourcing.zip
cd dashboard_insourcing
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
# Instalar todas as dependências necessárias
pip install -r requirements.txt
```

#### Dependências Adicionais por Banco de Dados

**Para SQL Server:**
```bash
pip install pyodbc
```

**Para Oracle:**
```bash
pip install cx_Oracle
```

---

## 🔧 Configuração do Banco de Dados

### Opção 1: SQL Server

1. **Abrir o arquivo `database_connector.py`**

2. **Editar a seção SQL_SERVER_CONFIG:**

```python
SQL_SERVER_CONFIG = {
    'server': 'seu_servidor.database.windows.net',  # Ex: myserver.database.windows.net
    'database': 'DashboardInsourcing',              # Nome do seu banco
    'username': 'seu_usuario',                      # Seu usuário SQL
    'password': 'sua_senha',                        # Sua senha
    'driver': '{ODBC Driver 17 for SQL Server}'     # Driver instalado
}
```

3. **Alterar o tipo de banco:**

```python
DATABASE_TYPE = 'sqlserver'  # Alterar de 'csv' para 'sqlserver'
```

4. **Testar a conexão:**

```bash
python database_connector.py
```

### Opção 2: Oracle

1. **Abrir o arquivo `database_connector.py`**

2. **Editar a seção ORACLE_CONFIG:**

```python
ORACLE_CONFIG = {
    'host': 'localhost',              # IP ou hostname do servidor Oracle
    'port': 1521,                     # Porta padrão do Oracle
    'service_name': 'ORCL',           # Service Name do banco
    # OU use 'sid': 'ORCL' ao invés de service_name
    'username': 'seu_usuario',        # Seu usuário Oracle
    'password': 'sua_senha'           # Sua senha
}
```

3. **Configurar Oracle Instant Client (se necessário):**

```python
# Adicionar no início do arquivo database_connector.py, após os imports:
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir="/caminho/para/instantclient")
```

4. **Alterar o tipo de banco:**

```python
DATABASE_TYPE = 'oracle'  # Alterar de 'csv' para 'oracle'
```

5. **Testar a conexão:**

```bash
python database_connector.py
```

### Opção 3: Modo CSV (Desenvolvimento)

O dashboard já vem configurado para usar CSV por padrão. Os arquivos estão em:
- `data/fato_metricas_diarias.csv`
- `data/metas_kpis.csv`

Não é necessária nenhuma configuração adicional.

---

## 📊 Estrutura de Dados Necessária

### Tabela Principal: `fato_metricas_diarias`

```sql
CREATE TABLE fato_metricas_diarias (
    -- Dimensões
    Data DATE NOT NULL,
    Operacao VARCHAR(10) NOT NULL,  -- 'B2C' ou 'B2B'
    Cidade VARCHAR(50) NOT NULL,
    Gerente VARCHAR(100) NOT NULL,
    
    -- KPIs Resumo Executivo
    NPS DECIMAL(5,2),
    Ocupacao_Pct DECIMAL(5,2),
    Absenteismo_Pct DECIMAL(5,2),
    TMA_Seg DECIMAL(8,2),
    Conversao_Pct DECIMAL(5,2),
    SLA_Atendimento_Pct DECIMAL(5,2),
    
    -- KPIs Qualidade
    Rechamadas_24h_Pct DECIMAL(5,2),
    Rechamadas_7d_Pct DECIMAL(5,2),
    Transferencia_Pct DECIMAL(5,2),
    Nota_TDNA DECIMAL(4,2),
    Falha_Operacional_Pct DECIMAL(5,2),
    Aderencia_Processual_Pct DECIMAL(5,2),
    Nota_Monitoria_Whisper DECIMAL(4,2),
    CallBack_Tentado_Efetivado_Pct DECIMAL(5,2),
    
    -- KPIs Produção
    Chamadas_Atendidas DECIMAL(10,2),
    Abandono_Pct DECIMAL(5,2),
    RGC_Pct DECIMAL(5,2),
    TMA_Producao DECIMAL(8,2),
    Pausa_Pct DECIMAL(5,2),
    Tempo_Logado_Hrs DECIMAL(6,2),
    Abs_Pct DECIMAL(5,2),
    TO_Pct DECIMAL(5,2),
    Produtividade_HC DECIMAL(10,2),
    Margem_Operacional_DRE_Pct DECIMAL(5,2),
    
    -- KPIs Negócios
    Qnt_Negocios_Totais DECIMAL(10,2),
    Conversao_Negocios_Pct DECIMAL(5,2),
    Churn_FTTH_Pos_Pct DECIMAL(5,2),
    Cancelamento_FTTH_Pct DECIMAL(5,2),
    Rentabilizacoes_Totais_R DECIMAL(15,2),
    Taxa_Retencao_Pct DECIMAL(5,2),
    Arrecadacao_Pct DECIMAL(5,2),
    
    -- KPIs Financeiro
    Custo_PRV_Mensal DECIMAL(15,2),
    Compensation_Total DECIMAL(15,2),
    Gastos_Ferias DECIMAL(15,2),
    Custo_HE DECIMAL(15,2),
    Custo_Unitario_Operacao DECIMAL(10,2),
    Custo_Margem_HC DECIMAL(15,2),
    Valor_Taxi DECIMAL(10,2),
    
    PRIMARY KEY (Data, Operacao, Cidade, Gerente)
);
```

### Tabela de Metas: `metas_kpis`

```sql
CREATE TABLE metas_kpis (
    kpi_id VARCHAR(50) PRIMARY KEY,
    kpi_nome VARCHAR(100) NOT NULL,
    meta_valor DECIMAL(10,2),
    inverter BIT DEFAULT 0  -- 1 se menor é melhor, 0 se maior é melhor
);
```

### Inserir Metas (Exemplo)

```sql
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('nps', 'NPS', 70, 0),
('ocupacao', 'Ocupação %', 85, 0),
('absenteismo', 'Absenteísmo %', 5, 1),
('tma', 'TMA (seg)', 300, 1),
('conversao', 'Conversão %', 15, 0),
('sla', 'SLA %', 90, 0);
-- ... adicionar todas as outras metas
```

### Script de Criação Completo

Um script SQL completo está disponível em:
- `scripts/create_tables_sqlserver.sql` (para SQL Server)
- `scripts/create_tables_oracle.sql` (para Oracle)

---

## ▶️ Execução do Dashboard

### Método 1: Execução Direta

```bash
# Ativar ambiente virtual (se criado)
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Executar dashboard
python dashboard_app_final.py
```

O dashboard estará disponível em: **http://localhost:8050**

### Método 2: Execução em Background (Linux/Mac)

```bash
nohup python dashboard_app_final.py > dashboard.log 2>&1 &
```

### Método 3: Usando Gunicorn (Produção)

```bash
# Instalar Gunicorn
pip install gunicorn

# Executar com Gunicorn
gunicorn dashboard_app_final:server -b 0.0.0.0:8050 --workers 4
```

### Parar o Dashboard

```bash
# Se executando em foreground: Ctrl+C

# Se executando em background:
pkill -f dashboard_app_final
```

---

## 🐛 Solução de Problemas

### Erro: "Module not found"

**Solução:** Instalar a dependência faltante
```bash
pip install nome_do_modulo
```

### Erro: "Unable to connect to database"

**Verificar:**
1. Credenciais corretas em `database_connector.py`
2. Servidor de banco acessível (firewall, VPN)
3. Driver ODBC/Oracle Client instalado
4. Testar conexão: `python database_connector.py`

### Erro: "Port 8050 already in use"

**Solução:** Alterar porta no arquivo `dashboard_app_final.py`
```python
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8051)  # Alterar porta
```

### Dashboard lento

**Otimizações:**
1. Criar índices nas colunas Data, Operacao, Cidade, Gerente
2. Limitar período de dados carregados
3. Aumentar memória do servidor
4. Usar cache de dados

### Erro de codificação (caracteres especiais)

**Solução:** Adicionar encoding UTF-8
```python
# No database_connector.py, ao ler CSV:
df = pd.read_csv(csv_path, encoding='utf-8')
```

---

## 🔄 Manutenção e Atualização

### Atualizar Dados

O dashboard carrega dados automaticamente ao iniciar. Para atualizar:
1. Parar o dashboard
2. Atualizar dados no banco
3. Reiniciar o dashboard

### Backup

**Arquivos importantes para backup:**
- `dashboard_app_final.py` (código principal)
- `database_connector.py` (configurações de conexão)
- `data/` (dados CSV, se usado)
- `assets/` (logo e recursos visuais)

### Adicionar Novos KPIs

1. Adicionar coluna na tabela `fato_metricas_diarias`
2. Atualizar query em `database_connector.py`
3. Adicionar KPI em `dashboard_app_final.py` no dicionário correspondente
4. Adicionar meta em `metas_kpis`

### Logs

Logs são salvos em:
- `dashboard.log` (execução do dashboard)
- Console (se executando em foreground)

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar esta documentação
2. Verificar `RESUMO_IMPLEMENTACAO_COMPLETA.md`
3. Testar conexão com `python database_connector.py`
4. Verificar logs em `dashboard.log`

---

## 📝 Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Driver de banco instalado (ODBC/Oracle Client)
- [ ] Arquivo `database_connector.py` configurado
- [ ] Conexão testada (`python database_connector.py`)
- [ ] Tabelas criadas no banco de dados
- [ ] Dados carregados nas tabelas
- [ ] Dashboard executado com sucesso
- [ ] Dashboard acessível no navegador

---

**Dashboard KPIs Insourcing - Vivo Fibra**  
**Versão 1.0.0**  
**Data: Dezembro 2024**
