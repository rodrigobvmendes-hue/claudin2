# Radar Vivo de Infraestrutura de Combustíveis Líquidos

## Objetivo do projeto
Radar vivo de infraestrutura de combustíveis líquidos no Brasil, cruzando informação de mercado externo e o Plano Diretor interno da ALE.

## Público autorizado
Acesso restrito à responsável pelo projeto e às pessoas expressamente autorizadas.

## Classificação
Este repositório contém informações confidenciais, incluindo dados internos da ALE, contratos, custos, negociações, NPV, status de projetos, phase-outs e análises estratégicas.

## Estrutura do repositório
- `source_documents/mercado` — fontes públicas e documentos de mercado.
- `source_documents/interno_confidencial` — documentos internos confidenciais da ALE.
- `data` — bases de dados estruturadas e índices de fontes.
- `intelligence` — relatórios executivos e notas estratégicas.
- `prompts` — prompts operacionais para atualização e revisão.
- `reports` — entregáveis, análises e materiais de acompanhamento.

## Separação obrigatória
- Mercado externo não deve ser misturado com informação interna confidencial.
- Dados internos da ALE nunca devem ser tratados como fonte pública.

## Bases principais
- `data/mercado_projetos_infraestrutura.csv`
- `data/ale_plano_diretor_projetos.csv`
- `data/ale_contratos_armazenagem.csv`
- `data/matriz_cruzamento_mercado_ale.csv`
- `data/fontes_documentos.csv`

## Governança do dado
A coluna `natureza_do_dado` define a proveniência e o grau de inferência:
- `extraído_literalmente` — informação retirada literalmente do documento.
- `normalizado_a_partir_da_fonte` — texto reorganizado, sem nova conclusão.
- `análise_derivada` — interpretações ou cruzamentos entre fontes.
- `não_identificado` — quando não há evidência clara para classificar.

## Rotina mensal
O prompt oficial de atualização está em `prompts/rotina_mensal_radar_e_comite.md`.

## Regras de segurança
- Não compartilhar documentos internos fora do grupo autorizado.
- Não copiar dados internos em materiais externos.
- Não tratar análises derivadas como fato.
- Não commitar arquivos temporários.
- Não usar informações sem fonte identificada para decisão executiva.

## Aviso final
Este repositório é uma base de inteligência estratégica interna, não um material público.