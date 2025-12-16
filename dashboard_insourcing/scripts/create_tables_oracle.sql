-- ============================================================================
-- Script de Criação de Tabelas - Oracle
-- Dashboard KPIs Insourcing - Vivo
-- ============================================================================

-- ============================================================================
-- Tabela Principal: Fato de Métricas Diárias
-- ============================================================================

-- Remover tabela se existir
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE fato_metricas_diarias CASCADE CONSTRAINTS';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;
/

CREATE TABLE fato_metricas_diarias (
    -- Dimensões (Chave Primária)
    data_metrica DATE NOT NULL,
    operacao VARCHAR2(10) NOT NULL,  -- 'B2C' ou 'B2B'
    cidade VARCHAR2(50) NOT NULL,
    gerente VARCHAR2(100) NOT NULL,
    
    -- KPIs Resumo Executivo (6 KPIs)
    nps NUMBER(5,2),
    ocupacao_pct NUMBER(5,2),
    absenteismo_pct NUMBER(5,2),
    tma_seg NUMBER(8,2),
    conversao_pct NUMBER(5,2),
    sla_atendimento_pct NUMBER(5,2),
    
    -- KPIs Qualidade (8 KPIs)
    rechamadas_24h_pct NUMBER(5,2),
    rechamadas_7d_pct NUMBER(5,2),
    transferencia_pct NUMBER(5,2),
    nota_tdna NUMBER(4,2),
    falha_operacional_pct NUMBER(5,2),
    aderencia_processual_pct NUMBER(5,2),
    nota_monitoria_whisper NUMBER(4,2),
    callback_tentado_efetivado_pct NUMBER(5,2),
    
    -- KPIs Produção (10 KPIs)
    chamadas_atendidas NUMBER(10,2),
    abandono_pct NUMBER(5,2),
    rgc_pct NUMBER(5,2),
    tma_producao NUMBER(8,2),
    pausa_pct NUMBER(5,2),
    tempo_logado_hrs NUMBER(6,2),
    abs_pct NUMBER(5,2),
    to_pct NUMBER(5,2),
    produtividade_hc NUMBER(10,2),
    margem_operacional_dre_pct NUMBER(5,2),
    
    -- KPIs Negócios (7 KPIs)
    qnt_negocios_totais NUMBER(10,2),
    conversao_negocios_pct NUMBER(5,2),
    churn_ftth_pos_pct NUMBER(5,2),
    cancelamento_ftth_pct NUMBER(5,2),
    rentabilizacoes_totais_r NUMBER(15,2),
    taxa_retencao_pct NUMBER(5,2),
    arrecadacao_pct NUMBER(5,2),
    
    -- KPIs Financeiro (7 KPIs)
    custo_prv_mensal NUMBER(15,2),
    compensation_total NUMBER(15,2),
    gastos_ferias NUMBER(15,2),
    custo_he NUMBER(15,2),
    custo_unitario_operacao NUMBER(10,2),
    custo_margem_hc NUMBER(15,2),
    valor_taxi NUMBER(10,2),
    
    -- Auditoria
    data_insercao TIMESTAMP DEFAULT SYSTIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT SYSTIMESTAMP,
    
    CONSTRAINT pk_fato_metricas PRIMARY KEY (data_metrica, operacao, cidade, gerente)
);

-- Criar índices para melhor performance
CREATE INDEX ix_fato_metricas_data ON fato_metricas_diarias(data_metrica);
CREATE INDEX ix_fato_metricas_operacao ON fato_metricas_diarias(operacao);
CREATE INDEX ix_fato_metricas_cidade ON fato_metricas_diarias(cidade);
CREATE INDEX ix_fato_metricas_gerente ON fato_metricas_diarias(gerente);

-- Comentários nas colunas
COMMENT ON TABLE fato_metricas_diarias IS 'Tabela fato com métricas diárias de KPIs de Insourcing';
COMMENT ON COLUMN fato_metricas_diarias.data_metrica IS 'Data da métrica';
COMMENT ON COLUMN fato_metricas_diarias.operacao IS 'Tipo de operação: B2C ou B2B';
COMMENT ON COLUMN fato_metricas_diarias.cidade IS 'Cidade/Grupo da operação';
COMMENT ON COLUMN fato_metricas_diarias.gerente IS 'Nome do gerente responsável';

-- ============================================================================
-- Tabela de Metas dos KPIs
-- ============================================================================

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE metas_kpis CASCADE CONSTRAINTS';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;
/

CREATE TABLE metas_kpis (
    kpi_id VARCHAR2(50) PRIMARY KEY,
    kpi_nome VARCHAR2(100) NOT NULL,
    meta_valor NUMBER(10,2),
    inverter NUMBER(1) DEFAULT 0,  -- 1 se menor é melhor, 0 se maior é melhor
    ativo NUMBER(1) DEFAULT 1,
    data_atualizacao TIMESTAMP DEFAULT SYSTIMESTAMP
);

COMMENT ON TABLE metas_kpis IS 'Tabela de metas dos KPIs';
COMMENT ON COLUMN metas_kpis.inverter IS '1 = menor é melhor, 0 = maior é melhor';

-- ============================================================================
-- Inserir Metas Padrão
-- ============================================================================

INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('nps', 'NPS', 70.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('ocupacao', 'Ocupação %', 85.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('absenteismo', 'Absenteísmo %', 5.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('tma', 'TMA (seg)', 300.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('conversao', 'Conversão %', 15.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('sla', 'SLA %', 90.00, 0);

-- Qualidade
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('rechamadas_24h', '% Rechamadas 24hs', 5.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('rechamadas_7d', '% Rechamadas 7 dias', 10.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('transferencia', '% Transferência', 15.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('nota_tdna', 'Nota TDNA', 8.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('falha_operacional', '% Falha Operacional', 3.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('aderencia_processual', '% Aderência Processual', 95.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('nota_monitoria', 'Nota Monitoria Whisper', 8.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('callback', '% CallBack tentado e efetivado', 80.00, 0);

-- Produção
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('chamadas_atendidas', 'Chamadas Atendidas', NULL, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('abandono', '%Abandono', 5.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('rgc', '% RGC', 10.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('tma_producao', 'TMA', 300.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('pausa', '% Pausa', 10.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('tempo_logado', 'Tempo Logado', 6.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('abs', '% Abs', 5.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('to', 'TO', 3.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('produtividade_hc', 'Produtividade / HC', 100.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('margem_operacional', 'Margem Operacional (DRE)', 15.00, 0);

-- Negócios
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('negocios_totais', 'Qnt. Negócios totais', NULL, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('conversao_negocios', '% Conversão', 15.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('churn', '% Churn FTTH / Pós', 2.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('cancelamento_ftth', '% Cancelamento de FTTH', 5.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('rentabilizacoes', 'R$ Rentabilizações totais', NULL, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('taxa_retencao', '%Taxa de Retenção', 85.00, 0);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('arrecadacao', '% arrecadação', 90.00, 0);

-- Financeiro
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('custo_prv', 'Custo PRV mensal', NULL, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('compensation', 'Compensation Total', NULL, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('gastos_ferias', 'Gastos Férias', NULL, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('custo_he', 'Custo HE', NULL, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('custo_unitario', 'Custo unitário por Operação', 25.00, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('custo_margem_hc', 'Custo / margem por HC', NULL, 1);
INSERT INTO metas_kpis (kpi_id, kpi_nome, meta_valor, inverter) VALUES
('valor_taxi', 'Valor Taxi', NULL, 1);

COMMIT;

-- ============================================================================
-- View para facilitar consultas
-- ============================================================================

CREATE OR REPLACE VIEW vw_dashboard_completo AS
SELECT 
    f.*,
    EXTRACT(YEAR FROM f.data_metrica) AS ano,
    EXTRACT(MONTH FROM f.data_metrica) AS mes,
    TO_CHAR(f.data_metrica, 'IW') AS semana,
    TO_CHAR(f.data_metrica, 'Day') AS dia_semana
FROM fato_metricas_diarias f;

-- ============================================================================
-- Procedure para inserir/atualizar dados
-- ============================================================================

CREATE OR REPLACE PROCEDURE sp_inserir_atualizar_metrica (
    p_data IN DATE,
    p_operacao IN VARCHAR2,
    p_cidade IN VARCHAR2,
    p_gerente IN VARCHAR2,
    p_nps IN NUMBER DEFAULT NULL,
    p_ocupacao_pct IN NUMBER DEFAULT NULL
    -- Adicione outros parâmetros conforme necessário
) AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM fato_metricas_diarias
    WHERE data_metrica = p_data
      AND operacao = p_operacao
      AND cidade = p_cidade
      AND gerente = p_gerente;
    
    IF v_count > 0 THEN
        -- Atualizar registro existente
        UPDATE fato_metricas_diarias
        SET 
            nps = NVL(p_nps, nps),
            ocupacao_pct = NVL(p_ocupacao_pct, ocupacao_pct),
            data_atualizacao = SYSTIMESTAMP
        WHERE data_metrica = p_data
          AND operacao = p_operacao
          AND cidade = p_cidade
          AND gerente = p_gerente;
    ELSE
        -- Inserir novo registro
        INSERT INTO fato_metricas_diarias (
            data_metrica, operacao, cidade, gerente,
            nps, ocupacao_pct
        ) VALUES (
            p_data, p_operacao, p_cidade, p_gerente,
            p_nps, p_ocupacao_pct
        );
    END IF;
    
    COMMIT;
END;
/

-- ============================================================================
-- Trigger para atualizar data_atualizacao automaticamente
-- ============================================================================

CREATE OR REPLACE TRIGGER trg_fato_metricas_update
BEFORE UPDATE ON fato_metricas_diarias
FOR EACH ROW
BEGIN
    :NEW.data_atualizacao := SYSTIMESTAMP;
END;
/

-- ============================================================================
-- Dados de exemplo (opcional - remover em produção)
-- ============================================================================

/*
INSERT INTO fato_metricas_diarias (
    data_metrica, operacao, cidade, gerente,
    nps, ocupacao_pct, absenteismo_pct, tma_seg, conversao_pct, sla_atendimento_pct
) VALUES (
    TO_DATE('2024-01-01', 'YYYY-MM-DD'), 'B2C', 'São Paulo', 'João Silva',
    65.5, 82.3, 6.2, 285.0, 12.5, 91.2
);

COMMIT;
*/

-- ============================================================================
-- Verificação final
-- ============================================================================

DECLARE
    v_count_fato NUMBER;
    v_count_metas NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count_fato FROM user_tables WHERE table_name = 'FATO_METRICAS_DIARIAS';
    SELECT COUNT(*) INTO v_count_metas FROM user_tables WHERE table_name = 'METAS_KPIS';
    
    DBMS_OUTPUT.PUT_LINE('✅ Script executado com sucesso!');
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('Tabelas criadas:');
    DBMS_OUTPUT.PUT_LINE('  - fato_metricas_diarias: ' || v_count_fato);
    DBMS_OUTPUT.PUT_LINE('  - metas_kpis: ' || v_count_metas);
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('Views criadas:');
    DBMS_OUTPUT.PUT_LINE('  - vw_dashboard_completo');
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('Procedures criadas:');
    DBMS_OUTPUT.PUT_LINE('  - sp_inserir_atualizar_metrica');
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('Próximos passos:');
    DBMS_OUTPUT.PUT_LINE('1. Inserir seus dados na tabela fato_metricas_diarias');
    DBMS_OUTPUT.PUT_LINE('2. Configurar database_connector.py com suas credenciais');
    DBMS_OUTPUT.PUT_LINE('3. Executar: python dashboard_app_final.py');
END;
/
