"""
Mapeamento completo dos 38 KPIs com informações de agregação correta
"""

VIVO_COLORS = {
    'neon_purple': '#9D4EDD',
    'neon_pink': '#FF006E',
    'neon_cyan': '#00F5FF',
    'neon_green': '#39FF14',
    'neon_gold': '#FFD700',
    'text': '#FFFFFF'
}

# ============================================================================
# RESUMO EXECUTIVO - 6 KPIs
# ============================================================================

KPIS_RESUMO = {
    'nps': {
        'nome': 'NPS',
        'coluna': 'NPS',
        'tipo_agregacao': 'MEDIA',  # Média simples
        'meta': 70,
        'inverter': False,
        'cor': VIVO_COLORS['neon_purple']
    },
    'ocupacao': {
        'nome': 'Ocupação %',

        'tipo_agregacao': 'RAZAO',  # Numerador / Denominador
        'coluna_numerador': 'Ocupacao_Tempo_Ocupado_Hrs',
        'coluna_denominador': 'Tempo_Logado_Hrs',
        'meta': 85,
        'inverter': False,
        'cor': VIVO_COLORS['neon_pink']
    },
    'absenteismo': {
        'nome': 'Absenteísmo %',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Absenteismo_Dias_Ausentes',
        'coluna_denominador': 'Absenteismo_Dias_Uteis',
        'meta': 5,
        'inverter': True,
        'cor': VIVO_COLORS['neon_cyan']
    },
    'tma': {
        'nome': 'TMA (seg)',
        'coluna': 'TMA_Seg',
        'tipo_agregacao': 'MEDIA_PONDERADA',  # Tempo total / Chamadas
        'coluna_numerador': 'TMA_Tempo_Total_Seg',
        'coluna_peso': 'Chamadas_Atendidas',
        'meta': 300,
        'inverter': True,
        'cor': VIVO_COLORS['neon_gold']
    },
    'conversao': {
        'nome': 'Conversão %',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Conversao_Numerador',
        'coluna_denominador': 'Conversao_Denominador',
        'meta': 15,
        'inverter': False,
        'cor': VIVO_COLORS['neon_pink']
    },
    'sla': {
        'nome': 'SLA %',

        'tipo_agregacao': 'MEDIA',  # Média simples
        'meta': 90,
        'inverter': False,
        'cor': VIVO_COLORS['neon_green']
    }
}

# ============================================================================
# QUALIDADE - 8 KPIs
# ============================================================================

KPIS_QUALIDADE = {
    'rechamadas_24h': {
        'nome': '% Rechamadas 24hs',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Rechamadas_24h_Numerador',
        'coluna_denominador': 'Rechamadas_24h_Denominador',
        'meta': 5,
        'inverter': True,
        'cor': VIVO_COLORS['neon_purple']
    },
    'rechamadas_7d': {
        'nome': '% Rechamadas 7 dias',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Rechamadas_7d_Numerador',
        'coluna_denominador': 'Rechamadas_7d_Denominador',
        'meta': 10,
        'inverter': True,
        'cor': VIVO_COLORS['neon_pink']
    },
    'transferencia': {
        'nome': '% Transferência',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Transferencia_Numerador',
        'coluna_denominador': 'Transferencia_Denominador',
        'meta': 15,
        'inverter': True,
        'cor': VIVO_COLORS['neon_cyan']
    },
    'nota_tdna': {
        'nome': 'Nota TDNA',
        'coluna': 'Nota_TDNA',
        'tipo_agregacao': 'MEDIA',
        'meta': 8,
        'inverter': False,
        'cor': VIVO_COLORS['neon_gold']
    },
    'falha_operacional': {
        'nome': '% Falha Operacional',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Falha_Operacional_Numerador',
        'coluna_denominador': 'Falha_Operacional_Denominador',
        'meta': 3,
        'inverter': True,
        'cor': VIVO_COLORS['neon_purple']
    },
    'aderencia_processual': {
        'nome': '% Aderência Processual',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Aderencia_Processual_Numerador',
        'coluna_denominador': 'Aderencia_Processual_Denominador',
        'meta': 95,
        'inverter': False,
        'cor': VIVO_COLORS['neon_pink']
    },
    'nota_monitoria': {
        'nome': 'Nota Monitoria Whisper',
        'coluna': 'Nota_Monitoria_Whisper',
        'tipo_agregacao': 'MEDIA',
        'meta': 8,
        'inverter': False,
        'cor': VIVO_COLORS['neon_cyan']
    },
    'callback': {
        'nome': '% CallBack tentado e efetivado',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Callback_Numerador',
        'coluna_denominador': 'Callback_Denominador',
        'meta': 80,
        'inverter': False,
        'cor': VIVO_COLORS['neon_gold']
    }
}

# ============================================================================
# PRODUÇÃO - 10 KPIs
# ============================================================================

KPIS_PRODUCAO = {
    'chamadas_atendidas': {
        'nome': 'Chamadas Atendidas',
        'coluna': 'Chamadas_Atendidas',
        'tipo_agregacao': 'SOMA',
        'meta': None,
        'inverter': False,
        'cor': VIVO_COLORS['neon_purple']
    },
    'abandono': {
        'nome': '%Abandono',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Abandono_Numerador',
        'coluna_denominador': 'Abandono_Denominador',
        'meta': 5,
        'inverter': True,
        'cor': VIVO_COLORS['neon_pink']
    },
    'rgc': {
        'nome': '% RGC',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'RGC_Numerador',
        'coluna_denominador': 'RGC_Denominador',
        'meta': 10,
        'inverter': False,
        'cor': VIVO_COLORS['neon_cyan']
    },
    'tma_producao': {
        'nome': 'TMA',
        'coluna': 'TMA_Seg',
        'tipo_agregacao': 'MEDIA_PONDERADA',
        'coluna_numerador': 'TMA_Producao_Tempo_Total',
        'coluna_peso': 'Chamadas_Atendidas',
        'meta': 300,
        'inverter': True,
        'cor': VIVO_COLORS['neon_gold']
    },
    'pausa': {
        'nome': '% Pausa',

        'tipo_agregacao': 'MEDIA',  # Pode ser média simples
        'meta': 10,
        'inverter': True,
        'cor': VIVO_COLORS['neon_purple']
    },
    'tempo_logado': {
        'nome': 'Tempo Logado',
        'coluna': 'Tempo_Logado_Hrs',
        'tipo_agregacao': 'SOMA',
        'formato': 'HH:MM:SS',
        'meta': 6,
        'inverter': False,
        'cor': VIVO_COLORS['neon_pink']
    },
    'abs': {
        'nome': '% Abs',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Abs_Dias_Ausentes',
        'coluna_denominador': 'Abs_Dias_Uteis',
        'meta': 5,
        'inverter': True,
        'cor': VIVO_COLORS['neon_cyan']
    },
    'to': {
        'nome': 'TO',

        'tipo_agregacao': 'MEDIA',  # Turnover pode ser média
        'meta': 3,
        'inverter': True,
        'cor': VIVO_COLORS['neon_gold']
    },
    'produtividade_hc': {
        'nome': 'Produtividade / HC',
        'coluna': 'Produtividade_HC',
        'tipo_agregacao': 'SOMA',
        'meta': 100,
        'inverter': False,
        'cor': VIVO_COLORS['neon_purple']
    },
    'margem_operacional': {
        'nome': 'Margem Operacional (DRE)',

        'tipo_agregacao': 'MEDIA',  # Margem pode ser média
        'meta': 15,
        'inverter': False,
        'cor': VIVO_COLORS['neon_pink']
    }
}

# ============================================================================
# NEGÓCIOS - 7 KPIs
# ============================================================================

KPIS_NEGOCIOS = {
    'negocios_totais': {
        'nome': 'Qnt. Negócios totais',
        'coluna': 'Qnt_Negocios_Totais',
        'tipo_agregacao': 'SOMA',
        'meta': None,
        'inverter': False,
        'cor': VIVO_COLORS['neon_purple']
    },
    'conversao_negocios': {
        'nome': '% Conversão',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Conversao_Negocios_Numerador',
        'coluna_denominador': 'Conversao_Negocios_Denominador',
        'meta': 15,
        'inverter': False,
        'cor': VIVO_COLORS['neon_pink']
    },
    'churn': {
        'nome': '% Churn FTTH / Pós',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Churn_Numerador',
        'coluna_denominador': 'Churn_Denominador',
        'meta': 2,
        'inverter': True,
        'cor': VIVO_COLORS['neon_cyan']
    },
    'cancelamento_ftth': {
        'nome': '% Cancelamento de FTTH',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Cancelamento_FTTH_Numerador',
        'coluna_denominador': 'Cancelamento_FTTH_Denominador',
        'meta': 5,
        'inverter': True,
        'cor': VIVO_COLORS['neon_gold']
    },
    'rentabilizacoes': {
        'nome': 'R$ Rentabilizações totais',
        'coluna': 'Rentabilizacoes_Totais_RS',
        'tipo_agregacao': 'SOMA',
        'meta': None,
        'inverter': False,
        'cor': VIVO_COLORS['neon_purple']
    },
    'taxa_retencao': {
        'nome': '%Taxa de Retenção',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Taxa_Retencao_Numerador',
        'coluna_denominador': 'Taxa_Retencao_Denominador',
        'meta': 85,
        'inverter': False,
        'cor': VIVO_COLORS['neon_pink']
    },
    'arrecadacao': {
        'nome': '% arrecadação',

        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Arrecadacao_Numerador',
        'coluna_denominador': 'Arrecadacao_Denominador',
        'meta': 90,
        'inverter': False,
        'cor': VIVO_COLORS['neon_cyan']
    }
}

# ============================================================================
# FINANCEIRO - 7 KPIs
# ============================================================================

KPIS_FINANCEIRO = {
    'custo_prv': {
        'nome': 'Custo PRV mensal',
        'coluna': 'Custo_PRV_Mensal_RS',
        'tipo_agregacao': 'SOMA',
        'meta': None,
        'inverter': True,
        'cor': VIVO_COLORS['neon_purple']
    },
    'compensation': {
        'nome': 'Compensation Total',
        'coluna': 'Compensation_Total_RS',
        'tipo_agregacao': 'SOMA',
        'meta': None,
        'inverter': True,
        'cor': VIVO_COLORS['neon_pink']
    },
    'gastos_ferias': {
        'nome': 'Gastos Férias',
        'coluna': 'Gastos_Ferias_RS',
        'tipo_agregacao': 'SOMA',
        'meta': None,
        'inverter': True,
        'cor': VIVO_COLORS['neon_cyan']
    },
    'custo_he': {
        'nome': 'Custo HE',
        'coluna': 'Custo_HE_RS',
        'tipo_agregacao': 'SOMA',
        'meta': None,
        'inverter': True,
        'cor': VIVO_COLORS['neon_gold']
    },
    'custo_unitario': {
        'nome': 'Custo unitário por Operação',
        'coluna': 'Custo_Unitario_Operacao_RS',
        'tipo_agregacao': 'MEDIA',  # Média ponderada seria melhor, mas aceita média simples
        'meta': 25,
        'inverter': True,
        'cor': VIVO_COLORS['neon_purple']
    },
    'custo_margem_hc': {
        'nome': 'Custo / margem por HC',
        'coluna': 'Custo_Margem_HC_RS',
        'tipo_agregacao': 'SOMA',
        'meta': None,
        'inverter': True,
        'cor': VIVO_COLORS['neon_pink']
    },
    'valor_taxi': {
        'nome': 'Valor Taxi',
        'coluna': 'Valor_Taxi_RS',
        'tipo_agregacao': 'SOMA',
        'meta': None,
        'inverter': True,
        'cor': VIVO_COLORS['neon_cyan']
    }
}

# ============================================================================
# DICIONÁRIO COMPLETO (para fácil acesso)
# ============================================================================

TODOS_KPIS = {
    'resumo': KPIS_RESUMO,
    'qualidade': KPIS_QUALIDADE,
    'producao': KPIS_PRODUCAO,
    'negocios': KPIS_NEGOCIOS,
    'financeiro': KPIS_FINANCEIRO
}
