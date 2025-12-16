"""
Módulo de Conexão com Bancos de Dados
Dashboard KPIs Insourcing - Vivo

Suporta: SQL Server e Oracle
"""

import pandas as pd
import os
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURAÇÃO - EDITE AQUI COM SUAS CREDENCIAIS
# ============================================================================

# SQL SERVER
SQL_SERVER_CONFIG = {
    'server': 'seu_servidor.database.windows.net',  # Ex: myserver.database.windows.net
    'database': 'nome_do_banco',
    'username': 'seu_usuario',
    'password': 'sua_senha',
    'driver': '{ODBC Driver 17 for SQL Server}'  # ou '{SQL Server}'
}

# ORACLE
ORACLE_CONFIG = {
    'host': 'seu_host_oracle',  # Ex: localhost ou IP
    'port': 1521,
    'service_name': 'seu_service_name',  # ou use 'sid' ao invés de 'service_name'
    'username': 'seu_usuario',
    'password': 'sua_senha'
}

# Escolha qual banco usar: 'sqlserver', 'oracle' ou 'csv'
DATABASE_TYPE = 'csv'  # Altere para 'sqlserver' ou 'oracle' quando configurar

# ============================================================================
# FUNÇÕES DE CONEXÃO
# ============================================================================

def conectar_sqlserver():
    """Conecta ao SQL Server e retorna a conexão"""
    try:
        import pyodbc
        
        conn_str = (
            f"DRIVER={SQL_SERVER_CONFIG['driver']};"
            f"SERVER={SQL_SERVER_CONFIG['server']};"
            f"DATABASE={SQL_SERVER_CONFIG['database']};"
            f"UID={SQL_SERVER_CONFIG['username']};"
            f"PWD={SQL_SERVER_CONFIG['password']}"
        )
        
        conn = pyodbc.connect(conn_str)
        print("✅ Conectado ao SQL Server com sucesso!")
        return conn
        
    except ImportError:
        print("❌ Erro: pyodbc não instalado. Execute: pip install pyodbc")
        return None
    except Exception as e:
        print(f"❌ Erro ao conectar ao SQL Server: {e}")
        return None


def conectar_oracle():
    """Conecta ao Oracle e retorna a conexão"""
    try:
        import cx_Oracle
        
        # Criar DSN (Data Source Name)
        dsn = cx_Oracle.makedsn(
            ORACLE_CONFIG['host'],
            ORACLE_CONFIG['port'],
            service_name=ORACLE_CONFIG['service_name']
            # ou use: sid=ORACLE_CONFIG['sid']
        )
        
        conn = cx_Oracle.connect(
            user=ORACLE_CONFIG['username'],
            password=ORACLE_CONFIG['password'],
            dsn=dsn
        )
        
        print("✅ Conectado ao Oracle com sucesso!")
        return conn
        
    except ImportError:
        print("❌ Erro: cx_Oracle não instalado. Execute: pip install cx_Oracle")
        return None
    except Exception as e:
        print(f"❌ Erro ao conectar ao Oracle: {e}")
        return None


# ============================================================================
# QUERIES SQL - ADAPTE CONFORME SUA ESTRUTURA DE DADOS
# ============================================================================

# Query principal para buscar dados do fato de métricas
QUERY_FATO_METRICAS = """
SELECT 
    Data,
    Operacao,
    Cidade,
    Gerente,
    
    -- KPIs Resumo
    NPS,
    Ocupacao_Pct,
    Absenteismo_Pct,
    TMA_Seg,
    Conversao_Pct,
    SLA_Atendimento_Pct,
    
    -- KPIs Qualidade
    Rechamadas_24h_Pct,
    Rechamadas_7d_Pct,
    Transferencia_Pct,
    Nota_TDNA,
    Falha_Operacional_Pct,
    Aderencia_Processual_Pct,
    Nota_Monitoria_Whisper,
    CallBack_Tentado_Efetivado_Pct,
    
    -- KPIs Produção
    Chamadas_Atendidas,
    Abandono_Pct,
    RGC_Pct,
    TMA_Producao,
    Pausa_Pct,
    Tempo_Logado_Hrs,
    Abs_Pct,
    TO_Pct,
    Produtividade_HC,
    Margem_Operacional_DRE_Pct,
    
    -- KPIs Negócios
    Qnt_Negocios_Totais,
    Conversao_Negocios_Pct,
    Churn_FTTH_Pos_Pct,
    Cancelamento_FTTH_Pct,
    Rentabilizacoes_Totais_R,
    Taxa_Retencao_Pct,
    Arrecadacao_Pct,
    
    -- KPIs Financeiro
    Custo_PRV_Mensal,
    Compensation_Total,
    Gastos_Ferias,
    Custo_HE,
    Custo_Unitario_Operacao,
    Custo_Margem_HC,
    Valor_Taxi

FROM fato_metricas_diarias
WHERE Data >= ? AND Data <= ?
ORDER BY Data, Operacao, Cidade, Gerente
"""

# Query para metas
QUERY_METAS = """
SELECT 
    kpi_id,
    kpi_nome,
    meta_valor,
    inverter
FROM metas_kpis
"""


# ============================================================================
# FUNÇÃO PRINCIPAL PARA CARREGAR DADOS
# ============================================================================

def carregar_dados_banco(data_inicio=None, data_fim=None):
    """
    Carrega dados do banco de dados configurado
    
    Args:
        data_inicio: Data inicial (formato: 'YYYY-MM-DD')
        data_fim: Data final (formato: 'YYYY-MM-DD')
    
    Returns:
        DataFrame com os dados ou None em caso de erro
    """
    
    # Valores padrão se não fornecidos
    if data_inicio is None:
        data_inicio = '2024-01-01'
    if data_fim is None:
        data_fim = datetime.now().strftime('%Y-%m-%d')
    
    print(f"\n🔄 Carregando dados de {data_inicio} até {data_fim}...")
    
    try:
        if DATABASE_TYPE == 'sqlserver':
            conn = conectar_sqlserver()
            if conn is None:
                return None
            
            df = pd.read_sql(QUERY_FATO_METRICAS, conn, params=[data_inicio, data_fim])
            conn.close()
            
        elif DATABASE_TYPE == 'oracle':
            conn = conectar_oracle()
            if conn is None:
                return None
            
            # Oracle usa :1, :2 para parâmetros
            query_oracle = QUERY_FATO_METRICAS.replace('?', ':1').replace('?', ':2', 1)
            df = pd.read_sql(query_oracle, conn, params=[data_inicio, data_fim])
            conn.close()
            
        elif DATABASE_TYPE == 'csv':
            # Modo CSV (desenvolvimento)
            csv_path = Path(__file__).parent / 'data' / 'fato_metricas_diarias.csv'
            print(f"📁 Carregando dados do CSV: {csv_path}")
            df = pd.read_csv(csv_path)
            df['Data'] = pd.to_datetime(df['Data'])
            
            # Filtrar por data
            df = df[(df['Data'] >= data_inicio) & (df['Data'] <= data_fim)]
            
        else:
            print(f"❌ Tipo de banco inválido: {DATABASE_TYPE}")
            return None
        
        # Converter coluna Data para datetime
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'])
        
        print(f"✅ Dados carregados: {len(df)} registros")
        return df
        
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return None


def carregar_metas():
    """Carrega metas dos KPIs do banco de dados"""
    
    try:
        if DATABASE_TYPE == 'sqlserver':
            conn = conectar_sqlserver()
            if conn is None:
                return None
            df = pd.read_sql(QUERY_METAS, conn)
            conn.close()
            
        elif DATABASE_TYPE == 'oracle':
            conn = conectar_oracle()
            if conn is None:
                return None
            df = pd.read_sql(QUERY_METAS, conn)
            conn.close()
            
        elif DATABASE_TYPE == 'csv':
            csv_path = Path(__file__).parent / 'data' / 'metas_kpis.csv'
            df = pd.read_csv(csv_path)
        
        return df
        
    except Exception as e:
        print(f"❌ Erro ao carregar metas: {e}")
        return None


# ============================================================================
# TESTE DE CONEXÃO
# ============================================================================

def testar_conexao():
    """Testa a conexão com o banco de dados configurado"""
    
    print("\n" + "="*60)
    print("TESTE DE CONEXÃO COM BANCO DE DADOS")
    print("="*60)
    print(f"\nTipo de banco configurado: {DATABASE_TYPE.upper()}")
    
    if DATABASE_TYPE == 'sqlserver':
        print("\n📊 Testando conexão com SQL Server...")
        print(f"Servidor: {SQL_SERVER_CONFIG['server']}")
        print(f"Banco: {SQL_SERVER_CONFIG['database']}")
        conn = conectar_sqlserver()
        if conn:
            conn.close()
            print("✅ Conexão testada com sucesso!")
            return True
        else:
            print("❌ Falha na conexão")
            return False
            
    elif DATABASE_TYPE == 'oracle':
        print("\n🔶 Testando conexão com Oracle...")
        print(f"Host: {ORACLE_CONFIG['host']}")
        print(f"Service: {ORACLE_CONFIG['service_name']}")
        conn = conectar_oracle()
        if conn:
            conn.close()
            print("✅ Conexão testada com sucesso!")
            return True
        else:
            print("❌ Falha na conexão")
            return False
            
    elif DATABASE_TYPE == 'csv':
        print("\n📁 Modo CSV (desenvolvimento)")
        csv_path = Path(__file__).parent / 'data' / 'fato_metricas_diarias.csv'
        if csv_path.exists():
            print(f"✅ Arquivo CSV encontrado: {csv_path}")
            return True
        else:
            print(f"❌ Arquivo CSV não encontrado: {csv_path}")
            return False


# ============================================================================
# EXECUÇÃO DIRETA PARA TESTE
# ============================================================================

if __name__ == "__main__":
    # Testar conexão
    testar_conexao()
    
    # Tentar carregar dados
    print("\n" + "="*60)
    print("TESTE DE CARREGAMENTO DE DADOS")
    print("="*60)
    
    df = carregar_dados_banco('2024-01-01', '2024-12-31')
    
    if df is not None:
        print(f"\n✅ Dados carregados com sucesso!")
        print(f"📊 Total de registros: {len(df)}")
        print(f"📅 Período: {df['Data'].min()} até {df['Data'].max()}")
        print(f"\n🔍 Primeiras linhas:")
        print(df.head())
        print(f"\n📋 Colunas disponíveis:")
        print(df.columns.tolist())
    else:
        print("\n❌ Falha ao carregar dados")
