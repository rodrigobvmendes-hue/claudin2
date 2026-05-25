# Prompt: Rotina mensal de radar e comitê

Objetivo: orientar a atualização mensal completa do projeto de radar de infraestrutura de combustíveis líquidos, incluindo fontes, CSVs de monitoramento e relatórios executivos.

## Instruções operacionais

1. Verifique se há novos documentos em `source_documents`.
2. Atualize o índice de fontes em `data/fontes_documentos.csv`.
3. Atualize os CSVs de monitoramento:
   - `data/mercado_projetos_infraestrutura.csv`
   - `data/ale_plano_diretor_projetos.csv`
   - `data/ale_contratos_armazenagem.csv`
   - `data/matriz_cruzamento_mercado_ale.csv`
4. Preserve a separação entre mercado externo e interno confidencial.
5. Para cada linha de CSV, registre `natureza_do_dado` com uma das opções:
   - `extraído_literalmente`
   - `normalizado_a_partir_da_fonte`
   - `análise_derivada`
   - `não_identificado`
6. Atualize os relatórios executivos:
   - `intelligence/radar_mercado/sintese_executiva_mercado.md`
   - `intelligence/plano_diretor_ale/status_executivo_plano_interno.md`
   - `intelligence/cruzamentos_estrategicos/agenda_prioritaria_comite.md`
7. Gere um changelog executivo contendo:
   - o que mudou no mês
   - quais projetos subiram de prioridade
   - quais projetos ficaram em holding
   - quais decisões precisam de comitê
   - quais lacunas de informação permanecem
8. Nunca invente dados.
9. Nunca trate informação interna confidencial como fonte pública.
10. Separe claramente fato, normalização e análise derivada.

## Estrutura de saída

### 1. Atualização do índice de fontes
- Identificar novos documentos em `source_documents`.
- Registrar cada fonte com metadados relevantes.

### 2. Atualização dos CSVs
- `mercado_projetos_infraestrutura.csv`: só informação pública de mercado.
- `ale_plano_diretor_projetos.csv`: só informação interna ALE.
- `ale_contratos_armazenagem.csv`: contratos, custos e despesas internas.
- `matriz_cruzamento_mercado_ale.csv`: cruzamentos entre mercado público e iniciativas internas.

Para cada CSV:
- mantenha os projetos existentes do repositório;
- não inclua novos projetos sem evidência;
- marque `natureza_do_dado` conforme a origem do dado.

### 3. Atualização dos relatórios executivos
- `sintese_executiva_mercado.md`: foco no mercado externo.
- `status_executivo_plano_interno.md`: foco no plano interno da ALE.
- `agenda_prioritaria_comite.md`: foco nas decisões e alinhamento com o mercado.

### 4. Changelog executivo
- Apresente mudanças no mês de forma objetiva.
- Identifique projetos que subiram de prioridade.
- Liste projetos em holding.
- Destaque decisões pendentes de comitê.
- Aponte lacunas de informação que ainda precisam ser validadas.

## Regras de qualidade

- Use sempre evidência do documento ou do CSV.
- Dê preferência a `extraído_literalmente` quando o dado estiver literalmente no documento.
- Use `normalizado_a_partir_da_fonte` quando reorganizar texto sem gerar novas conclusões.
- Use `análise_derivada` apenas para cruzamentos e interpretações explícitas.
- Use `não_identificado` quando não houver evidência clara.
- Não misture confidencial interno ALE com informações externas de mercado.
- Evite frases vagas: descreva claramente a origem do dado.

## Observações finais
Este prompt deve ser usado todo mês para atualizar rota e governança do projeto. Ele é operacional e padroniza a produção de fontes, dados e relatórios executivos sem alterar a lógica de conteúdo do repositório.
