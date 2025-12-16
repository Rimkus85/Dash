# GUIA DE CONFIGURAÇÃO - POWER AUTOMATE

Este guia explica como configurar os fluxos de automação para o Dashboard de KPIs - Insourcing.

## 📋 VISÃO GERAL DOS FLUXOS

Foram criados 3 fluxos de automação:

1. **Alertas no Teams** - Monitora KPIs críticos e envia alertas em tempo real
2. **Resumo Semanal por E-mail** - Envia relatório executivo toda segunda-feira
3. **Alertas no WhatsApp** - Notificações críticas via WhatsApp Business API

---

## 🔧 PASSO 1: PUBLICAR O DASHBOARD NO POWER BI SERVICE

Antes de configurar os fluxos, você precisa publicar o dashboard:

1. Abra o arquivo `.pbix` no Power BI Desktop
2. Clique em **"Publicar"** na faixa de opções
3. Selecione o workspace de destino
4. Anote os IDs necessários:
   - **Workspace ID**: Vá em Configurações do Workspace > URL (último segmento)
   - **Report ID**: Abra o relatório > URL (segmento após `/reports/`)
   - **Dataset ID**: Configurações do Dataset > URL

**Exemplo de URL:**
```
https://app.powerbi.com/groups/12345678-abcd-1234-abcd-123456789abc/reports/87654321-dcba-4321-dcba-987654321cba
                                    └─────── Workspace ID ───────┘         └─────── Report ID ───────┘
```

---

## 🚀 PASSO 2: IMPORTAR FLUXOS NO POWER AUTOMATE

### 2.1. Acessar Power Automate

1. Acesse [https://make.powerautomate.com](https://make.powerautomate.com)
2. Faça login com sua conta Microsoft 365
3. Selecione o ambiente correto (Production ou seu ambiente corporativo)

### 2.2. Criar Novo Fluxo

Para cada arquivo JSON fornecido:

1. Clique em **"Meus fluxos"** > **"+ Novo fluxo"** > **"Fluxo de nuvem automatizado"** (para alertas) ou **"Fluxo de nuvem agendado"** (para resumo)
2. Dê um nome ao fluxo
3. Configure o gatilho conforme descrito em cada seção abaixo

---

## 📢 FLUXO 1: ALERTAS NO TEAMS

### Objetivo
Monitorar KPIs críticos a cada hora (horário comercial) e enviar alertas no Teams quando limites são ultrapassados.

### Configuração Passo a Passo

#### 1. Criar o Fluxo

- **Nome:** Dashboard Insourcing - Alertas Teams
- **Tipo:** Fluxo de nuvem agendado
- **Recorrência:** A cada 1 hora, de segunda a sexta, das 8h às 18h

#### 2. Adicionar Ação: Obter Dados do Power BI

1. Clique em **"+ Nova etapa"**
2. Procure por **"Power BI"**
3. Selecione **"Executar uma consulta em um conjunto de dados"**
4. Configure:
   - **Workspace:** Selecione seu workspace
   - **Dataset:** Dashboard_KPIs_Insourcing
   - **Tabela:** fato_metricas_diarias
   - **Consulta DAX:**
   ```dax
   EVALUATE
   FILTER(
       ADDCOLUMNS(
           SUMMARIZE(
               fato_metricas_diarias,
               fato_metricas_diarias[Data],
               fato_metricas_diarias[Gerente]
           ),
           "Ocupacao", AVERAGE(fato_metricas_diarias[Ocupacao_Pct]),
           "Absenteismo", AVERAGE(fato_metricas_diarias[Absenteismo_Pct]),
           "Falha_Op", AVERAGE(fato_metricas_diarias[Falha_Operacional_Pct]),
           "Rechamadas", AVERAGE(fato_metricas_diarias[Rechamadas_7d_Pct])
       ),
       fato_metricas_diarias[Data] = TODAY()
   )
   ```

#### 3. Adicionar Condição: Verificar Alertas

1. Adicione uma **"Condição"**
2. Configure a expressão:
   ```
   @or(
       greater(outputs('Obter_Dados_Power_BI')?['body/value'][0]?['Ocupacao'], 97),
       greater(outputs('Obter_Dados_Power_BI')?['body/value'][0]?['Absenteismo'], 10),
       greater(outputs('Obter_Dados_Power_BI')?['body/value'][0]?['Falha_Op'], 4)
   )
   ```

#### 4. Se Sim: Postar no Teams

1. No ramo **"Se sim"**, adicione **"Postar mensagem em um chat ou canal"** (Microsoft Teams)
2. Configure:
   - **Postar como:** Flow bot
   - **Postar em:** Canal
   - **Team:** Selecione seu time
   - **Canal:** Selecione o canal (ex: "Operações" ou "Alertas")
   - **Mensagem:** Use Adaptive Card (veja template abaixo)

**Template de Adaptive Card:**
```json
{
    "type": "AdaptiveCard",
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.4",
    "body": [
        {
            "type": "Container",
            "style": "attention",
            "items": [
                {
                    "type": "TextBlock",
                    "text": "⚠️ ALERTA CRÍTICO - Dashboard Insourcing",
                    "weight": "Bolder",
                    "size": "Large",
                    "color": "Attention"
                }
            ]
        },
        {
            "type": "FactSet",
            "facts": [
                {
                    "title": "Ocupação:",
                    "value": "@{outputs('Obter_Dados_Power_BI')?['body/value'][0]?['Ocupacao']}%"
                },
                {
                    "title": "Absenteísmo:",
                    "value": "@{outputs('Obter_Dados_Power_BI')?['body/value'][0]?['Absenteismo']}%"
                },
                {
                    "title": "Gerente:",
                    "value": "@{outputs('Obter_Dados_Power_BI')?['body/value'][0]?['Gerente']}"
                }
            ]
        },
        {
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.OpenUrl",
                    "title": "Abrir Dashboard",
                    "url": "https://app.powerbi.com/groups/SEU_WORKSPACE/reports/SEU_REPORT_ID"
                }
            ]
        }
    ]
}
```

#### 5. Testar o Fluxo

1. Clique em **"Testar"** > **"Manualmente"**
2. Clique em **"Executar fluxo"**
3. Verifique se a mensagem aparece no Teams

---

## 📧 FLUXO 2: RESUMO SEMANAL POR E-MAIL

### Objetivo
Enviar relatório executivo toda segunda-feira às 8h com snapshot do dashboard e principais KPIs.

### Configuração Passo a Passo

#### 1. Criar o Fluxo

- **Nome:** Dashboard Insourcing - Resumo Semanal Email
- **Tipo:** Fluxo de nuvem agendado
- **Recorrência:** Semanal, toda segunda-feira às 8h

#### 2. Adicionar Ação: Exportar Relatório do Power BI

1. Adicione **"Exportar para arquivo para relatórios do Power BI"**
2. Configure:
   - **Workspace:** Selecione seu workspace
   - **Relatório:** Dashboard_KPIs_Insourcing
   - **Formato de exportação:** PNG
   - **Páginas:** Resumo Executivo

#### 3. Adicionar Ação: Obter Dados para Resumo

1. Adicione **"Executar uma consulta em um conjunto de dados"** (Power BI)
2. Configure consulta DAX para obter médias da semana:
   ```dax
   EVALUATE
   SUMMARIZE(
       FILTER(
           fato_metricas_diarias,
           fato_metricas_diarias[Data] >= TODAY() - 7 &&
           fato_metricas_diarias[Data] <= TODAY()
       ),
       "NPS_Medio", AVERAGE(fato_metricas_diarias[NPS]),
       "Ocupacao_Media", AVERAGE(fato_metricas_diarias[Ocupacao_Pct]),
       "Conversao_Media", AVERAGE(fato_metricas_diarias[Conversao_Pct]),
       "Margem_Media", AVERAGE(fato_metricas_diarias[Margem_Operacional_Pct]),
       "Receita_Total", SUM(fato_metricas_diarias[Receita_Total])
   )
   ```

#### 4. Adicionar Ação: Enviar E-mail

1. Adicione **"Enviar um email (V2)"** (Office 365 Outlook)
2. Configure:
   - **Para:** diretoria@empresa.com.br; gerentes@empresa.com.br
   - **Assunto:** 📊 Resumo Semanal - Dashboard Insourcing (Semana @{formatDateTime(utcNow(), 'W')})
   - **Corpo:** HTML (veja template abaixo)
   - **Anexos:** Adicione o arquivo PNG exportado

**Template HTML Simplificado:**
```html
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background-color: #1e3a5f; color: white; padding: 20px; text-align: center; }
        .kpi { display: inline-block; margin: 10px; padding: 15px; border: 1px solid #ddd; }
        .value { font-size: 28px; font-weight: bold; color: #0078d4; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Resumo Semanal - Dashboard Insourcing</h1>
    </div>
    <div style="margin: 20px;">
        <h2>Principais Indicadores</h2>
        <div class="kpi">
            <div class="value">@{outputs('Obter_Dados')?['body/value'][0]?['NPS_Medio']}</div>
            <div>NPS</div>
        </div>
        <div class="kpi">
            <div class="value">@{outputs('Obter_Dados')?['body/value'][0]?['Ocupacao_Media']}%</div>
            <div>Ocupação</div>
        </div>
        <div class="kpi">
            <div class="value">@{outputs('Obter_Dados')?['body/value'][0]?['Conversao_Media']}%</div>
            <div>Conversão</div>
        </div>
    </div>
    <div style="margin: 20px;">
        <img src="cid:dashboard_snapshot.png" style="max-width: 100%;">
    </div>
    <div style="margin: 20px;">
        <a href="https://app.powerbi.com/groups/SEU_WORKSPACE/reports/SEU_REPORT_ID" 
           style="background-color:#0078d4; color:white; padding:10px 20px; text-decoration:none;">
           Acessar Dashboard Completo
        </a>
    </div>
</body>
</html>
```

---

## 💬 FLUXO 3: ALERTAS NO WHATSAPP

### Objetivo
Enviar notificações críticas via WhatsApp quando alertas são disparados no Power BI.

### ⚠️ IMPORTANTE: Requisitos

Este fluxo requer:
- **WhatsApp Business API** (pago, requer aprovação da Meta)
- Ou **alternativa gratuita:** Telegram Bot (recomendado)

### Opção A: WhatsApp Business API (Complexo)

#### Pré-requisitos
1. Conta WhatsApp Business verificada
2. Acesso à Meta Business Suite
3. Phone Number ID e Access Token

#### Passos
1. Acesse [Meta for Developers](https://developers.facebook.com/)
2. Crie um app e configure WhatsApp Business API
3. Obtenha credenciais (Phone Number ID e Token)
4. No Power Automate, use ação **HTTP** com:
   - **Método:** POST
   - **URI:** https://graph.facebook.com/v18.0/SEU_PHONE_NUMBER_ID/messages
   - **Cabeçalhos:** Authorization: Bearer SEU_TOKEN
   - **Corpo:** (veja arquivo JSON)

### Opção B: Telegram Bot (Recomendado - Gratuito)

#### Pré-requisitos
1. Conta no Telegram
2. Criar um bot via @BotFather

#### Passos

1. **Criar o Bot:**
   - Abra o Telegram e procure por **@BotFather**
   - Envie `/newbot`
   - Escolha um nome e username
   - Copie o **token** fornecido

2. **Obter Chat ID:**
   - Envie uma mensagem para seu bot
   - Acesse: `https://api.telegram.org/botSEU_TOKEN/getUpdates`
   - Copie o **chat_id** do resultado

3. **Configurar no Power Automate:**
   - Adicione ação **HTTP**
   - Configure:
     - **Método:** POST
     - **URI:** `https://api.telegram.org/botSEU_TOKEN/sendMessage`
     - **Cabeçalhos:** Content-Type: application/json
     - **Corpo:**
     ```json
     {
         "chat_id": "SEU_CHAT_ID",
         "text": "🚨 *ALERTA CRÍTICO*\n\n📊 KPI: Ocupação\n📈 Valor: 98%\n⚠️ Limite: 97%",
         "parse_mode": "Markdown"
     }
     ```

4. **Criar Grupo no Telegram (Opcional):**
   - Crie um grupo com os gerentes
   - Adicione o bot ao grupo
   - Obtenha o chat_id do grupo (será negativo)
   - Use esse chat_id para enviar para todos

---

## 🔐 SEGURANÇA E BOAS PRÁTICAS

### Proteção de Credenciais

1. **Nunca exponha tokens diretamente no fluxo**
2. Use **Azure Key Vault** para armazenar:
   - WhatsApp Access Token
   - Telegram Bot Token
   - Credenciais de banco de dados

#### Como usar Key Vault no Power Automate:

1. Adicione ação **"Obter segredo"** (Azure Key Vault)
2. Configure:
   - **Nome do cofre:** seu-keyvault
   - **Nome do segredo:** telegram-bot-token
3. Use `@{outputs('Obter_segredo')?['value']}` nas ações seguintes

### Limitações e Quotas

- **Power BI:** 48 atualizações por dia (plano Pro)
- **Power Automate:** 40.000 ações/mês (plano gratuito)
- **Teams:** Sem limite de mensagens
- **WhatsApp API:** Cobrado por mensagem
- **Telegram:** 30 mensagens/segundo (gratuito)

---

## 📊 MONITORAMENTO E AUDITORIA

### Verificar Histórico de Execuções

1. Acesse Power Automate
2. Clique no fluxo
3. Vá em **"Histórico de execuções de 28 dias"**
4. Analise sucessos e falhas

### Criar Relatório de Auditoria

Adicione ao final de cada fluxo:

```
Ação: Criar item (SharePoint)
Lista: Historico_Automacoes
Campos:
  - Titulo: Nome do Fluxo
  - Data_Execucao: @{utcNow()}
  - Status: @{if(equals(outputs('Acao_Principal')?['statusCode'], 200), 'Sucesso', 'Falha')}
  - Detalhes: @{outputs('Acao_Principal')}
```

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Erro: "Não foi possível conectar ao Power BI"
- Verifique se o dataset está publicado
- Confirme permissões no workspace
- Reautentique a conexão do Power BI

### Erro: "Falha ao enviar mensagem no Teams"
- Verifique se o bot tem permissão no canal
- Confirme que o Team ID e Channel ID estão corretos
- Teste com um canal público primeiro

### Erro: "Telegram não recebe mensagens"
- Verifique se o token está correto
- Confirme que você enviou pelo menos 1 mensagem para o bot
- Teste a URL do getUpdates no navegador

### Fluxo não executa no horário
- Verifique o fuso horário configurado
- Confirme que o fluxo está **ativado**
- Verifique se há erros no histórico

---

## 📚 RECURSOS ADICIONAIS

- [Documentação Power Automate](https://learn.microsoft.com/pt-br/power-automate/)
- [Power BI REST API](https://learn.microsoft.com/pt-br/rest/api/power-bi/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Adaptive Cards Designer](https://adaptivecards.io/designer/)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)

---

## ✅ CHECKLIST DE CONFIGURAÇÃO

Antes de ativar os fluxos, verifique:

- [ ] Dashboard publicado no Power BI Service
- [ ] Workspace ID e Report ID anotados
- [ ] Conexões do Power BI autenticadas no Power Automate
- [ ] Canal do Teams criado e configurado
- [ ] E-mails dos destinatários atualizados
- [ ] Bot do Telegram criado (se usar essa opção)
- [ ] Tokens armazenados de forma segura
- [ ] Fluxos testados manualmente
- [ ] Histórico de execuções monitorado
- [ ] Documentação compartilhada com a equipe

---

**Dúvidas?** Consulte a documentação oficial ou entre em contato com o administrador do Power Platform da sua organização.
