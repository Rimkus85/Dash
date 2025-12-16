-- ============================================================================
-- Script de Criação de Tabelas - SQL Server
-- Dashboard KPIs Insourcing - Vivo
-- ============================================================================

USE [DashboardInsourcing];  -- Altere para o nome do seu banco
GO

-- ============================================================================
-- Tabela Principal: Fato de Métricas Diárias
-- ============================================================================

IF OBJECT_ID('dbo.fato_metricas_diarias', 'U') IS NOT NULL
    DROP TABLE dbo.fato_metricas_diarias;
GO

CREATE TABLE dbo.fato_metricas_diarias (
    -- Dimensões (Chave Primária)
    Data DATE NOT NULL,
    Operacao VARCHAR(10) NOT NULL,  -- 'B2C' ou 'B2B'
    Cidade VARCHAR(50) NOT NULL,
    Gerente VARCHAR(100) NOT NULL,
    
    -- KPIs Resumo Executivo (6 KPIs)
    NPS DECIMAL(5,2) NULL,
    Ocupacao_Pct DECIMAL(5,2) NULL,
    Absenteismo_Pct DECIMAL(5,2) NULL,
    TMA_Seg DECIMAL(8,2) NULL,
    Conversao_Pct DECIMAL(5,2) NULL,
    SLA_Atendimento_Pct DECIMAL(5,2) NULL,
    
    -- KPIs Qualidade (8 KPIs)
    Rechamadas_24h_Pct DECIMAL(5,2) NULL,
    Rechamadas_7d_Pct DECIMAL(5,2) NULL,
    Transferencia_Pct DECIMAL(5,2) NULL,
    Nota_TDNA DECIMAL(4,2) NULL,
    Falha_Operacional_Pct DECIMAL(5,2) NULL,
    Aderencia_Processual_Pct DECIMAL(5,2) NULL,
    Nota_Monitoria_Whisper DECIMAL(4,2) NULL,
    CallBack_Tentado_Efetivado_Pct DECIMAL(5,2) NULL,
    
    -- KPIs Produção (10 KPIs)
    Chamadas_Atendidas DECIMAL(10,2) NULL,
    Abandono_Pct DECIMAL(5,2) NULL,
    RGC_Pct DECIMAL(5,2) NULL,
    TMA_Producao DECIMAL(8,2) NULL,
    Pausa_Pct DECIMAL(5,2) NULL,
    Tempo_Logado_Hrs DECIMAL(6,2) NULL,
    Abs_Pct DECIMAL(5,2) NULL,
    TO_Pct DECIMAL(5,2) NULL,
    Produtividade_HC DECIMAL(10,2) NULL,
    Margem_Operacional_DRE_Pct DECIMAL(5,2) NULL,
    
    -- KPIs Negócios (7 KPIs)
    Qnt_Negocios_Totais DECIMAL(10,2) NULL,
    Conversao_Negocios_Pct DECIMAL(5,2) NULL,
    Churn_FTTH_Pos_Pct DECIMAL(5,2) NULL,
    Cancelamento_FTTH_Pct DECIMAL(5,2) NULL,
    Rentabilizacoes_Totais_R DECIMAL(15,2) NULL,
    Taxa_Retencao_Pct DECIMAL(5,2) NULL,
    Arrecadacao_Pct DECIMAL(5,2) NULL,
    
    -- KPIs Financeiro (7 KPIs)
    Custo_PRV_Mensal DECIMAL(15,2) NULL,
    Compensation_Total DECIMAL(15,2) NULL,
    Gastos_Ferias DECIMAL(15,2) NULL,
    Custo_HE DECIMAL(15,2) NULL,
    Custo_Unitario_Operacao DECIMAL(10,2) NULL,
    Custo_Margem_HC DECIMAL(15,2) NULL,
    Valor_Taxi DECIMAL(10,2) NULL,
    
    -- Auditoria
    Data_Insercao DATETIME DEFAULT GETDATE(),
    Data_Atualizacao DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT PK_fato_metricas PRIMARY KEY (Data, Operacao, Cidade, Gerente)
);
GO

-- Criar índices para melhor performance
CREATE INDEX IX_fato_metricas_data ON dbo.fato_metricas_diarias(Data);
CREATE INDEX IX_fato_metricas_operacao ON dbo.fato_metricas_diarias(Operacao);
CREATE INDEX IX_fato_metricas_cidade ON dbo.fato_metricas_diarias(Cidade);
CREATE INDEX IX_fato_metricas_gerente ON dbo.fato_metricas_diarias(Gerente);
GO

-- ============================================================================
-- Tabela de Metas dos KPIs
-- ============================================================================

IF OBJECT_ID('dbo.metas_kpis', 'U') IS NOT NULL
    DROP TABLE dbo.metas_kpis;
GO

CREATE TABLE dbo.metas_kpis (
    kpi_id VARCHAR(50) PRIMARY KEY,
    kpi_nome VARCHAR(100) NOT NULL,
    meta_valor DECIMAL(10,2) NULL,
    inverter BIT DEFAULT 0,  -- 1 se menor é melhor, 0 se maior é melhor
    ativo BIT DEFAULT 1,
    Data_Atualizacao DATETIME DEFAULT GETDATE()
);
GO

-- ============================================================================
-- Inserir Metas Padrão
-- ============================================================================

INSERT INTO dbo.metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
-- Resumo Executivo
('nps', 'NPS', 70.00, 0),
('ocupacao', 'Ocupação %', 85.00, 0),
('absenteismo', 'Absenteísmo %', 5.00, 1),
('tma', 'TMA (seg)', 300.00, 1),
('conversao', 'Conversão %', 15.00, 0),
('sla', 'SLA %', 90.00, 0),

-- Qualidade
('rechamadas_24h', '% Rechamadas 24hs', 5.00, 1),
('rechamadas_7d', '% Rechamadas 7 dias', 10.00, 1),
('transferencia', '% Transferência', 15.00, 1),
('nota_tdna', 'Nota TDNA', 8.00, 0),
('falha_operacional', '% Falha Operacional', 3.00, 1),
('aderencia_processual', '% Aderência Processual', 95.00, 0),
('nota_monitoria', 'Nota Monitoria Whisper', 8.00, 0),
('callback', '% CallBack tentado e efetivado', 80.00, 0),

-- Produção
('chamadas_atendidas', 'Chamadas Atendidas', NULL, 0),
('abandono', '%Abandono', 5.00, 1),
('rgc', '% RGC', 10.00, 0),
('tma_producao', 'TMA', 300.00, 1),
('pausa', '% Pausa', 10.00, 1),
('tempo_logado', 'Tempo Logado', 6.00, 0),
('abs', '% Abs', 5.00, 1),
('to', 'TO', 3.00, 1),
('produtividade_hc', 'Produtividade / HC', 100.00, 0),
('margem_operacional', 'Margem Operacional (DRE)', 15.00, 0),

-- Negócios
('negocios_totais', 'Qnt. Negócios totais', NULL, 0),
('conversao_negocios', '% Conversão', 15.00, 0),
('churn', '% Churn FTTH / Pós', 2.00, 1),
('cancelamento_ftth', '% Cancelamento de FTTH', 5.00, 1),
('rentabilizacoes', 'R$ Rentabilizações totais', NULL, 0),
('taxa_retencao', '%Taxa de Retenção', 85.00, 0),
('arrecadacao', '% arrecadação', 90.00, 0),

-- Financeiro
('custo_prv', 'Custo PRV mensal', NULL, 1),
('compensation', 'Compensation Total', NULL, 1),
('gastos_ferias', 'Gastos Férias', NULL, 1),
('custo_he', 'Custo HE', NULL, 1),
('custo_unitario', 'Custo unitário por Operação', 25.00, 1),
('custo_margem_hc', 'Custo / margem por HC', NULL, 1),
('valor_taxi', 'Valor Taxi', NULL, 1);
GO

-- ============================================================================
-- View para facilitar consultas
-- ============================================================================

IF OBJECT_ID('dbo.vw_dashboard_completo', 'V') IS NOT NULL
    DROP VIEW dbo.vw_dashboard_completo;
GO

CREATE VIEW dbo.vw_dashboard_completo AS
SELECT 
    f.*,
    YEAR(f.Data) AS Ano,
    MONTH(f.Data) AS Mes,
    DATEPART(WEEK, f.Data) AS Semana,
    DATENAME(WEEKDAY, f.Data) AS DiaSemana
FROM dbo.fato_metricas_diarias f;
GO

-- ============================================================================
-- Procedure para inserir/atualizar dados
-- ============================================================================

IF OBJECT_ID('dbo.sp_inserir_atualizar_metrica', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_inserir_atualizar_metrica;
GO

CREATE PROCEDURE dbo.sp_inserir_atualizar_metrica
    @Data DATE,
    @Operacao VARCHAR(10),
    @Cidade VARCHAR(50),
    @Gerente VARCHAR(100),
    @NPS DECIMAL(5,2) = NULL,
    @Ocupacao_Pct DECIMAL(5,2) = NULL
    -- Adicione outros parâmetros conforme necessário
AS
BEGIN
    SET NOCOUNT ON;
    
    IF EXISTS (
        SELECT 1 FROM dbo.fato_metricas_diarias 
        WHERE Data = @Data 
          AND Operacao = @Operacao 
          AND Cidade = @Cidade 
          AND Gerente = @Gerente
    )
    BEGIN
        -- Atualizar registro existente
        UPDATE dbo.fato_metricas_diarias
        SET 
            NPS = ISNULL(@NPS, NPS),
            Ocupacao_Pct = ISNULL(@Ocupacao_Pct, Ocupacao_Pct),
            Data_Atualizacao = GETDATE()
        WHERE Data = @Data 
          AND Operacao = @Operacao 
          AND Cidade = @Cidade 
          AND Gerente = @Gerente;
    END
    ELSE
    BEGIN
        -- Inserir novo registro
        INSERT INTO dbo.fato_metricas_diarias (
            Data, Operacao, Cidade, Gerente, 
            NPS, Ocupacao_Pct
        )
        VALUES (
            @Data, @Operacao, @Cidade, @Gerente,
            @NPS, @Ocupacao_Pct
        );
    END
END;
GO

-- ============================================================================
-- Dados de exemplo (opcional - remover em produção)
-- ============================================================================

/*
INSERT INTO dbo.fato_metricas_diarias (
    Data, Operacao, Cidade, Gerente,
    NPS, Ocupacao_Pct, Absenteismo_Pct, TMA_Seg, Conversao_Pct, SLA_Atendimento_Pct
)
VALUES 
    ('2024-01-01', 'B2C', 'São Paulo', 'João Silva', 65.5, 82.3, 6.2, 285.0, 12.5, 91.2),
    ('2024-01-01', 'B2B', 'São Paulo', 'Maria Santos', 68.2, 85.1, 5.8, 295.0, 14.2, 93.5);
*/

-- ============================================================================
-- Verificação final
-- ============================================================================

PRINT '✅ Tabelas criadas com sucesso!';
PRINT '';
PRINT 'Tabelas criadas:';
PRINT '  - dbo.fato_metricas_diarias';
PRINT '  - dbo.metas_kpis';
PRINT '';
PRINT 'Views criadas:';
PRINT '  - dbo.vw_dashboard_completo';
PRINT '';
PRINT 'Procedures criadas:';
PRINT '  - dbo.sp_inserir_atualizar_metrica';
PRINT '';
PRINT 'Próximos passos:';
PRINT '1. Inserir seus dados na tabela fato_metricas_diarias';
PRINT '2. Configurar database_connector.py com suas credenciais';
PRINT '3. Executar: python dashboard_app_final.py';
GO

-- ============================================================================
-- COLUNAS ADICIONADAS PARA AGREGAÇÃO INTELIGENTE (Versão 2.0)
-- ============================================================================

-- Campo Grupo (separado de Cidade)
ALTER TABLE fato_metricas_diarias ADD Grupo VARCHAR(50);

-- Colunas para Ocupação
ALTER TABLE fato_metricas_diarias ADD Ocupacao_Tempo_Ocupado_Hrs DECIMAL(10,2);

-- Colunas para Absenteísmo
ALTER TABLE fato_metricas_diarias ADD Absenteismo_Dias_Ausentes DECIMAL(10,2);
ALTER TABLE fato_metricas_diarias ADD Absenteismo_Dias_Uteis INT;

-- Colunas para TMA
ALTER TABLE fato_metricas_diarias ADD TMA_Tempo_Total_Seg DECIMAL(15,2);

-- Colunas para Conversão
ALTER TABLE fato_metricas_diarias ADD Conversao_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Conversao_Denominador INT;

-- Colunas para SLA
ALTER TABLE fato_metricas_diarias ADD SLA_Atendidas_Dentro_Meta INT;
ALTER TABLE fato_metricas_diarias ADD SLA_Total_Chamadas INT;

-- Colunas para Rechamadas 24h
ALTER TABLE fato_metricas_diarias ADD Rechamadas_24h_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Rechamadas_24h_Denominador INT;

-- Colunas para Rechamadas 7d
ALTER TABLE fato_metricas_diarias ADD Rechamadas_7d_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Rechamadas_7d_Denominador INT;

-- Colunas para Transferência
ALTER TABLE fato_metricas_diarias ADD Transferencia_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Transferencia_Denominador INT;

-- Colunas para Falha Operacional
ALTER TABLE fato_metricas_diarias ADD Falha_Operacional_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Falha_Operacional_Denominador INT;

-- Colunas para Aderência Processual
ALTER TABLE fato_metricas_diarias ADD Aderencia_Processual_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Aderencia_Processual_Denominador INT;

-- Colunas para CallBack
ALTER TABLE fato_metricas_diarias ADD Callback_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Callback_Denominador INT;

-- Colunas para Abandono
ALTER TABLE fato_metricas_diarias ADD Abandono_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Abandono_Denominador INT;

-- Colunas para RGC
ALTER TABLE fato_metricas_diarias ADD RGC_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD RGC_Denominador INT;

-- Colunas para TMA Produção
ALTER TABLE fato_metricas_diarias ADD TMA_Producao_Tempo_Total DECIMAL(15,2);

-- Colunas para Pausa
ALTER TABLE fato_metricas_diarias ADD Pausa_Tempo_Hrs DECIMAL(10,2);

-- Colunas para Absenteísmo Produção
ALTER TABLE fato_metricas_diarias ADD Abs_Dias_Ausentes DECIMAL(10,2);
ALTER TABLE fato_metricas_diarias ADD Abs_Dias_Uteis INT;

-- Colunas para TO (Turnover)
ALTER TABLE fato_metricas_diarias ADD TO_Saidas INT;
ALTER TABLE fato_metricas_diarias ADD TO_Headcount INT;

-- Colunas para Margem Operacional
ALTER TABLE fato_metricas_diarias ADD Margem_Operacional_Receita DECIMAL(15,2);
ALTER TABLE fato_metricas_diarias ADD Margem_Operacional_Custo DECIMAL(15,2);

-- Colunas para Conversão Negócios
ALTER TABLE fato_metricas_diarias ADD Conversao_Negocios_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Conversao_Negocios_Denominador INT;

-- Colunas para Churn
ALTER TABLE fato_metricas_diarias ADD Churn_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Churn_Denominador INT;

-- Colunas para Cancelamento FTTH
ALTER TABLE fato_metricas_diarias ADD Cancelamento_FTTH_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Cancelamento_FTTH_Denominador INT;

-- Colunas para Taxa Retenção
ALTER TABLE fato_metricas_diarias ADD Taxa_Retencao_Numerador INT;
ALTER TABLE fato_metricas_diarias ADD Taxa_Retencao_Denominador INT;

-- Colunas para Arrecadação
ALTER TABLE fato_metricas_diarias ADD Arrecadacao_Numerador DECIMAL(15,2);
ALTER TABLE fato_metricas_diarias ADD Arrecadacao_Denominador DECIMAL(15,2);

-- ============================================================================
-- TOTAL: 36 novas colunas + 1 campo Grupo = 37 alterações
-- ============================================================================
