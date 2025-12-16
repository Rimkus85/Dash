"""
Mapeamento Completo dos 32 KPIs por Eixo
Baseado na lista fornecida pelo usuário
"""

from dashboard_app_final import VIVO_COLORS

# ============================================================================
# EIXO: QUALIDADE (8 KPIs)
# ============================================================================

KPIS_QUALIDADE = {
    'rechamadas_24h': {
        'coluna': 'Rechamadas_24h_Pct',
        'nome': '% Rechamadas 24hs',
        'cor': VIVO_COLORS['red'],
        'meta': 5,
        'inverter': True,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'rechamadas_7d': {
        'coluna': 'Rechamadas_7d_Pct',
        'nome': '% Rechamadas 7 dias',
        'cor': VIVO_COLORS['danger'],
        'meta': 10,
        'inverter': True,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'transferencia': {
        'coluna': 'Transferencia_Pct',
        'nome': '% Transferência',
        'cor': VIVO_COLORS['warning'],
        'meta': 15,
        'inverter': True,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'nota_tdna': {
        'coluna': 'Nota_TDNA',
        'nome': 'Nota TDNA',
        'cor': VIVO_COLORS['neon_cyan'],
        'meta': 8.5,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'falha_operacional': {
        'coluna': 'Falha_Operacional_Pct',
        'nome': '% Falha Operacional',
        'cor': VIVO_COLORS['red'],
        'meta': 3,
        'inverter': True,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'aderencia_processual': {
        'coluna': 'Aderencia_Processual_Pct',
        'nome': '% Aderência Processual',
        'cor': VIVO_COLORS['neon_green'],
        'meta': 95,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'monitoria_whisper': {
        'coluna': 'Nota_Monitoria_Whisper',
        'nome': 'Nota Monitoria Whisper',
        'cor': VIVO_COLORS['neon_pink'],
        'meta': 8.0,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'callback_tentado': {
        'coluna': 'CallBack_Tentado_Efetivado_Pct',
        'nome': '% CallBack tentado e efetivado',
        'cor': VIVO_COLORS['secondary'],
        'meta': 80,
        'visoes': ['ilha', 'operador', 'cidades']
    }
}

# ============================================================================
# EIXO: PRODUÇÃO (8 KPIs)
# ============================================================================

KPIS_PRODUCAO = {
    'chamadas_atendidas': {
        'coluna': 'Chamadas_Atendidas',
        'nome': 'Chamadas Atendidas / demandas',
        'cor': VIVO_COLORS['neon_cyan'],
        'meta': None,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes']
    },
    'abandono': {
        'coluna': 'Abandono_Pct',
        'nome': '%Abandono',
        'cor': VIVO_COLORS['red'],
        'meta': 5,
        'inverter': True,
        'visoes': ['ilha']
    },
    'rgc': {
        'coluna': 'RGC_Pct',
        'nome': '% RGC',
        'cor': VIVO_COLORS['warning'],
        'meta': 10,
        'inverter': True,
        'visoes': ['ilha']
    },
    'tma': {
        'coluna': 'TMA_Seg',
        'nome': 'TMA',
        'cor': VIVO_COLORS['gold'],
        'meta': 300,
        'inverter': True,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'pausa': {
        'coluna': 'Pausa_Pct',
        'nome': '% Pausa',
        'cor': VIVO_COLORS['warning'],
        'meta': 10,
        'inverter': True,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'tempo_logado': {
        'coluna': 'Tempo_Logado_Horas',
        'nome': 'Tempo Logado',
        'cor': VIVO_COLORS['neon_green'],
        'meta': 7.5,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'absenteismo': {
        'coluna': 'Absenteismo_Pct',
        'nome': '% Abs',
        'cor': VIVO_COLORS['red'],
        'meta': 5,
        'inverter': True,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes']
    },
    'to': {
        'coluna': 'TO_Pct',
        'nome': 'TO',
        'cor': VIVO_COLORS['danger'],
        'meta': 3,
        'inverter': True,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes']
    },
    'produtividade_hc': {
        'coluna': 'Produtividade_HC',
        'nome': 'Produtividade / HC',
        'cor': VIVO_COLORS['neon_pink'],
        'meta': 100,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'margem_operacional': {
        'coluna': 'Margem_Operacional_DRE_Pct',
        'nome': 'Margem Operacional (DRE)',
        'cor': VIVO_COLORS['neon_green'],
        'meta': 15,
        'visoes': ['ilha']
    }
}

# ============================================================================
# EIXO: NEGÓCIOS (7 KPIs)
# ============================================================================

KPIS_NEGOCIOS = {
    'qnt_negocios': {
        'coluna': 'Qnt_Negocios_Totais',
        'nome': 'Qnt. Negócios totais gerados',
        'cor': VIVO_COLORS['neon_cyan'],
        'meta': None,
        'visoes': ['ilha', 'operador', 'quartis']
    },
    'conversao': {
        'coluna': 'Conversao_Pct',
        'nome': '% Conversao (e tipo de negócio)',
        'cor': VIVO_COLORS['neon_green'],
        'meta': 15,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'churn_ftth': {
        'coluna': 'Churn_FTTH_Pos_Pct',
        'nome': '% Churn FTTH / Pós',
        'cor': VIVO_COLORS['red'],
        'meta': 2,
        'inverter': True,
        'visoes': ['ilha', 'operador', 'cidades', 'quartis']
    },
    'cancelamento_ftth': {
        'coluna': 'Cancelamento_FTTH_Pct',
        'nome': '% Cancelamento de FTTH',
        'cor': VIVO_COLORS['danger'],
        'meta': 5,
        'inverter': True,
        'visoes': ['ilha', 'operador', 'cidades', 'quartis']
    },
    'rentabilizacoes': {
        'coluna': 'Rentabilizacoes_Totais_RS',
        'nome': 'R$ Rentabilizações totais',
        'cor': VIVO_COLORS['neon_pink'],
        'meta': None,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes', 'quartis']
    },
    'taxa_retencao': {
        'coluna': 'Taxa_Retencao_Pct',
        'nome': '%Taxa de Retenção',
        'cor': VIVO_COLORS['neon_green'],
        'meta': 85,
        'visoes': ['ilha', 'operador', 'quartis']
    },
    'arrecadacao': {
        'coluna': 'Arrecadacao_Pct',
        'nome': '% arrecadação',
        'cor': VIVO_COLORS['gold'],
        'meta': 90,
        'visoes': ['ilha', 'operador', 'quartis']
    }
}

# ============================================================================
# EIXO: FINANCEIRO (9 KPIs)
# ============================================================================

KPIS_FINANCEIRO = {
    'custo_prv_mensal': {
        'coluna': 'Custo_PRV_Mensal_RS',
        'nome': 'Custo PRV mensal e evolução',
        'cor': VIVO_COLORS['neon_cyan'],
        'meta': None,
        'visoes': ['ilha', 'operador', 'gerente']
    },
    'compensation_total': {
        'coluna': 'Compensation_Total_RS',
        'nome': 'Compensation Total',
        'cor': VIVO_COLORS['neon_pink'],
        'meta': None,
        'visoes': ['ilha']
    },
    'gastos_ferias': {
        'coluna': 'Gastos_Ferias_RS',
        'nome': 'Gastos Férias',
        'cor': VIVO_COLORS['warning'],
        'meta': None,
        'visoes': ['gerente']
    },
    'custo_he': {
        'coluna': 'Custo_HE_RS',
        'nome': 'Custo HE',
        'cor': VIVO_COLORS['gold'],
        'meta': None,
        'visoes': ['gerente', 'quartis']
    },
    'custo_unitario_operacao': {
        'coluna': 'Custo_Unitario_Operacao_RS',
        'nome': 'Custo unitário por Operação',
        'cor': VIVO_COLORS['neon_green'],
        'meta': 25,
        'inverter': True,
        'visoes': ['ilha', 'gerente']
    },
    'custo_margem_hc': {
        'coluna': 'Custo_Margem_HC_RS',
        'nome': 'Custo / margem por HC',
        'cor': VIVO_COLORS['secondary'],
        'meta': None,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes']
    },
    'valor_taxi': {
        'coluna': 'Valor_Taxi_RS',
        'nome': 'Valor Taxi',
        'cor': VIVO_COLORS['red'],
        'meta': None,
        'visoes': ['ilha', 'operador', 'cidades', 'gerentes']
    }
}

# ============================================================================
# RESUMO EXECUTIVO (6 KPIs principais)
# ============================================================================

KPIS_RESUMO = {
    'nps': {
        'coluna': 'NPS',
        'nome': 'NPS',
        'cor': VIVO_COLORS['neon_pink'],
        'meta': 70
    },
    'ocupacao': {
        'coluna': 'Ocupacao_Pct',
        'nome': 'Ocupação %',
        'cor': VIVO_COLORS['neon_cyan'],
        'meta': 85
    },
    'absenteismo': {
        'coluna': 'Absenteismo_Pct',
        'nome': 'Absenteísmo %',
        'cor': VIVO_COLORS['red'],
        'meta': 5,
        'inverter': True
    },
    'tma': {
        'coluna': 'TMA_Seg',
        'nome': 'TMA (seg)',
        'cor': VIVO_COLORS['gold'],
        'meta': 300,
        'inverter': True
    },
    'conversao': {
        'coluna': 'Conversao_Pct',
        'nome': 'Conversão %',
        'cor': VIVO_COLORS['neon_green'],
        'meta': 15
    },
    'sla': {
        'coluna': 'SLA_Atendimento_Pct',
        'nome': 'SLA %',
        'cor': VIVO_COLORS['secondary'],
        'meta': 90
    }
}

# ============================================================================
# MAPEAMENTO COMPLETO
# ============================================================================

TODOS_OS_EIXOS = {
    'resumo': {'nome': '📈 Resumo Executivo', 'kpis': KPIS_RESUMO},
    'qualidade': {'nome': '✅ Qualidade', 'kpis': KPIS_QUALIDADE},
    'producao': {'nome': '⚙️ Produção', 'kpis': KPIS_PRODUCAO},
    'negocios': {'nome': '💼 Negócios', 'kpis': KPIS_NEGOCIOS},
    'financeiro': {'nome': '💰 Financeiro', 'kpis': KPIS_FINANCEIRO}
}

def get_kpis_por_eixo(eixo):
    """Retorna KPIs de um eixo específico"""
    return TODOS_OS_EIXOS.get(eixo, {}).get('kpis', {})

def get_nome_eixo(eixo):
    """Retorna nome formatado do eixo"""
    return TODOS_OS_EIXOS.get(eixo, {}).get('nome', eixo.title())
