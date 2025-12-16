#!/usr/bin/env python3.11
"""
Dashboard KPIs Insourcing - Vivo Fibra
Versão Final Otimizada
"""

import dash
from dash import dcc, html, Input, Output, State, ALL, callback_context
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import base64
from functools import lru_cache
import json

# Importar KPIs com informações de agregação
from kpis_completos_com_agregacao import (
    KPIS_RESUMO, KPIS_QUALIDADE, KPIS_PRODUCAO, 
    KPIS_NEGOCIOS, KPIS_FINANCEIRO, TODOS_KPIS, VIVO_COLORS
)

# ============================================================================
# CONFIGURAÇÃO E CACHE GLOBAL
# ============================================================================

DATA_DIR = Path(__file__).parent / 'data'
ASSETS_DIR = Path(__file__).parent / 'assets'

_DADOS_CACHE = None

def calcular_percentuais_dinamicos(df):
    """
    Calcula percentuais dinamicamente a partir de numerador/denominador
    (Otimização: campos _Pct foram removidos do banco)
    """
    # Evitar divisão por zero
    def safe_divide(num, den):
        return np.where(den != 0, (num / den) * 100, 0)
    
    # Lista de KPIs que precisam de cálculo percentual
    calculos = [
        ('Ocupacao_Pct', 'Ocupacao_Numerador', 'Ocupacao_Denominador'),
        ('Absenteismo_Pct', 'Absenteismo_Numerador', 'Absenteismo_Denominador'),
        ('SLA_Atendimento_Pct', 'SLA_Atendimento_Numerador', 'SLA_Atendimento_Denominador'),
        ('Conversao_Pct', 'Conversao_Numerador', 'Conversao_Denominador'),
        ('Rechamadas_24h_Pct', 'Rechamadas_24h_Numerador', 'Rechamadas_24h_Denominador'),
        ('Rechamadas_7d_Pct', 'Rechamadas_7d_Numerador', 'Rechamadas_7d_Denominador'),
        ('Transferencia_Pct', 'Transferencia_Numerador', 'Transferencia_Denominador'),
        ('Falha_Operacional_Pct', 'Falha_Operacional_Numerador', 'Falha_Operacional_Denominador'),
        ('Aderencia_Processual_Pct', 'Aderencia_Processual_Numerador', 'Aderencia_Processual_Denominador'),
        ('CallBack_Tentado_Efetivado_Pct', 'Callback_Numerador', 'Callback_Denominador'),
        ('Abandono_Pct', 'Abandono_Numerador', 'Abandono_Denominador'),
        ('RGC_Pct', 'RGC_Numerador', 'RGC_Denominador'),
        ('Pausa_Pct', 'Pausa_Numerador', 'Pausa_Denominador'),
        ('TO_Pct', 'TO_Numerador', 'TO_Denominador'),
        ('Churn_FTTH_Pos_Pct', 'Churn_Numerador', 'Churn_Denominador'),
        ('Cancelamento_FTTH_Pct', 'Cancelamento_FTTH_Numerador', 'Cancelamento_FTTH_Denominador'),
        ('Taxa_Retencao_Pct', 'Taxa_Retencao_Numerador', 'Taxa_Retencao_Denominador'),
        ('Arrecadacao_Pct', 'Arrecadacao_Numerador', 'Arrecadacao_Denominador'),
        ('Margem_Operacional_DRE_Pct', 'Margem_Operacional_DRE_Numerador', 'Margem_Operacional_DRE_Denominador'),
    ]
    
    # Calcular cada percentual
    for col_pct, col_num, col_den in calculos:
        if col_num in df.columns and col_den in df.columns:
            df[col_pct] = safe_divide(df[col_num], df[col_den])
    
    return df

def carregar_dados_global():
    """Carrega dados uma única vez e mantém em cache"""
    global _DADOS_CACHE
    
    if _DADOS_CACHE is not None:
        return _DADOS_CACHE
    
    print("🔄 Carregando dados...")
    
    df_metricas = pd.read_csv(DATA_DIR / 'fato_metricas_diarias.csv')
    df_metricas['Data'] = pd.to_datetime(df_metricas['Data'])
    df_metricas['Ano'] = df_metricas['Data'].dt.year
    df_metricas['Mes'] = df_metricas['Data'].dt.month
    df_metricas['Periodo_M'] = df_metricas['Data'].dt.to_period('M')
    df_metricas['Periodo_W'] = df_metricas['Data'].dt.to_period('W')
    df_metricas['Periodo_D'] = df_metricas['Data'].dt.date
    
    # Calcular percentuais dinamicamente a partir de numerador/denominador
    # (Campos _Pct foram removidos do banco para otimização)
    df_metricas = calcular_percentuais_dinamicos(df_metricas)
    
    _DADOS_CACHE = df_metricas
    
    print(f"✅ Dados carregados: {len(df_metricas)} registros")
    return df_metricas

# ============================================================================
# CORES E ESTILO VIVO FIBRA
# ============================================================================

# VIVO_COLORS e KPIS importados de kpis_completos_com_agregacao.py

# Cores adicionais para compatibilidade
VIVO_COLORS.update({
    'primary': '#660099',
    'secondary': '#A100FF',
    'gold': '#FFD700',
    'red': '#FF1744',
    'bg_dark': '#0A0118',
    'bg_medium': '#1A0B2E',
    'bg_card': '#2D1B4E',
    'success': '#00C853',
    'warning': '#FFB300',
    'danger': '#D32F2F',
    'gray_light': '#E0E0E0',
    'gray_medium': '#9E9E9E'
})

PLOTLY_TEMPLATE = {
    'layout': {
        'paper_bgcolor': 'rgba(26, 11, 46, 0.6)',
        'plot_bgcolor': 'rgba(10, 1, 24, 0.4)',
        'font': {'color': VIVO_COLORS['text'], 'family': 'Inter, sans-serif'},
        'title_font': {'size': 18, 'color': VIVO_COLORS['neon_pink']},
        'xaxis': {
            'gridcolor': 'rgba(255, 255, 255, 0.1)',
            'zerolinecolor': 'rgba(255, 255, 255, 0.2)'
        },
        'yaxis': {
            'gridcolor': 'rgba(255, 255, 255, 0.1)',
            'zerolinecolor': 'rgba(255, 255, 255, 0.2)'
        },
        'margin': {'l': 40, 'r': 40, 't': 60, 'b': 40}
    }
}

# KPIS já importados de kpis_completos_com_agregacao.py com informações de agregação

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def filtrar_dados(df, start_date, end_date, operacao, grupo, cidade, gerente):
    """Aplica filtros aos dados"""
    df_filtrado = df.copy()
    
    if start_date and end_date:
        df_filtrado = df_filtrado[
            (df_filtrado['Data'] >= start_date) & 
            (df_filtrado['Data'] <= end_date)
        ]
    
    if operacao and operacao != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Operacao'] == operacao]
    
    if grupo and grupo != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Grupo'] == grupo]
    
    if cidade and cidade != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Cidade'] == cidade]
    
    if gerente and gerente != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Gerente'] == gerente]
    
    return df_filtrado


def agregar_kpi_corretamente(df, kpi_info, granularidade='ME'):
    """
    Agrega KPI de acordo com seu tipo (MEDIA, RAZAO, MEDIA_PONDERADA, SOMA)
    """
    
    if len(df) == 0:
        return pd.DataFrame()
    
    tipo = kpi_info.get('tipo_agregacao', 'MEDIA')
    coluna = kpi_info['coluna']
    
    # Determinar coluna de agrupamento
    if granularidade == 'ME':
        grupo_col = df['Data'].dt.to_period('M')
    elif granularidade == 'W':
        grupo_col = df['Data'].dt.to_period('W')
    else:
        grupo_col = df['Data']
    
    if tipo == 'MEDIA':
        # Média simples (NPS, Notas)
        resultado = df.groupby(grupo_col)[coluna].mean().reset_index()
        resultado.columns = ['Data', coluna]
        
    elif tipo == 'RAZAO':
        # Soma numerador / Soma denominador * 100
        numerador = kpi_info.get('coluna_numerador')
        denominador = kpi_info.get('coluna_denominador')
        
        if numerador and denominador and numerador in df.columns and denominador in df.columns:
            soma_num = df.groupby(grupo_col)[numerador].sum()
            soma_den = df.groupby(grupo_col)[denominador].sum()
            
            resultado = pd.DataFrame({
                'Data': soma_num.index,
                coluna: (soma_num / soma_den * 100).fillna(0).values
            })
        else:
            # Fallback para média simples se não tiver numerador/denominador
            resultado = df.groupby(grupo_col)[coluna].mean().reset_index()
            resultado.columns = ['Data', coluna]
        
    elif tipo == 'MEDIA_PONDERADA':
        # Soma numerador / Soma peso
        numerador = kpi_info.get('coluna_numerador')
        peso = kpi_info.get('coluna_peso')
        
        if numerador and peso and numerador in df.columns and peso in df.columns:
            soma_num = df.groupby(grupo_col)[numerador].sum()
            soma_peso = df.groupby(grupo_col)[peso].sum()
            
            resultado = pd.DataFrame({
                'Data': soma_num.index,
                coluna: (soma_num / soma_peso).fillna(0).values
            })
        else:
            # Fallback para média simples
            resultado = df.groupby(grupo_col)[coluna].mean().reset_index()
            resultado.columns = ['Data', coluna]
        
    elif tipo == 'SOMA':
        # Soma simples (Chamadas, Custos)
        resultado = df.groupby(grupo_col)[coluna].sum().reset_index()
        resultado.columns = ['Data', coluna]
    
    else:
        # Default: média simples
        resultado = df.groupby(grupo_col)[coluna].mean().reset_index()
        resultado.columns = ['Data', coluna]
    
    # Converter Data para timestamp se for Period
    if hasattr(resultado['Data'].iloc[0], 'to_timestamp'):
        resultado['Data'] = resultado['Data'].apply(lambda x: x.to_timestamp())
    
    return resultado


def criar_pivot_otimizado(df, kpi_coluna, dimensao, kpi_info, granularidade='ME', max_periodos=30):
    """Cria pivot table otimizado com agregação inteligente"""
    
    if len(df) == 0 or kpi_coluna not in df.columns:
        return pd.DataFrame()
    
    if granularidade == 'ME':
        periodo_col = 'Periodo_M'
    elif granularidade == 'W':
        periodo_col = 'Periodo_W'
    else:
        periodo_col = 'Periodo_D'
    
    periodos_unicos = sorted(df[periodo_col].unique())[-max_periodos:]
    df_para_pivot = df[df[periodo_col].isin(periodos_unicos)].copy()
    
    try:
        tipo_agregacao = kpi_info.get('tipo_agregacao', 'MEDIA')
        
        if tipo_agregacao == 'RAZAO':
            # Para KPIs de razão, somar numerador e denominador
            col_num = kpi_info.get('coluna_numerador')
            col_den = kpi_info.get('coluna_denominador')
            
            if col_num and col_den and col_num in df_para_pivot.columns and col_den in df_para_pivot.columns:
                pivot_num = df_para_pivot.pivot_table(index=dimensao, columns=periodo_col, values=col_num, aggfunc='sum').fillna(0)
                pivot_den = df_para_pivot.pivot_table(index=dimensao, columns=periodo_col, values=col_den, aggfunc='sum').fillna(0)
                pivot = ((pivot_num / pivot_den.replace(0, 1)) * 100).fillna(0).round(2)
            else:
                # Fallback para média
                pivot = df_para_pivot.pivot_table(index=dimensao, columns=periodo_col, values=kpi_coluna, aggfunc='mean').fillna(0).round(2)
        
        elif tipo_agregacao == 'MEDIA_PONDERADA':
            # Para médias ponderadas (TMA)
            col_num = kpi_info.get('coluna_numerador')
            col_peso = kpi_info.get('coluna_peso')
            
            if col_num and col_peso and col_num in df_para_pivot.columns and col_peso in df_para_pivot.columns:
                pivot_num = df_para_pivot.pivot_table(index=dimensao, columns=periodo_col, values=col_num, aggfunc='sum').fillna(0)
                pivot_peso = df_para_pivot.pivot_table(index=dimensao, columns=periodo_col, values=col_peso, aggfunc='sum').fillna(0)
                pivot = (pivot_num / pivot_peso.replace(0, 1)).fillna(0).round(2)
            else:
                # Fallback para média
                pivot = df_para_pivot.pivot_table(index=dimensao, columns=periodo_col, values=kpi_coluna, aggfunc='mean').fillna(0).round(2)
        
        elif tipo_agregacao == 'SOMA':
            # Soma simples
            pivot = df_para_pivot.pivot_table(index=dimensao, columns=periodo_col, values=kpi_coluna, aggfunc='sum').fillna(0).round(2)
        
        else:
            # MEDIA: média simples
            pivot = df_para_pivot.pivot_table(index=dimensao, columns=periodo_col, values=kpi_coluna, aggfunc='mean').fillna(0).round(2)
        
        # Converter colunas para formato de data
        if granularidade == 'ME':
            pivot.columns = [pd.Period(col, 'M').strftime('%m/%y') if isinstance(col, pd.Period) else str(col)[:5].replace('-', '/') for col in pivot.columns]
        elif granularidade == 'W':
            # Formato semanal: "abr\n01 à 07"
            novos_nomes = []
            for col in pivot.columns:
                if isinstance(col, pd.Period):
                    # Pegar primeira e última data da semana
                    start_date = col.start_time
                    end_date = col.end_time
                    
                    # Se virada de mês, usar mês que se encerra
                    if start_date.month != end_date.month:
                        mes_nome = end_date.strftime('%b').lower()
                    else:
                        mes_nome = start_date.strftime('%b').lower()
                    
                    # Formato: "abr\n01 à 07"
                    nome_col = f"{mes_nome}\n{start_date.day:02d} à {end_date.day:02d}"
                    novos_nomes.append(nome_col)
                else:
                    novos_nomes.append(str(col))
            pivot.columns = novos_nomes
        else:
            pivot.columns = [pd.to_datetime(col).strftime('%d/%m/%y') if not isinstance(col, str) else col for col in pivot.columns]
        
        return pivot
    except Exception as e:
        print(f"Erro ao criar pivot: {e}")
        return pd.DataFrame()

def criar_grafico_evolutivo(df, kpi_info, granularidade='ME'):
    """Cria gráfico de evolução temporal com agregação correta"""
    
    if len(df) == 0:
        return go.Figure()
    
    # Usar agregação inteligente
    df_agrupado = agregar_kpi_corretamente(df, kpi_info, granularidade)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_agrupado['Data'],
        y=df_agrupado[kpi_info['coluna']],
        mode='lines+markers',
        name=kpi_info['nome'],
        line=dict(color=kpi_info['cor'], width=3),
        marker=dict(size=8, color=kpi_info['cor']),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(list(bytes.fromhex(kpi_info['cor'][1:])) + [0.2])}"
    ))
    
    if 'meta' in kpi_info and kpi_info['meta'] is not None:
        fig.add_hline(
            y=kpi_info['meta'],
            line_dash="dash",
            line_color=VIVO_COLORS['neon_green'],
            annotation_text=f"Meta: {kpi_info['meta']}",
            annotation_position="right"
        )
    
    fig.update_layout(
        **PLOTLY_TEMPLATE['layout'],
        title=f"Evolução: {kpi_info['nome']}",
        xaxis_title='Período',
        yaxis_title=kpi_info['nome'],
        hovermode='x unified',
        showlegend=False
    )
    
    return fig

def criar_tabela_dash(pivot_df, titulo):
    """Cria tabela com fundo branco, texto preto e scroll horizontal"""
    
    if pivot_df.empty:
        return html.Div("Sem dados", style={'color': VIVO_COLORS['text'], 'padding': '20px'})
    
    df_table = pivot_df.reset_index()
    
    # Formatar valores com vírgula em vez de ponto
    for col in df_table.columns:
        if df_table[col].dtype in ['float64', 'float32']:
            df_table[col] = df_table[col].apply(lambda x: f"{x:.2f}".replace('.', ',') if pd.notna(x) else '')
    
    # Estilo de tabela com fundo branco e fonte menor
    header_style = {
        'backgroundColor': VIVO_COLORS['primary'],
        'color': '#FFFFFF',
        'fontWeight': '600',
        'textAlign': 'center',
        'padding': '6px 4px',
        'fontSize': '0.65rem',
        'whiteSpace': 'pre-wrap',  # Permite quebra de linha
        'minWidth': '50px'
    }
    
    cell_style = {
        'textAlign': 'center',
        'padding': '4px 3px',
        'borderBottom': '1px solid #E0E0E0',
        'fontSize': '0.6rem',
        'whiteSpace': 'nowrap',
        'minWidth': '45px'
    }
    
    # Criar tabela HTML customizada
    header = html.Thead(
        html.Tr([html.Th(col, style=header_style) for col in df_table.columns])
    )
    
    rows = []
    for i, row in df_table.iterrows():
        bg_color = '#FFFFFF' if i % 2 == 0 else '#F5F5F5'  # Linhas alternadas
        row_cells = [
            html.Td(str(row[col]), style={**cell_style, 'backgroundColor': bg_color})
            for col in df_table.columns
        ]
        rows.append(html.Tr(row_cells))
    
    body = html.Tbody(rows)
    
    table = html.Table(
        [header, body],
        style={
            'width': 'auto',
            'borderCollapse': 'collapse',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'minWidth': '100%'
        }
    )
    
    # Container com scroll horizontal
    return html.Div([
        html.H6(
            titulo,
            style={
                'color': VIVO_COLORS['neon_pink'],
                'marginBottom': '10px',
                'fontSize': '0.85rem',
                'fontWeight': '600',
                'textShadow': f'0 0 10px {VIVO_COLORS["neon_pink"]}'
            }
        ),
        html.Div(
            table,
            style={
                'overflowX': 'auto',  # Scroll horizontal apenas na tabela
                'overflowY': 'visible',
                'maxWidth': '100%'
            }
        )
    ], style={
        'backgroundColor': '#FFFFFF',
        'border': f'2px solid {VIVO_COLORS["primary"]}',
        'borderRadius': '8px',
        'padding': '12px',
        'marginBottom': '20px'
    })

def formatar_valor_kpi(valor, formato=None):
    """Formata valor do KPI de acordo com o formato especificado"""
    if pd.isna(valor):
        return "--"
    
    if formato == 'HH:MM:SS':
        # Já vem no formato HH:MM:SS do banco, retornar como texto
        return str(valor)
    else:
        # Formato padrão com vírgula
        return f"{valor:.1f}".replace('.', ',')


def criar_card_kpi(titulo, valor, meta, kpi_id, cor):
    """Cria card de KPI com status de meta (layout antigo)"""
    
    # Determinar status baseado na meta
    status_icon = "●"
    status_text = ""
    cor_borda = cor
    cor_valor = cor
    glow_color = f'rgba{tuple(list(bytes.fromhex(cor[1:])) + [0.3])}'
    atingimento_pct = 0
    
    # Verificar se KPI tem formato especial
    kpi_info = KPIS_RESUMO.get(kpi_id, {}) or KPIS_QUALIDADE.get(kpi_id, {}) or KPIS_PRODUCAO.get(kpi_id, {}) or KPIS_NEGOCIOS.get(kpi_id, {}) or KPIS_FINANCEIRO.get(kpi_id, {})
    formato = kpi_info.get('formato', None)
    
    if meta and not pd.isna(valor):
        try:
            # Verificar se KPI deve ser invertido (menor é melhor)
            inverter = KPIS_RESUMO.get(kpi_id, {}).get('inverter', False)
            
            if inverter:
                # Para KPIs onde menor é melhor (absenteísmo, TMA)
                atingimento_pct = (meta / float(valor)) * 100 if float(valor) > 0 else 100
                if float(valor) <= float(meta):
                    cor_borda = VIVO_COLORS['success']
                    cor_valor = VIVO_COLORS['success']
                    status_icon = "✓"
                    status_text = "Meta atingida"
                    glow_color = 'rgba(0, 200, 83, 0.4)'
                elif float(valor) <= float(meta) * 1.1:
                    cor_borda = VIVO_COLORS['warning']
                    cor_valor = VIVO_COLORS['warning']
                    status_icon = "⚠"
                    status_text = "Atenção"
                    glow_color = 'rgba(255, 179, 0, 0.3)'
                else:
                    cor_borda = VIVO_COLORS['danger']
                    cor_valor = VIVO_COLORS['danger']
                    status_icon = "✗"
                    status_text = "Crítico"
                    glow_color = 'rgba(211, 47, 47, 0.4)'
            else:
                # Para KPIs onde maior é melhor (NPS, Ocupação, etc)
                atingimento_pct = (float(valor) / float(meta)) * 100
                if float(valor) >= float(meta):
                    cor_borda = VIVO_COLORS['success']
                    cor_valor = VIVO_COLORS['success']
                    status_icon = "✓"
                    status_text = "Meta atingida"
                    glow_color = 'rgba(0, 200, 83, 0.4)'
                elif float(valor) >= float(meta) * 0.9:
                    cor_borda = VIVO_COLORS['warning']
                    cor_valor = VIVO_COLORS['warning']
                    status_icon = "⚠"
                    status_text = "Atenção"
                    glow_color = 'rgba(255, 179, 0, 0.3)'
                else:
                    cor_borda = VIVO_COLORS['danger']
                    cor_valor = VIVO_COLORS['danger']
                    status_icon = "✗"
                    status_text = "Crítico"
                    glow_color = 'rgba(211, 47, 47, 0.4)'
        except:
            pass
    
    return dbc.Card([
        dbc.CardBody([
            html.P(titulo, style={
                'fontSize': '0.7rem',
                'color': VIVO_COLORS['gray_medium'],
                'marginBottom': '0.25rem',
                'fontWeight': '600',
                'textTransform': 'uppercase',
                'letterSpacing': '1px'
            }),
            html.H3(formatar_valor_kpi(valor, formato), style={
                'color': cor_valor,
                'fontWeight': 'bold',
                'margin': '0.25rem 0',
                'fontSize': '1.5rem',
                'textShadow': f'0 0 10px {glow_color}'
            }),
            html.Div([
                html.Span(status_icon, style={
                    'color': cor_borda,
                    'marginRight': '0.25rem',
                    'fontSize': '0.9rem',
                    'textShadow': f'0 0 8px {glow_color}'
                }),
                html.Span(status_text, style={
                    'fontSize': '0.9rem',
                    'color': cor_borda,
                    'fontWeight': '600'
                })
            ], style={'marginTop': '0.25rem'}) if status_text else None,
            html.Div(f"{atingimento_pct:.0f}% da meta", style={
                'fontSize': '0.65rem',
                'color': VIVO_COLORS['gray_light'],
                'marginTop': '0.25rem'
            }) if meta else None
        ], style={'padding': '0.75rem'})
    ], style={
        'height': '100%',
        'background': f'linear-gradient(135deg, rgba(45, 27, 78, 0.6), rgba(26, 11, 46, 0.8))',
        'border': f'1px solid rgba(255, 255, 255, 0.1)',
        'borderLeft': f'3px solid {cor_borda}',
        'borderRadius': '12px',
        'boxShadow': f'0 4px 20px {glow_color}',
        'backdropFilter': 'blur(10px)',
        'marginBottom': '0.5rem'
    })

# ============================================================================
# CARREGAR LOGO
# ============================================================================

def carregar_logo():
    logo_path = ASSETS_DIR / 'logo_vivo_correto.png'
    if logo_path.exists():
        with open(logo_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

# ============================================================================
# APLICAÇÃO DASH
# ============================================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True
)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard KPIs Insourcing - Vivo</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(135deg, #0A0118 0%, #1A0B2E 50%, #2D1B4E 100%);
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
                overflow-x: hidden;
                max-width: 100vw;
                box-sizing: border-box;
            }
            * {
                box-sizing: border-box;
            }
            .container-fluid {
                padding-left: 20px !important;
                padding-right: 20px !important;
                max-width: 100% !important;
                margin: 0 !important;
            }
            .row {
                margin-left: 0 !important;
                margin-right: 0 !important;
            }
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: rgba(26, 11, 46, 0.4);
            }
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(180deg, #660099, #FF00FF);
                border-radius: 4px;
            }
            /* Dropdown styling */
            .Select-control {
                background-color: rgba(26, 11, 46, 0.8) !important;
                border-color: rgba(255, 255, 255, 0.2) !important;
            }
            .Select-value-label, .Select-placeholder, .Select-input input {
                color: #FFFFFF !important;
            }
            .Select-option {
                background-color: rgba(26, 11, 46, 0.95) !important;
                color: #FFFFFF !important;
            }
            .Select-option:hover {
                background-color: rgba(102, 0, 153, 0.8) !important;
            }
            /* Texto selecionado visível */
            .Select-value {
                color: #FFFFFF !important;
            }
            .Select-value-label {
                color: #FFFFFF !important;
            }
            /* DatePicker styling */
            .DateInput {
                background-color: rgba(26, 11, 46, 0.8) !important;
            }
            .DateInput_input {
                color: #FFFFFF !important;
                background-color: transparent !important;
                font-size: 0.85rem !important;
                height: 0.82cm !important;
                padding: 2px 8px !important;
                line-height: 0.78cm !important;
            }
            .DateInput_input::placeholder {
                color: rgba(255, 255, 255, 0.5) !important;
            }
            .DateRangePickerInput {
                background-color: rgba(26, 11, 46, 0.8) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }
            .DateRangePickerInput__withBorder {
                background-color: rgba(26, 11, 46, 0.8) !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

logo_encoded = carregar_logo()

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                # Logo à esquerda
                html.Img(
                    src=f'data:image/png;base64,{logo_encoded}' if logo_encoded else '',
                    style={
                        'height': '126px',
                        'position': 'absolute',
                        'left': '20px',
                        'top': '7px',
                        'filter': 'drop-shadow(0 0 20px rgba(255, 0, 255, 0.6))'
                    }
                ),
                # Título centralizado (alinhado verticalmente com logo)
                html.Div([
                    html.H1(
                        "Dashboard de KPIs - Insourcing",
                        style={
                            'color': VIVO_COLORS['text'],
                            'fontSize': '1.8rem',
                            'fontWeight': '700',
                            'marginBottom': '5px',
                            'textShadow': f'0 0 20px {VIVO_COLORS["neon_pink"]}',
                            'lineHeight': '126px'  # Alinhado com altura do logo
                        }
                    ),
                    html.P(
                        "Monitoramento de Operações B2C e B2B",
                        style={
                            'color': VIVO_COLORS['neon_cyan'],
                            'fontSize': '0.9rem',
                            'marginBottom': '0',
                            'textShadow': f'0 0 10px {VIVO_COLORS["neon_cyan"]}',
                            'position': 'absolute',
                            'bottom': '10px',
                            'width': '100%',
                            'textAlign': 'center'
                        }
                    )
                ], style={'textAlign': 'center', 'position': 'relative', 'height': '126px'})
            ], style={
                'background': f'linear-gradient(90deg, {VIVO_COLORS["bg_dark"]}, {VIVO_COLORS["bg_medium"]}, {VIVO_COLORS["primary"]})',
                'padding': '7px 15px',
                'borderRadius': '12px',
                'boxShadow': f'0 4px 20px rgba(255, 0, 255, 0.3)',
                'marginBottom': '20px',
                'position': 'relative',
                'height': '140px'
            })
        ], width=12)
    ]),
    
    # Filtros
    dbc.Row([
        dbc.Col([
            html.Label("Período:", style={'color': VIVO_COLORS['text'], 'fontSize': '0.85rem', 'fontWeight': '600'}),
            dcc.DatePickerRange(
                id='filtro-periodo',
                start_date='2024-01-01',
                end_date='2024-12-31',
                display_format='DD/MM/YYYY',
                style={'width': '100%'}
            )
        ], md=3),
        dbc.Col([
            html.Label("Operação:", style={'color': VIVO_COLORS['text'], 'fontSize': '0.85rem', 'fontWeight': '600'}),
            dcc.Dropdown(
                id='filtro-operacao',
                options=[
                    {'label': 'Todas', 'value': 'Todas'},
                    {'label': 'B2C', 'value': 'B2C'},
                    {'label': 'B2B', 'value': 'B2B'}
                ],
                value='Todas',
                style={'fontSize': '0.85rem'}
            )
        ], md=2),
        dbc.Col([
            html.Label("Grupo:", style={'color': VIVO_COLORS['text'], 'fontSize': '0.85rem', 'fontWeight': '600'}),
            dcc.Dropdown(
                id='filtro-grupo',
                value='Todos',
                style={'fontSize': '0.85rem'}
            )
        ], md=2),
        dbc.Col([
            html.Label("Cidade:", style={'color': VIVO_COLORS['text'], 'fontSize': '0.85rem', 'fontWeight': '600'}),
            dcc.Dropdown(
                id='filtro-cidade',
                value='Todas',
                style={'fontSize': '0.85rem'}
            )
        ], md=2),
        dbc.Col([
            html.Label("Gerente:", style={'color': VIVO_COLORS['text'], 'fontSize': '0.85rem', 'fontWeight': '600'}),
            dcc.Dropdown(
                id='filtro-gerente',
                value='Todos',
                style={'fontSize': '0.85rem'}
            )
        ], md=2),
        dbc.Col([
            html.Label("Granularidade:", style={'color': VIVO_COLORS['text'], 'fontSize': '0.85rem', 'fontWeight': '600'}),
            dcc.Dropdown(
                id='filtro-granularidade',
                options=[
                    {'label': 'Mensal', 'value': 'ME'},
                    {'label': 'Semanal', 'value': 'W'},
                    {'label': 'Diário', 'value': 'D'}
                ],
                value='ME',
                style={'fontSize': '0.85rem'}
            )
        ], md=3)
    ], style={'marginBottom': '20px'}, className='g-2'),
    
    # Tabs
    dbc.Tabs(
        id='tabs',
        active_tab='resumo',
        children=[
            dbc.Tab(label='📈 Resumo', tab_id='resumo'),
            dbc.Tab(label='✅ Qualidade', tab_id='qualidade'),
            dbc.Tab(label='⚙️ Produção', tab_id='producao'),
            dbc.Tab(label='💼 Negócios', tab_id='negocios'),
            dbc.Tab(label='💰 Financeiro', tab_id='financeiro')
        ],
        style={'marginBottom': '20px'}
    ),
    
    # Conteúdo dinâmico
    html.Div(id='conteudo-pagina')
    
], fluid=True, style={
    'padding': '10px 20px',
    'maxWidth': '100%',
    'width': '100%',
    'margin': '0 auto',
    'overflowX': 'hidden',
    'boxSizing': 'border-box'
})

# ============================================================================
# CALLBACKS
# ============================================================================

# Callback para popular opções de Grupo
@app.callback(
    Output('filtro-grupo', 'options'),
    [Input('filtro-periodo', 'start_date'),
     Input('filtro-periodo', 'end_date'),
     Input('filtro-operacao', 'value')]
)
def atualizar_opcoes_grupo(start_date, end_date, operacao):
    """Popula opções de grupos"""
    df = carregar_dados_global()
    df_filtrado = filtrar_dados(df, start_date, end_date, operacao, None, None, None)
    grupos = ['Todos'] + sorted(df_filtrado['Grupo'].unique().tolist())
    return [{'label': g, 'value': g} for g in grupos]

# Callback para popular opções de Cidade (filtrado por Grupo)
@app.callback(
    Output('filtro-cidade', 'options'),
    [Input('filtro-periodo', 'start_date'),
     Input('filtro-periodo', 'end_date'),
     Input('filtro-operacao', 'value'),
     Input('filtro-grupo', 'value')]
)
def atualizar_opcoes_cidade(start_date, end_date, operacao, grupo):
    """Popula opções de cidades (filtradas por grupo se selecionado)"""
    df = carregar_dados_global()
    df_filtrado = filtrar_dados(df, start_date, end_date, operacao, None, None, None)
    
    # Filtrar por grupo se selecionado
    if grupo and grupo != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Grupo'] == grupo]
    
    cidades = ['Todas'] + sorted(df_filtrado['Cidade'].unique().tolist())
    return [{'label': c, 'value': c} for c in cidades]

# Callback para popular opções de Gerente (filtrado por Grupo e Cidade)
@app.callback(
    Output('filtro-gerente', 'options'),
    [Input('filtro-periodo', 'start_date'),
     Input('filtro-periodo', 'end_date'),
     Input('filtro-operacao', 'value'),
     Input('filtro-grupo', 'value'),
     Input('filtro-cidade', 'value')]
)
def atualizar_opcoes_gerente(start_date, end_date, operacao, grupo, cidade):
    """Popula opções de gerentes (filtradas por grupo e cidade se selecionados)"""
    df = carregar_dados_global()
    df_filtrado = filtrar_dados(df, start_date, end_date, operacao, None, None, None)
    
    # Filtrar por grupo se selecionado
    if grupo and grupo != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Grupo'] == grupo]
    
    # Filtrar por cidade se selecionada
    if cidade and cidade != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Cidade'] == cidade]
    
    gerentes = ['Todos'] + sorted(df_filtrado['Gerente'].unique().tolist())
    return [{'label': g, 'value': g} for g in gerentes]

@app.callback(
    Output('conteudo-pagina', 'children'),
    [
        Input('tabs', 'active_tab'),
        Input('filtro-periodo', 'start_date'),
        Input('filtro-periodo', 'end_date'),
        Input('filtro-operacao', 'value'),
        Input('filtro-grupo', 'value'),
        Input('filtro-cidade', 'value'),
        Input('filtro-gerente', 'value'),
        Input('filtro-granularidade', 'value'),
        Input({'type': 'radio-kpi', 'index': ALL}, 'value')
    ],
    prevent_initial_call=False
)
def atualizar_conteudo(tab, start_date, end_date, operacao, grupo, cidade, gerente, granularidade, radio_values):
    """Callback principal"""
    
    if not tab:
        tab = 'resumo'
    if not operacao:
        operacao = 'Todas'
    if not grupo:
        grupo = 'Todos'
    if not cidade:
        cidade = 'Todas'
    if not gerente:
        gerente = 'Todos'
    if not granularidade:
        granularidade = 'ME'
    
    df = carregar_dados_global()
    df_filtrado = filtrar_dados(df, start_date, end_date, operacao, grupo, cidade, gerente)
    
    if len(df_filtrado) == 0:
        return html.Div("Sem dados para o período selecionado", 
                       style={'color': VIVO_COLORS['text'], 'padding': '40px', 'textAlign': 'center'})
    
    kpi_selecionado = 'nps'
    if radio_values and any(radio_values):
        kpi_selecionado = [v for v in radio_values if v][0]
    
    kpi_info = KPIS_RESUMO.get(kpi_selecionado, KPIS_RESUMO['nps'])
    
    if tab == 'resumo':
        # Cards
        cards = []
        for kpi_id, kpi in KPIS_RESUMO.items():
            valor = df_filtrado[kpi['coluna']].mean()
            cards.append(
                dbc.Col([
                    criar_card_kpi(kpi['nome'], valor, kpi.get('meta'), kpi_id, kpi['cor'])
                ], xl=2, lg=3, md=4, sm=6, xs=12)
            )
        
        # Radio buttons
        radio_buttons = dcc.RadioItems(
            id={'type': 'radio-kpi', 'index': 'resumo'},
            options=[
                {'label': f" {kpi['nome']}", 'value': kpi_id}
                for kpi_id, kpi in KPIS_RESUMO.items()
            ],
            value=kpi_selecionado,
            inline=True,
            style={
                'color': VIVO_COLORS['text'],
                'fontSize': '0.9rem',
                'padding': '15px'
            },
            labelStyle={'marginRight': '20px', 'cursor': 'pointer'}
        )
        
        # Gráfico
        fig = criar_grafico_evolutivo(df_filtrado, kpi_info, granularidade)
        
        # Pivots
        pivot_operacao = criar_pivot_otimizado(df_filtrado, kpi_info['coluna'], 'Operacao', kpi_info, granularidade, 30)
        pivot_cidade = criar_pivot_otimizado(df_filtrado, kpi_info['coluna'], 'Cidade', kpi_info, granularidade, 30)
        pivot_gerente = criar_pivot_otimizado(df_filtrado, kpi_info['coluna'], 'Gerente', kpi_info, granularidade, 30)
        
        if not pivot_cidade.empty and len(pivot_cidade.columns) > 0:
            try:
                pivot_cidade = pivot_cidade.nlargest(5, pivot_cidade.columns[-1])
            except:
                pivot_cidade = pivot_cidade.head(5)
        
        return html.Div([
            dbc.Row(cards, style={'marginBottom': '20px'}, className='g-2'),
            
            html.Div([
                html.Label("Selecione o KPI para visualizar no gráfico:", 
                          style={'color': VIVO_COLORS['neon_pink'], 'fontWeight': '600', 'marginBottom': '10px'}),
                radio_buttons
            ], style={
                'backgroundColor': 'rgba(45, 27, 78, 0.6)',
                'backdropFilter': 'blur(10px)',
                'border': '1px solid rgba(255, 255, 255, 0.1)',
                'borderRadius': '12px',
                'padding': '15px',
                'marginBottom': '20px',
                'boxShadow': f'0 4px 20px rgba(255, 0, 255, 0.2)'
            }),
            
            dcc.Graph(figure=fig, config={'displayModeBar': False}, style={'marginBottom': '30px'}),
            
            html.H5("Tabelas Evolutivas", style={'color': VIVO_COLORS['neon_cyan'], 'marginBottom': '15px'}),
            criar_tabela_dash(pivot_operacao, f"{kpi_info['nome']} por Operação"),
            criar_tabela_dash(pivot_cidade, f"{kpi_info['nome']} por Grupo (Top 5)"),
            criar_tabela_dash(pivot_gerente, f"{kpi_info['nome']} por Gerente")
        ])
    
    # Outros eixos: Qualidade, Produção, Negócios, Financeiro
    eixos_kpis = {
        'qualidade': KPIS_QUALIDADE,
        'producao': KPIS_PRODUCAO,
        'negocios': KPIS_NEGOCIOS,
        'financeiro': KPIS_FINANCEIRO
    }
    
    if tab in eixos_kpis:
        kpis_eixo = eixos_kpis[tab]
        
        # Filtrar apenas KPIs com colunas existentes
        kpis_disponiveis = {k: v for k, v in kpis_eixo.items() if v['coluna'] in df_filtrado.columns}
        
        if not kpis_disponiveis:
            return html.Div(f"Nenhum KPI disponível para {tab}", 
                           style={'color': VIVO_COLORS['text'], 'padding': '40px', 'textAlign': 'center'})
        
        # Determinar KPI selecionado
        if not kpi_selecionado or kpi_selecionado not in kpis_disponiveis:
            kpi_selecionado = list(kpis_disponiveis.keys())[0]
        
        kpi_info = kpis_disponiveis[kpi_selecionado]
        
        # Cards
        cards = []
        for kpi_id, kpi in kpis_disponiveis.items():
            valor = df_filtrado[kpi['coluna']].mean()
            cards.append(
                dbc.Col([
                    criar_card_kpi(kpi['nome'], valor, kpi.get('meta'), kpi_id, kpi['cor'])
                ], xl=2, lg=3, md=4, sm=6, xs=12)
            )
        
        # Radio buttons
        radio_buttons = dcc.RadioItems(
            id={'type': 'radio-kpi', 'index': tab},
            options=[
                {'label': f" {kpi['nome']}", 'value': kpi_id}
                for kpi_id, kpi in kpis_disponiveis.items()
            ],
            value=kpi_selecionado,
            inline=True,
            style={
                'color': VIVO_COLORS['text'],
                'fontSize': '0.9rem',
                'padding': '15px'
            },
            labelStyle={'marginRight': '20px', 'cursor': 'pointer'}
        )
        
        # Gráfico
        fig = criar_grafico_evolutivo(df_filtrado, kpi_info, granularidade)
        
        # Pivots
        pivot_operacao = criar_pivot_otimizado(df_filtrado, kpi_info['coluna'], 'Operacao', kpi_info, granularidade, 30)
        pivot_cidade = criar_pivot_otimizado(df_filtrado, kpi_info['coluna'], 'Cidade', kpi_info, granularidade, 30)
        pivot_gerente = criar_pivot_otimizado(df_filtrado, kpi_info['coluna'], 'Gerente', kpi_info, granularidade, 30)
        
        if not pivot_cidade.empty and len(pivot_cidade.columns) > 0:
            try:
                pivot_cidade = pivot_cidade.nlargest(5, pivot_cidade.columns[-1])
            except:
                pivot_cidade = pivot_cidade.head(5)
        
        return html.Div([
            dbc.Row(cards, style={'marginBottom': '20px'}, className='g-2'),
            
            html.Div([
                html.Label("Selecione o KPI para visualizar no gráfico:", 
                          style={'color': VIVO_COLORS['neon_pink'], 'fontWeight': '600', 'marginBottom': '10px'}),
                radio_buttons
            ], style={
                'backgroundColor': 'rgba(45, 27, 78, 0.6)',
                'backdropFilter': 'blur(10px)',
                'border': '1px solid rgba(255, 255, 255, 0.1)',
                'borderRadius': '12px',
                'padding': '15px',
                'marginBottom': '20px',
                'boxShadow': f'0 4px 20px rgba(255, 0, 255, 0.2)'
            }),
            
            dcc.Graph(figure=fig, config={'displayModeBar': False}, style={'marginBottom': '30px'}),
            
            html.H5("Tabelas Evolutivas", style={'color': VIVO_COLORS['neon_cyan'], 'marginBottom': '15px'}),
            criar_tabela_dash(pivot_operacao, f"{kpi_info['nome']} por Operação"),
            criar_tabela_dash(pivot_cidade, f"{kpi_info['nome']} por Grupo (Top 5)"),
            criar_tabela_dash(pivot_gerente, f"{kpi_info['nome']} por Gerente")
        ])
    
    return html.Div(f"Página {tab} não encontrada", 
                   style={'color': VIVO_COLORS['text'], 'padding': '40px', 'textAlign': 'center'})

# ============================================================================
# EXECUTAR
# ============================================================================

if __name__ == '__main__':
    carregar_dados_global()
    app.run(debug=False, host='0.0.0.0', port=8050)
