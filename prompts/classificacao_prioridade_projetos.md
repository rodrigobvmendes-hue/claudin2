# Prompt: Classificação de prioridade dos projetos

Objetivo: classificar projetos de infraestrutura de combustíveis líquidos conforme prioridade de execução e impacto.

## Instruções

- Use os critérios de prioridade descritos em `CLAUDE.md`.
- Separe projetos em: imediata, 1 a 3 anos, 3 a 10 anos, 10+ anos.
- Considere: probabilidade de execução, impacto competitivo, status atual e horizonte provável.
- Inclua breves razões para a classificação.

## Estrutura de saída

1. Projeto
2. Categoria de prioridade
3. Razão principal
4. Status atual
5. Impacto esperado
6. Risco principal

## Pontos de decisão

- Prioridade imediata: operacional, em obra avançada, autorizado ou com impacto relevante em 0-2 anos.
- 1 a 3 anos: alta chance de execução, impacto regional ou janela comercial antecipada.
- 3 a 10 anos: relevante, mas com incerteza de execução, licenciamento, concessão ou financiamento.
- 10+ anos: projeto estrutural de longo prazo, sem decisão comercial imediata.
