# 🔧 Como Implementar Filtros Adaptativos (Em Cascata)

**Objetivo:** Fazer com que os filtros se adaptem conforme a seleção do usuário.

**Exemplo:** Ao selecionar "Grupo: Platinum Especialista Fat", o filtro de Cidade deve mostrar apenas as cidades desse grupo, e o filtro de Gerente deve mostrar apenas os gerentes disponíveis nessas cidades.

---

## ⚠️ Por Que Não Está Implementado Agora?

Os filtros adaptativos causam **dependência circular** entre callbacks no Dash, o que pode travar o carregamento do dashboard. Para implementar corretamente, é necessário:

1. Testar com dados reais
2. Ajustar a lógica de callbacks
3. Possivelmente usar `State` ao invés de `Input` em alguns casos
4. Adicionar `prevent_initial_call` onde necessário

---

## 📋 **Implementação Recomendada**

### **Opção 1: Callbacks Separados (Mais Seguro)**

Criar 3 callbacks separados, um para cada filtro:

```python
# Callback 1: Atualizar opções de Grupo
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

# Callback 2: Atualizar opções de Cidade (filtrado por Grupo)
@app.callback(
    Output('filtro-cidade', 'options'),
    [Input('filtro-periodo', 'start_date'),
     Input('filtro-periodo', 'end_date'),
     Input('filtro-operacao', 'value'),
     Input('filtro-grupo', 'value')]  # ← Depende de Grupo
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

# Callback 3: Atualizar opções de Gerente (filtrado por Grupo e Cidade)
@app.callback(
    Output('filtro-gerente', 'options'),
    [Input('filtro-periodo', 'start_date'),
     Input('filtro-periodo', 'end_date'),
     Input('filtro-operacao', 'value'),
     Input('filtro-grupo', 'value'),      # ← Depende de Grupo
     Input('filtro-cidade', 'value')]     # ← Depende de Cidade
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
```

---

## 🔧 **Onde Adicionar no Código**

### **Localização:**
Adicionar **ANTES** do callback principal `atualizar_conteudo`, na seção de CALLBACKS.

### **Substituir:**
Remover o callback atual `atualizar_opcoes_filtros` e substituir pelos 3 callbacks acima.

### **Linha aproximada:** 822-843

---

## ⚠️ **Problemas Potenciais e Soluções**

### **Problema 1: Travamento no Carregamento**

**Causa:** Dependência circular entre callbacks.

**Solução:**
```python
# Adicionar prevent_initial_call onde necessário
@app.callback(
    Output('filtro-cidade', 'options'),
    [Input('filtro-grupo', 'value')],
    prevent_initial_call=True  # ← Adicionar isto
)
```

### **Problema 2: Filtro Resetando Automaticamente**

**Causa:** Quando as opções mudam, o valor selecionado pode não estar mais disponível.

**Solução:**
```python
# Adicionar callback para resetar valor quando opções mudam
@app.callback(
    Output('filtro-cidade', 'value'),
    [Input('filtro-cidade', 'options')]
)
def resetar_cidade(opcoes):
    # Se as opções mudaram, resetar para "Todas"
    return 'Todas'
```

### **Problema 3: Performance Lenta**

**Causa:** Callbacks sendo acionados múltiplas vezes.

**Solução:**
```python
# Usar @lru_cache para cachear resultados
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cidades_por_grupo(grupo):
    df = carregar_dados_global()
    if grupo != 'Todos':
        df = df[df['Grupo'] == grupo]
    return sorted(df['Cidade'].unique().tolist())
```

---

## 📝 **Passo a Passo para Implementar**

### **1. Fazer Backup**
```bash
cp dashboard_app_final.py dashboard_app_final_backup.py
```

### **2. Localizar Callback Atual**
Procurar por:
```python
def atualizar_opcoes_filtros(start_date, end_date):
```

### **3. Substituir pelo Código Acima**
Copiar os 3 callbacks separados.

### **4. Testar**
```bash
python3 dashboard_app_final.py
```

### **5. Verificar no Navegador**
- Selecionar um Grupo
- Verificar se Cidade mostra apenas cidades daquele grupo
- Selecionar uma Cidade
- Verificar se Gerente mostra apenas gerentes daquela cidade

---

## ✅ **Comportamento Esperado**

### **Exemplo Prático:**

**Situação Inicial:**
- Grupo: Todos
- Cidade: Todas (mostra todas as cidades)
- Gerente: Todos (mostra todos os gerentes)

**Após selecionar "Grupo: Platinum Especialista Fat":**
- Grupo: Platinum Especialista Fat
- Cidade: Apenas cidades desse grupo (ex: São Paulo, Rio de Janeiro)
- Gerente: Apenas gerentes desse grupo

**Após selecionar "Cidade: São Paulo":**
- Grupo: Platinum Especialista Fat
- Cidade: São Paulo
- Gerente: Apenas gerentes de São Paulo (ex: Felipe, Maria)

---

## 🐛 **Troubleshooting**

### **Dashboard não carrega após implementar**

1. Verificar log de erros:
```bash
tail -50 dashboard.log
```

2. Comentar os novos callbacks e testar um por um:
```python
# Comentar callback 2 e 3
# Testar apenas callback 1
# Se funcionar, descomentar callback 2
# Testar
# Se funcionar, descomentar callback 3
```

3. Adicionar try/except para debug:
```python
def atualizar_opcoes_cidade(start_date, end_date, operacao, grupo):
    try:
        # código aqui
    except Exception as e:
        print(f"Erro em atualizar_opcoes_cidade: {e}")
        return [{'label': 'Todas', 'value': 'Todas'}]
```

---

## 📚 **Referências**

- [Dash Callbacks Documentation](https://dash.plotly.com/basic-callbacks)
- [Dash Advanced Callbacks](https://dash.plotly.com/advanced-callbacks)
- [Dash Pattern-Matching Callbacks](https://dash.plotly.com/pattern-matching-callbacks)

---

## 💡 **Alternativa Simples (Se Tiver Problemas)**

Se os filtros adaptativos causarem muitos problemas, uma alternativa é:

### **Mostrar Aviso ao Usuário:**

Adicionar um texto de ajuda abaixo dos filtros:

```python
html.Div([
    html.I(className="fas fa-info-circle", style={'marginRight': '5px'}),
    html.Span("Dica: Selecione os filtros na ordem: Grupo → Cidade → Gerente para melhores resultados", 
              style={'fontSize': '0.8rem', 'color': VIVO_COLORS['gray_medium']})
], style={'marginTop': '10px', 'marginBottom': '20px'})
```

Dessa forma, o usuário sabe que deve selecionar na ordem correta, mesmo que os filtros não sejam adaptativos.

---

## ✅ **Conclusão**

Os filtros adaptativos são uma melhoria importante de UX, mas requerem cuidado na implementação para evitar problemas de performance e loops infinitos.

**Recomendação:** Implementar após ter dados reais e poder testar adequadamente.

---

**Última atualização:** 12/12/2024  
**Versão do Dashboard:** 2.0 Final
