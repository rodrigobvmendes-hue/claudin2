# Instruções para exportar PDF a partir do PPTX

Arquivo fonte: `reports/book_comite_infraestrutura.pptx`

Opção 1 — LibreOffice (Linux/macOS com LibreOffice instalado):

```bash
soffice --headless --convert-to pdf --outdir reports reports/book_comite_infraestrutura.pptx
```

Opção 2 — Microsoft PowerPoint (Windows/macOS):
- Abrir `reports/book_comite_infraestrutura.pptx` no PowerPoint
- Arquivo -> Exportar -> Criar PDF/XPS (selecionar qualidade e exportar para `reports/`)

Opção 3 — Usando Python (quando não houver LibreOffice/PowerPoint disponíveis):
- Requer `python-pptx` e bibliotecas externas para renderizar (geralmente não recomendada para produção).
- Melhor usar PowerPoint ou LibreOffice para manter fidelidade visual.

Observações:
- Não altere o arquivo `docs/templetes/*` (templates) — o PPTX já foi gerado mantendo os templates intactos.
- O PDF final ficará em `reports/book_comite_infraestrutura.pdf` após a conversão.
