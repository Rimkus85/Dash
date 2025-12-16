# 🤖 Automações Power Automate Incluídas
## Dashboard KPIs Insourcing - Vivo Fibra

---

## ✅ O Que Está Incluído

O pacote completo inclui **3 fluxos de automação** prontos para importar no Power Automate:

### 📁 Pasta: `power_automate/`

| Arquivo | Descrição | Frequência |
|---------|-----------|------------|
| `power_automate_alertas_teams.json` | Alertas no Microsoft Teams | A cada hora (8h-18h) |
| `power_automate_resumo_email.json` | Resumo semanal por e-mail | Segundas às 8h |
| `power_automate_alertas_whatsapp.json` | Alertas no WhatsApp | Tempo real |

---

## 📋 Documentação

### Guia Completo de Configuração

**Arquivo:** `GUIA_POWER_AUTOMATE.md`

Este guia contém:
- ✅ Passo a passo para importar os fluxos
- ✅ Configuração de conexões
- ✅ Personalização de alertas
- ✅ Testes e validação
- ✅ Solução de problemas

---

## 🔔 Automação 1: Alertas no Teams

**Arquivo:** `power_automate_alertas_teams.json`

### Funcionalidade
- Monitora KPIs críticos a cada hora
- Envia alertas quando metas não são atingidas
- Usa Adaptive Cards com visual Vivo
- Inclui link direto para o dashboard

### Configuração Necessária
1. Importar o arquivo JSON no Power Automate
2. Configurar conexão com o dashboard (HTTP)
3. Configurar conexão com Microsoft Teams
4. Definir canal do Teams para alertas
5. Personalizar limites de alerta (opcional)

### KPIs Monitorados
- NPS
- Ocupação %
- Absenteísmo %
- TMA
- Conversão %
- SLA %

---

## 📧 Automação 2: Resumo Semanal por E-mail

**Arquivo:** `power_automate_resumo_email.json`

### Funcionalidade
- Gera relatório executivo toda segunda-feira às 8h
- Inclui snapshot dos principais KPIs
- Comparativo com semana anterior
- Destaques positivos e negativos
- Link para dashboard completo

### Configuração Necessária
1. Importar o arquivo JSON no Power Automate
2. Configurar conexão com o dashboard (HTTP)
3. Configurar conexão com Outlook/Office 365
4. Definir lista de destinatários
5. Personalizar template de e-mail (opcional)

### Destinatários Sugeridos
- Diretoria
- Gerentes
- Coordenadores
- Analistas de BI

---

## 📱 Automação 3: Alertas no WhatsApp

**Arquivo:** `power_automate_alertas_whatsapp.json`

### Funcionalidade
- Notificações críticas em tempo real
- Disparado por alertas do dashboard
- Usa WhatsApp Business API ou Telegram
- Mensagens curtas e diretas

### Configuração Necessária
1. Importar o arquivo JSON no Power Automate
2. Configurar conexão com o dashboard (HTTP)
3. **Opção A:** Configurar WhatsApp Business API (pago)
4. **Opção B:** Configurar Telegram Bot (gratuito)
5. Definir números/grupos de destino
6. Personalizar mensagens (opcional)

### Opções de Integração

#### Opção A: WhatsApp Business API (Recomendado)
- **Custo:** Pago (varia por mensagem)
- **Vantagens:** Oficial, confiável, suporte
- **Fornecedores:** Twilio, MessageBird, Infobip
- **Setup:** Requer aprovação do Facebook

#### Opção B: Telegram Bot (Alternativa Gratuita)
- **Custo:** Gratuito
- **Vantagens:** Fácil setup, API simples
- **Limitações:** Requer Telegram instalado
- **Setup:** Criar bot via @BotFather

---

## 🚀 Como Importar os Fluxos

### Passo 1: Acessar Power Automate

1. Acesse: https://make.powerautomate.com
2. Faça login com sua conta Microsoft 365
3. Selecione seu ambiente

### Passo 2: Importar Fluxo

1. Clique em **"Meus fluxos"**
2. Clique em **"Importar"** → **"Importar Pacote (Legado)"**
3. Selecione o arquivo JSON (ex: `power_automate_alertas_teams.json`)
4. Clique em **"Carregar"**

### Passo 3: Configurar Conexões

1. Para cada conexão necessária, clique em **"Selecionar durante a importação"**
2. Escolha uma conexão existente ou crie nova
3. Conexões típicas:
   - **HTTP** (para acessar o dashboard)
   - **Microsoft Teams** (para alertas no Teams)
   - **Office 365 Outlook** (para e-mails)
   - **WhatsApp/Telegram** (para mensagens)

### Passo 4: Importar e Ativar

1. Clique em **"Importar"**
2. Aguarde conclusão da importação
3. Abra o fluxo importado
4. Clique em **"Ativar"** (canto superior direito)

### Passo 5: Testar

1. Clique em **"Testar"** → **"Manualmente"**
2. Clique em **"Executar fluxo"**
3. Verifique se o alerta foi enviado corretamente
4. Ajuste configurações se necessário

---

## ⚙️ Configurações Importantes

### URL do Dashboard

Todos os fluxos precisam da URL do dashboard:

```
http://seu-servidor:8050
```

**Onde configurar:**
- Na ação **"HTTP - GET"** de cada fluxo
- Substituir `http://localhost:8050` pela URL real

### Frequência de Execução

#### Alertas no Teams
- **Padrão:** A cada hora (8h-18h, dias úteis)
- **Personalizar:** Editar gatilho "Recorrência"
- **Sugestão:** Ajustar horário conforme necessidade

#### Resumo Semanal
- **Padrão:** Segundas-feiras às 8h
- **Personalizar:** Editar gatilho "Recorrência"
- **Sugestão:** Pode ser diário, semanal ou mensal

#### Alertas WhatsApp
- **Padrão:** Tempo real (disparado por webhook)
- **Personalizar:** Configurar webhook no dashboard
- **Sugestão:** Apenas para alertas críticos

### Limites de Alerta

Editar no fluxo, seção **"Condição"**:

```javascript
// Exemplo: NPS abaixo de 70
@less(body('HTTP_-_GET_Dashboard')?['nps'], 70)

// Exemplo: Absenteísmo acima de 5%
@greater(body('HTTP_-_GET_Dashboard')?['absenteismo'], 5)
```

---

## 📊 Integração com o Dashboard

### Endpoint de Dados

Os fluxos acessam o dashboard via HTTP para obter dados:

```
GET http://seu-servidor:8050/api/dados
```

**Nota:** O dashboard atual não tem API REST implementada. Para usar as automações, você precisará:

**Opção 1:** Criar endpoint API no dashboard
**Opção 2:** Conectar diretamente ao banco de dados
**Opção 3:** Usar Power BI como fonte de dados

### Exemplo de Endpoint API (Futuro)

```python
# Adicionar ao dashboard_app_final.py

@app.server.route('/api/dados')
def api_dados():
    df = carregar_dados_banco()
    dados = {
        'nps': df['NPS'].mean(),
        'ocupacao': df['Ocupacao_Pct'].mean(),
        'absenteismo': df['Absenteismo_Pct'].mean(),
        'tma': df['TMA_Seg'].mean(),
        'conversao': df['Conversao_Pct'].mean(),
        'sla': df['SLA_Atendimento_Pct'].mean()
    }
    return jsonify(dados)
```

---

## 🔐 Segurança

### Autenticação

Para proteger o endpoint do dashboard:

1. **Opção 1:** Autenticação básica HTTP
2. **Opção 2:** Token de API
3. **Opção 3:** OAuth 2.0

### Exemplo com Token

```python
# No dashboard
@app.server.route('/api/dados')
def api_dados():
    token = request.headers.get('Authorization')
    if token != 'Bearer SEU_TOKEN_SECRETO':
        return jsonify({'error': 'Não autorizado'}), 401
    # ... resto do código
```

No Power Automate:
- Adicionar header: `Authorization: Bearer SEU_TOKEN_SECRETO`

---

## 📱 Exemplo de Mensagens

### Alerta no Teams

```
🚨 ALERTA DE KPI - Dashboard Insourcing

📊 NPS: 65.0 (Meta: 70.0)
⚠️ Status: Abaixo da meta

📈 Ocupação: 71.4% (Meta: 85%)
❌ Status: Crítico

🔗 Ver Dashboard Completo
```

### Resumo Semanal

```
📊 Resumo Semanal - Dashboard Insourcing
Semana: 01/12 a 07/12/2024

✅ Destaques Positivos:
• SLA: 91.9% (Meta: 90%)
• NPS: 65.0 (Estável)

⚠️ Pontos de Atenção:
• Ocupação: 71.4% (Meta: 85%)
• Absenteísmo: 7.5% (Meta: 5%)

🔗 Acessar Dashboard
```

### Alerta WhatsApp

```
🚨 ALERTA CRÍTICO

Ocupação: 71.4%
Meta: 85%
Status: Abaixo

Ver: http://dashboard.link
```

---

## 🐛 Solução de Problemas

### Erro: "Não foi possível conectar ao dashboard"

**Solução:**
1. Verificar se o dashboard está rodando
2. Verificar URL no fluxo
3. Verificar firewall/rede
4. Testar URL no navegador

### Erro: "Falha ao enviar mensagem no Teams"

**Solução:**
1. Verificar permissões no Teams
2. Verificar se o canal existe
3. Reconectar integração do Teams
4. Testar com outro canal

### Erro: "Fluxo não executa no horário"

**Solução:**
1. Verificar se o fluxo está ativado
2. Verificar fuso horário da recorrência
3. Verificar histórico de execuções
4. Verificar limites do plano Power Automate

---

## 📋 Checklist de Configuração

### Alertas no Teams
- [ ] Arquivo JSON importado
- [ ] Conexão HTTP configurada
- [ ] Conexão Teams configurada
- [ ] Canal do Teams definido
- [ ] URL do dashboard atualizada
- [ ] Limites de alerta personalizados
- [ ] Fluxo ativado
- [ ] Teste realizado com sucesso

### Resumo Semanal
- [ ] Arquivo JSON importado
- [ ] Conexão HTTP configurada
- [ ] Conexão Outlook configurada
- [ ] Lista de destinatários definida
- [ ] URL do dashboard atualizada
- [ ] Template de e-mail personalizado
- [ ] Fluxo ativado
- [ ] Teste realizado com sucesso

### Alertas WhatsApp
- [ ] Arquivo JSON importado
- [ ] Conexão HTTP configurada
- [ ] WhatsApp/Telegram configurado
- [ ] Números/grupos definidos
- [ ] URL do dashboard atualizada
- [ ] Mensagens personalizadas
- [ ] Fluxo ativado
- [ ] Teste realizado com sucesso

---

## 🎯 Próximos Passos

### Fase 1: Configuração Básica
1. ✅ Arquivos incluídos no pacote
2. [ ] Você: Importar fluxos no Power Automate
3. [ ] Você: Configurar conexões
4. [ ] Você: Testar cada fluxo

### Fase 2: Integração com Dashboard
1. [ ] Criar endpoint API no dashboard
2. [ ] Configurar autenticação
3. [ ] Atualizar URLs nos fluxos
4. [ ] Validar dados retornados

### Fase 3: Personalização
1. [ ] Ajustar frequência de alertas
2. [ ] Personalizar mensagens
3. [ ] Adicionar novos KPIs
4. [ ] Criar novos fluxos

---

## 📚 Documentação Adicional

| Arquivo | Descrição |
|---------|-----------|
| `GUIA_POWER_AUTOMATE.md` | Guia completo e detalhado |
| `power_automate/power_automate_alertas_teams.json` | Fluxo de alertas Teams |
| `power_automate/power_automate_resumo_email.json` | Fluxo de resumo semanal |
| `power_automate/power_automate_alertas_whatsapp.json` | Fluxo de alertas WhatsApp |

---

## 🤝 Suporte

Para dúvidas sobre Power Automate:
1. Consultar `GUIA_POWER_AUTOMATE.md`
2. Documentação oficial: https://learn.microsoft.com/power-automate
3. Comunidade Power Automate: https://powerusers.microsoft.com

---

**Dashboard KPIs Insourcing - Vivo Fibra**  
**Versão 1.0.0 • Dezembro 2024**  
**✅ 3 Automações Incluídas no Pacote!**
