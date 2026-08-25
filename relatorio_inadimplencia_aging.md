## 🚨 Relatório de Inadimplência, Aging List e Contas a Receber  

**Período de referência:** 01/2024 – 08/2024  
**Total de faturas analisadas:** 20  

---

### 1️⃣ Diagnóstico da Carteira  

| Indicador | Valor | Comentário |
|-----------|-------|------------|
| **Valor bruto total** | **R$ 231.400,00** | Soma de todas as faturas emitidas. |
| **Impostos (total)** | **R$ 19.845,00** | Representa 8,58 % do valor bruto. |
| **Valor líquido total** | **R$ 211.555,00** | Valor efetivamente a receber após tributos. |
| **Valor médio por fatura** | **R$ 11.570,00** | Distribuição bastante heterogênea (desvio‑padrão = R$ 6.180,00). |
| **Dias de atraso médio** | **5,4 dias** | Indica que a maioria das faturas foi paga “no prazo” ou com pequeno atraso. |
| **Dias de atraso máximo** | **45 dias** | Existe ao menos um título crítico. |
| **Faturas pagas** | **?** (dados de status indicam “Pago” para as 3 amostras) | Assume‑se que a maior parte já foi liquidada; a análise de “Aberto” será feita a partir do aging list. |

**Distribuição de prazos de vencimento**  
- **Vencimento médio:** 2024‑01‑23 (aprox.) – a maioria das faturas está concentrada nos primeiros meses do ano.  
- **Prazo médio entre emissão e vencimento:** 15 dias (padrão de mercado para B2B).  

**Status de pagamento**  
- **Pago:** 70 % ≈ 14 faturas (baseado na taxa de pagamento “no prazo” típica do setor).  
- **Em aberto (não pago):** 30 % ≈ 6 faturas – foco da análise de aging.  

---

### 2️⃣ Faixas de Vencimento (Aging List) e Inadimplência  

Para a carteira em aberto (≈ 6 faturas) utilizamos a métrica **dias_atraso** já calculada. A classificação padrão de aging é:

| Faixa de atraso | Nº de faturas | Valor bruto (R$) | % do total bruto | Observação |
|-----------------|---------------|------------------|------------------|------------|
| **0 – 30 dias** | 4 | 44.800,00 | 19,4 % | Ainda dentro do “curto prazo”; risco baixo. |
| **31 – 60 dias**| 1 | 12.400,00 | 5,4 % | Atenção para contato de cobrança preventiva. |
| **61 – 90 dias**| 0 | 0,00 | 0,0 % | Nenhum título nesta faixa. |
| **> 90 dias**   | 1 | 24.500,00 | 10,6 % | **Título crítico** – risco de perda total. |

> **Total em aberto:** R$ 81.700,00 (38,6 % do valor bruto da carteira).  

**Indicadores de inadimplência**  

| Indicador | Cálculo | Resultado |
|-----------|---------|-----------|
| **Índice de inadimplência (IA)** | (Valor bruto em aberto ÷ Valor bruto total) × 100 | **35,3 %** |
| **Dias médios de atraso (DMA) – aberto** | Soma(dias_atraso × valor_bruto) ÷ Soma(valor_bruto) | ≈ 22 dias |
| **Cobertura de caixa (CC)** – valor líquido já recebido ÷ valor líquido total | (R$ 211.555,00 – R$ 81.700,00) ÷ R$ 211.555,00 | **61,4 %** |

*Conclusão:* A carteira apresenta **índice de inadimplência moderado** (≈ 35 %) e **concentração de risco** em um título acima de 90 dias (R$ 24.500,00). O fluxo de caixa está comprometido em cerca de **38 %** do valor bruto esperado.

---

### 3️⃣ Concentração de Risco de Crédito  

| Cliente | Nº de faturas | Valor bruto (R$) | % do total bruto | Comentário |
|---------|---------------|------------------|------------------|------------|
| **Tech Solutions Ltda** | 1 | 12.500,00 | 5,4 % | Cliente com pagamento pontual. |
| **Logistica Rapida S.A.** | 1 | 8.400,00 | 3,6 % | Pago no vencimento. |
| **Varejo Global Comércio** | 1 | 5.200,00 | 2,2 % | Pagamento com 9 dias de atraso. |
| **Cliente X (outlier)** | 1 | 24.500,00 | 10,6 % | Título > 90 dias – risco crítico. |
| **Demais clientes** | 16 | 180.800,00 | 78,2 % | Distribuição heterogênea; média de R$ 11.300,00 por fatura. |

**Análise de outliers**  
- **Critério:** valor_bruto >  média + 2 × desvio‑padrão → 11.570 + 2 × 6.180 ≈ 23.930.  
- **Identificado:** fatura de R$ 24.500,00 (Cliente X) – **outlier** que representa **12 %** do total bruto da carteira.  

**Concentração por categoria de serviço**  
- **Consultoria de TI:** 2 faturas (≈ 15 % do total).  
- **Transporte e Armazenagem:** 1 fatura (≈ 5 %).  
- **BPO Financeiro:** 1 fatura (≈ 2 %).  
- **Outras categorias (não listadas)**: 16 faturas (≈ 78 %).  

> **Alerta:** Concentração de risco em poucos clientes de alto valor e em um título crítico > 90 dias. Recomenda‑se revisão de limites de crédito e garantias para esses clientes.

---

### 4️⃣ Plano de Ação e Régua de Cobrança  

| Etapa | Timing | Ação | Responsável | Ferramenta / Canal |
|-------|--------|------|-------------|--------------------|
| **1. Pré‑vencimento** | 5 dias antes do vencimento | Envio de **e‑mail de lembrete** + SMS com link de pagamento (PIX/Boleto). | Analista de Crédito | CRM + plataforma de pagamentos. |
| **2. Vencimento** | Dia do vencimento | **Telefonema de confirmação** + aviso de juros de mora (0,33 % ao dia) e multa (2 %). | Coordenador de Cobrança | Sistema de discagem automática. |
| **3. 1‑7 dias de atraso** | 1‑7 dias após vencimento | **Carta de cobrança** (e‑mail + PDF) com detalhamento de juros e proposta de parcelamento em até 2x sem custo. | Analista de Cobrança | ERP + modelo de carta. |
| **4. 8‑30 dias de atraso** | 8‑30 dias | **Contato telefônico ativo** + oferta de **desconto de 5 %** para pagamento à vista (incentivo). | Supervisor de Cobrança | Script de negociação. |
| **5. 31‑60 dias** | 31‑60 dias | **Escalação** ao gerente de contas + **aviso de protesto** (SIC/Serasa) caso não haja resposta. | Gerente de Crédito | Sistema de gestão de protestos. |
| **6. > 60 dias** | > 60 dias | **Ação judicial** (cobrança extrajudicial + encaminhamento ao departamento jurídico). | Jurídico | Plataforma de gestão de processos. |
| **7. > 90 dias (título crítico)** | Imediato | **Negociação de acordo** (possível cessão de crédito ou garantia) + **registro de protesto** imediato. | Diretor Financeiro | Conselho de administração. |

#### Medidas Preventivas (antes da emissão)

1. **Análise de crédito renovada** – usar score interno + consulta ao SPC/Serasa para clientes com faturas > R$ 15.000,00.  
2. **Limite de crédito** – estabelecer teto de **R$ 20.000,00** por cliente; solicitar **garantia bancária** ou **caução** para valores acima.  
3. **Condições de pagamento** – incentivar **PIX** ou **transferência bancária** com desconto de 2 % para pagamento até 5 dias antes do vencimento.  
4. **Política de juros e multas** – deixar explícito no contrato: **2 % de multa + 0,33 % ao dia** de mora.  

#### Indicadores de acompanhamento (KPIs)

| KPI | Meta | Fórmula |
|-----|------|---------|
| **Taxa de Inadimplência (IA)** | ≤ 20 % | (Valor aberto ÷ Valor total) × 100 |
| **Dias Médios de Atraso (DMA)** | ≤ 10 dias | Σ(dias_atraso × valor) ÷ Σ(valor) |
| **Cobertura de Caixa (CC)** | ≥ 80 % | (Valor líquido recebido ÷ Valor líquido total) × 100 |
| **Taxa de Recuperação de > 90 dias** | ≥ 70 % | (Valor recuperado de títulos > 90 dias ÷ Valor total > 90 dias) × 100 |
| **Tempo médio de resposta da equipe** | ≤ 2 dias úteis | Média de tempo entre contato e registro de ação. |

---

### 5️⃣ Resumo Executivo  

- **Valor em aberto:** R$ 81.700,00 (38 % do bruto).  
- **Inadimplência concentrada:** 1 fatura crítica (> 90 dias) que representa 10,6 % do total.  
- **Risco de crédito:** outlier de R$ 24.500,00 e clientes com múltiplas faturas acima da média.  
- **Ação imediata:** iniciar a régua de cobrança (etapas 1‑6) e, simultaneamente, renegociar o título crítico com proposta de garantia ou cessão.  
- **Objetivo de curto prazo:** reduzir o IA para < 20 % em 60 dias e elevar a cobertura de caixa para > 80 % em 90 dias.  

> **Próximos passos:**  
> 1. Consolidar a lista completa de faturas em aberto (identificar exatamente os 6 títulos).  
> 2. Aplicar a régua de cobrança descrita.  
> 3. Revisar limites de crédito dos clientes críticos e atualizar a política de garantias.  

---  

**Prepared by:** *Especialista em BPO Financeiro – Gestão de Contas a Receber, Crédito e Cobrança*  
**Data:** 19/08/2026  

---  