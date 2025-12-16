# 🔧 Correção de Cálculo de Granularidade
## Dashboard KPIs Insourcing - Vivo Fibra

---

## ⚠️ **Problema Identificado**

O código atual usa **média simples** para agregar dados quando a granularidade muda (mensal → semanal → diário).

Isso está **INCORRETO** para a maioria dos KPIs!

---

## 📊 **Por Que Média Simples Está Errada?**

### **Exemplo: % Conversão**

**Dados diários:**
- Dia 1: 10 negócios / 100 chamadas = 10%
- Dia 2: 20 negócios / 50 chamadas = 40%

**Cálculo ERRADO (média simples):**
```
Conversão Semanal = (10% + 40%) / 2 = 25%
```

**Cálculo CORRETO (soma numerador/denominador):**
```
Conversão Semanal = (10 + 20) / (100 + 50) = 30 / 150 = 20%
```

**Diferença:** 25% vs 20% = **Erro de 25%!**

---

## 📋 **Classificação dos KPIs**

### **Tipo 1: MÉDIA (pode usar média simples)**
- NPS
- Nota TDNA
- Nota Monitoria Whisper

### **Tipo 2: RAZÃO (precisa numerador/denominador)**
- % Conversão = Negócios / Chamadas
- % Abandono = Abandonadas / Total
- % Ocupação = Tempo Ocupado / Tempo Logado
- % Absenteísmo = Dias Ausentes / Dias Úteis
- % RGC = RGC / Total
- % Pausa = Tempo Pausa / Tempo Logado
- % Transferência = Transferidas / Total
- % Rechamadas 24h = Rechamadas / Total
- % Rechamadas 7d = Rechamadas / Total
- % Falha Operacional = Falhas / Total
- % Aderência Processual = Aderente / Total
- % CallBack = CallBacks / Tentativas
- % Churn = Churns / Base
- % Cancelamento FTTH = Cancelamentos / Instalações
- % Taxa Retenção = Retidos / Total
- % Arrecadação = Arrecadado / Previsto
- Margem Operacional % = (Receita - Custo) / Receita

### **Tipo 3: MÉDIA PONDERADA (precisa peso)**
- TMA = Tempo Total / Chamadas Atendidas
- TO = Tempo Ocioso / Tempo Logado
- Custo unitário = Custo Total / Operações

### **Tipo 4: SOMA (nunca usar média)**
- Chamadas Atendidas
- Qnt. Negócios totais
- R$ Rentabilizações
- Custo PRV mensal
- Compensation Total
- Gastos Férias
- Custo HE
- Custo / margem por HC
- Valor Taxi
- Tempo Logado (horas)
- Produtividade / HC

---

## ✅ **Solução: Estrutura de Dados Correta**

### **Opção 1: Adicionar Colunas de Numerador/Denominador**

Para cada KPI do tipo RAZÃO ou MÉDIA PONDERADA, adicionar colunas auxiliares:

```sql
-- Exemplo para % Conversão
ALTER TABLE fato_metricas_diarias ADD COLUMN Conversao_Numerador INT;  -- Negócios
ALTER TABLE fato_metricas_diarias ADD COLUMN Conversao_Denominador INT;  -- Chamadas

-- Exemplo para TMA
ALTER TABLE fato_metricas_diarias ADD COLUMN TMA_Tempo_Total_Seg INT;  -- Tempo total
ALTER TABLE fato_metricas_diarias ADD COLUMN TMA_Chamadas_Atendidas INT;  -- Qtd chamadas
```

### **Opção 2: Tabela de Metadados de KPIs**

Criar tabela que define como calcular cada KPI:

```sql
CREATE TABLE kpi_metadados (
    kpi_id VARCHAR(50) PRIMARY KEY,
    kpi_nome VARCHAR(100),
    tipo_agregacao VARCHAR(20),  -- 'MEDIA', 'RAZAO', 'MEDIA_PONDERADA', 'SOMA'
    coluna_valor VARCHAR(50),
    coluna_numerador VARCHAR(50),
    coluna_denominador VARCHAR(50),
    coluna_peso VARCHAR(50)
);

INSERT INTO kpi_metadados VALUES
('nps', 'NPS', 'MEDIA', 'NPS', NULL, NULL, NULL),
('conversao', 'Conversão %', 'RAZAO', 'Conversao_Pct', 'Conversao_Numerador', 'Conversao_Denominador', NULL),
('tma', 'TMA', 'MEDIA_PONDERADA', 'TMA_Seg', 'TMA_Tempo_Total_Seg', NULL, 'TMA_Chamadas_Atendidas'),
('chamadas_atendidas', 'Chamadas Atendidas', 'SOMA', 'Chamadas_Atendidas', NULL, NULL, NULL);
```

---

## 🔧 **Código Corrigido**

### **Função de Agregação Inteligente**

```python
def agregar_kpi_corretamente(df, kpi_info, granularidade):
    """
    Agrega KPI de acordo com seu tipo
    """
    
    tipo = kpi_info.get('tipo_agregacao', 'MEDIA')
    coluna = kpi_info['coluna']
    
    # Agrupar por período
    if granularidade == 'ME':
        df_agrupado = df.groupby(df['Data'].dt.to_period('M'))
    elif granularidade == 'W':
        df_agrupado = df.groupby(df['Data'].dt.to_period('W'))
    else:
        df_agrupado = df.groupby('Data')
    
    if tipo == 'MEDIA':
        # Média simples (NPS, Notas)
        resultado = df_agrupado[coluna].mean()
        
    elif tipo == 'RAZAO':
        # Soma numerador / Soma denominador
        numerador = kpi_info['coluna_numerador']
        denominador = kpi_info['coluna_denominador']
        
        soma_num = df_agrupado[numerador].sum()
        soma_den = df_agrupado[denominador].sum()
        
        resultado = (soma_num / soma_den * 100).fillna(0)
        
    elif tipo == 'MEDIA_PONDERADA':
        # Soma valor * peso / Soma peso
        numerador = kpi_info['coluna_numerador']  # Ex: Tempo total
        peso = kpi_info['coluna_peso']  # Ex: Chamadas
        
        soma_num = df_agrupado[numerador].sum()
        soma_peso = df_agrupado[peso].sum()
        
        resultado = (soma_num / soma_peso).fillna(0)
        
    elif tipo == 'SOMA':
        # Soma simples (Chamadas, Custos)
        resultado = df_agrupado[coluna].sum()
    
    return resultado.reset_index()
```

### **Atualizar Dicionário de KPIs**

```python
KPIS_RESUMO = {
    'nps': {
        'nome': 'NPS',
        'coluna': 'NPS',
        'tipo_agregacao': 'MEDIA',
        'meta': 70,
        'cor': VIVO_COLORS['neon_purple']
    },
    'ocupacao': {
        'nome': 'Ocupação %',
        'coluna': 'Ocupacao_Pct',
        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Tempo_Ocupado_Hrs',
        'coluna_denominador': 'Tempo_Logado_Hrs',
        'meta': 85,
        'cor': VIVO_COLORS['neon_pink']
    },
    'conversao': {
        'nome': 'Conversão %',
        'coluna': 'Conversao_Pct',
        'tipo_agregacao': 'RAZAO',
        'coluna_numerador': 'Qnt_Negocios_Totais',
        'coluna_denominador': 'Chamadas_Atendidas',
        'meta': 15,
        'cor': VIVO_COLORS['neon_pink']
    },
    'tma': {
        'nome': 'TMA (seg)',
        'coluna': 'TMA_Seg',
        'tipo_agregacao': 'MEDIA_PONDERADA',
        'coluna_numerador': 'TMA_Tempo_Total_Seg',
        'coluna_peso': 'Chamadas_Atendidas',
        'meta': 300,
        'inverter': True,
        'cor': VIVO_COLORS['neon_gold']
    },
    'chamadas_atendidas': {
        'nome': 'Chamadas Atendidas',
        'coluna': 'Chamadas_Atendidas',
        'tipo_agregacao': 'SOMA',
        'meta': None,
        'cor': VIVO_COLORS['neon_cyan']
    }
}
```

### **Atualizar Funções de Gráfico e Pivot**

```python
def criar_grafico_evolutivo(df, kpi_info, granularidade='ME'):
    """Cria gráfico com agregação correta"""
    
    if len(df) == 0:
        return go.Figure()
    
    # Usar função de agregação inteligente
    df_agrupado = agregar_kpi_corretamente(df, kpi_info, granularidade)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_agrupado['Data'],
        y=df_agrupado[kpi_info['coluna']],
        mode='lines+markers',
        name=kpi_info['nome'],
        line=dict(color=kpi_info['cor'], width=3),
        marker=dict(size=8, color=kpi_info['cor'])
    ))
    
    # ... resto do código
    
    return fig


def criar_pivot_otimizado(df, kpi_info, dimensao, granularidade='ME', max_periodos=30):
    """Cria pivot com agregação correta"""
    
    if len(df) == 0:
        return pd.DataFrame()
    
    tipo = kpi_info.get('tipo_agregacao', 'MEDIA')
    coluna = kpi_info['coluna']
    
    # Determinar coluna de período
    if granularidade == 'ME':
        periodo_col = 'Periodo_M'
    elif granularidade == 'W':
        periodo_col = 'Periodo_W'
    else:
        periodo_col = 'Periodo_D'
    
    periodos_unicos = sorted(df[periodo_col].unique())[-max_periodos:]
    df_para_pivot = df[df[periodo_col].isin(periodos_unicos)].copy()
    
    if tipo == 'MEDIA':
        pivot = df_para_pivot.pivot_table(
            index=dimensao,
            columns=periodo_col,
            values=coluna,
            aggfunc='mean'
        )
        
    elif tipo == 'RAZAO':
        # Calcular numerador e denominador separadamente
        numerador = kpi_info['coluna_numerador']
        denominador = kpi_info['coluna_denominador']
        
        pivot_num = df_para_pivot.pivot_table(
            index=dimensao,
            columns=periodo_col,
            values=numerador,
            aggfunc='sum'
        )
        
        pivot_den = df_para_pivot.pivot_table(
            index=dimensao,
            columns=periodo_col,
            values=denominador,
            aggfunc='sum'
        )
        
        pivot = (pivot_num / pivot_den * 100).fillna(0)
        
    elif tipo == 'MEDIA_PONDERADA':
        numerador = kpi_info['coluna_numerador']
        peso = kpi_info['coluna_peso']
        
        pivot_num = df_para_pivot.pivot_table(
            index=dimensao,
            columns=periodo_col,
            values=numerador,
            aggfunc='sum'
        )
        
        pivot_peso = df_para_pivot.pivot_table(
            index=dimensao,
            columns=periodo_col,
            values=peso,
            aggfunc='sum'
        )
        
        pivot = (pivot_num / pivot_peso).fillna(0)
        
    elif tipo == 'SOMA':
        pivot = df_para_pivot.pivot_table(
            index=dimensao,
            columns=periodo_col,
            values=coluna,
            aggfunc='sum'
        )
    
    return pivot.round(2)
```

---

## 📊 **Colunas Necessárias no Banco**

Para implementar a correção, adicione estas colunas ao `fato_metricas_diarias`:

```sql
-- Numeradores e Denominadores para KPIs de RAZÃO

-- Conversão
ALTER TABLE fato_metricas_diarias ADD COLUMN Conversao_Numerador INT;  -- Negócios
ALTER TABLE fato_metricas_diarias ADD COLUMN Conversao_Denominador INT;  -- Chamadas

-- Ocupação
ALTER TABLE fato_metricas_diarias ADD COLUMN Tempo_Ocupado_Hrs DECIMAL(8,2);
-- Tempo_Logado_Hrs já existe

-- Abandono
ALTER TABLE fato_metricas_diarias ADD COLUMN Chamadas_Abandonadas INT;
ALTER TABLE fato_metricas_diarias ADD COLUMN Chamadas_Oferecidas INT;

-- TMA
ALTER TABLE fato_metricas_diarias ADD COLUMN TMA_Tempo_Total_Seg INT;
-- Chamadas_Atendidas já existe

-- Absenteísmo
ALTER TABLE fato_metricas_diarias ADD COLUMN Dias_Ausentes DECIMAL(5,2);
ALTER TABLE fato_metricas_diarias ADD COLUMN Dias_Uteis DECIMAL(5,2);

-- ... adicionar para todos os outros KPIs de RAZÃO
```

---

## 🎯 **Próximos Passos**

### **Fase 1: Análise**
- [ ] Identificar quais KPIs você tem numerador/denominador disponíveis
- [ ] Classificar cada KPI (MEDIA, RAZAO, MEDIA_PONDERADA, SOMA)
- [ ] Mapear colunas necessárias

### **Fase 2: Estrutura de Dados**
- [ ] Adicionar colunas de numerador/denominador no banco
- [ ] Criar tabela `kpi_metadados`
- [ ] Popular dados históricos

### **Fase 3: Código**
- [ ] Implementar função `agregar_kpi_corretamente()`
- [ ] Atualizar dicionários de KPIs
- [ ] Atualizar `criar_grafico_evolutivo()`
- [ ] Atualizar `criar_pivot_otimizado()`

### **Fase 4: Testes**
- [ ] Testar cada tipo de agregação
- [ ] Validar resultados com dados reais
- [ ] Comparar com cálculos manuais

---

## 📝 **Exemplo Prático**

### **Antes (ERRADO):**

```
Dia 1: 100 chamadas, 10 negócios = 10%
Dia 2: 50 chamadas, 20 negócios = 40%

Conversão Semanal (média simples) = (10% + 40%) / 2 = 25%  ❌
```

### **Depois (CORRETO):**

```
Dia 1: 100 chamadas, 10 negócios
Dia 2: 50 chamadas, 20 negócios

Conversão Semanal = (10 + 20) / (100 + 50) = 30 / 150 = 20%  ✅
```

---

## 🤝 **Suporte**

Para implementar esta correção:
1. Consultar este documento
2. Verificar estrutura de dados disponível
3. Adaptar código conforme necessidade
4. Testar extensivamente

---

**Dashboard KPIs Insourcing - Vivo Fibra**  
**Versão 1.0.0 • Dezembro 2024**  
**⚠️ Correção Crítica de Cálculo de Granularidade**
