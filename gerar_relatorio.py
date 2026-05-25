#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RADAR ESTRATÉGICO DE INFRAESTRUTURA — COMBUSTÍVEIS LÍQUIDOS NO BRASIL
Analista Sênior | Distribuidora Nacional | Maio/2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import datetime

# ── Paleta ────────────────────────────────────────────────────────────────────
DARK_BLUE    = colors.HexColor('#1A2B4A')
MID_BLUE     = colors.HexColor('#2563EB')
LIGHT_BLUE   = colors.HexColor('#DBEAFE')
ACCENT_RED   = colors.HexColor('#DC2626')
ACCENT_AMBER = colors.HexColor('#D97706')
ACCENT_GREEN = colors.HexColor('#059669')
ACCENT_GRAY  = colors.HexColor('#6B7280')
TABLE_HEAD   = colors.HexColor('#1E3A5F')
TABLE_ALT    = colors.HexColor('#F0F4FF')
BORDER_GRAY  = colors.HexColor('#CBD5E1')
SECTION_BG   = colors.HexColor('#EFF6FF')
AMEACA_BG    = colors.HexColor('#FEF2F2')
OPP_BG       = colors.HexColor('#F0FDF4')

W, H = A4
styles = getSampleStyleSheet()

def make_style(name, **kwargs):
    base = kwargs.pop('parent', 'Normal')
    return ParagraphStyle(name=name, parent=styles[base], **kwargs)

# ── Estilos ───────────────────────────────────────────────────────────────────
COVER_TITLE  = make_style('CT', fontSize=26, textColor=colors.white,
    fontName='Helvetica-Bold', alignment=TA_LEFT, spaceAfter=8, leading=32)
COVER_SUB    = make_style('CS', fontSize=13, textColor=colors.HexColor('#BFDBFE'),
    fontName='Helvetica', alignment=TA_LEFT, spaceAfter=4, leading=18)
COVER_META   = make_style('CM', fontSize=10, textColor=colors.HexColor('#93C5FD'),
    fontName='Helvetica', alignment=TA_LEFT, leading=15)
COVER_TAG    = make_style('CTG', fontSize=8, textColor=colors.HexColor('#BFDBFE'),
    fontName='Helvetica-Bold', alignment=TA_LEFT, leading=12)

SEC_TITLE    = make_style('ST', fontSize=15, textColor=DARK_BLUE,
    fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=4, leading=20)
SUBSEC       = make_style('SS', fontSize=11, textColor=MID_BLUE,
    fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=3, leading=15)
BODY         = make_style('BD', fontSize=8.5, textColor=colors.HexColor('#1F2937'),
    fontName='Helvetica', spaceAfter=4, leading=13, alignment=TA_JUSTIFY)
BODY_B       = make_style('BDB', fontSize=8.5, textColor=DARK_BLUE,
    fontName='Helvetica-Bold', spaceAfter=4, leading=13)
BULLET_S     = make_style('BLS', fontSize=8.5, textColor=colors.HexColor('#1F2937'),
    fontName='Helvetica', leftIndent=14, spaceAfter=3, leading=13, bulletIndent=4)
NOTE_S       = make_style('NS', fontSize=7.5, textColor=ACCENT_GRAY,
    fontName='Helvetica-Oblique', spaceAfter=3, leading=11, leftIndent=8,
    backColor=SECTION_BG)
TH           = make_style('TH', fontSize=7.2, textColor=colors.white,
    fontName='Helvetica-Bold', alignment=TA_CENTER, leading=10)
TC           = make_style('TC', fontSize=7.0, textColor=colors.HexColor('#111827'),
    fontName='Helvetica', alignment=TA_LEFT, leading=10, wordWrap='CJK')
TC_B         = make_style('TCB', fontSize=7.0, textColor=DARK_BLUE,
    fontName='Helvetica-Bold', alignment=TA_LEFT, leading=10)
TC_SM        = make_style('TCSM', fontSize=6.5, textColor=colors.HexColor('#374151'),
    fontName='Helvetica', alignment=TA_LEFT, leading=9.5, wordWrap='CJK')
TC_C         = make_style('TCC', fontSize=6.8, textColor=colors.HexColor('#111827'),
    fontName='Helvetica', alignment=TA_CENTER, leading=9.5, wordWrap='CJK')

# ── Helpers ───────────────────────────────────────────────────────────────────
def hr(color=BORDER_GRAY, thick=0.5, sb=4, sa=4):
    return HRFlowable(width='100%', thickness=thick, color=color,
                      spaceAfter=sa, spaceBefore=sb)

def sec(title, n=None):
    label = f"{n}. {title}" if n else title
    return [hr(MID_BLUE, 1.5, 12, 2), Paragraph(label, SEC_TITLE),
            hr(BORDER_GRAY, 0.3, 0, 6)]

def sub(text):
    return Paragraph(text, SUBSEC)

def p(text, style=BODY):
    return Paragraph(text, style)

def bullets(items):
    return [Paragraph(f"• {i}", BULLET_S) for i in items]

def sp(h=0.3):
    return Spacer(1, h*cm)

def cell(text, style=TC):
    return Paragraph(text, style)

def make_table(headers, rows, widths, alt=True, small=False, head_color=TABLE_HEAD):
    cs = TC_SM if small else TC
    h_row = [cell(h, TH) for h in headers]
    data = [h_row]
    for i, row in enumerate(rows):
        r = []
        for j, v in enumerate(row):
            if isinstance(v, tuple):
                r.append(cell(v[0], v[1]))
            else:
                r.append(cell(str(v), cs))
        data.append(r)
    ts = [
        ('BACKGROUND', (0,0), (-1,0), head_color),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER_GRAY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.white, TABLE_ALT] if alt else [colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]
    return Table(data, colWidths=widths, style=TableStyle(ts),
                 repeatRows=1, hAlign='LEFT')

# ── Numeração de páginas ───────────────────────────────────────────────────────
class DocWithFooter(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        self.report_date = "Maio/2026"

    def handle_pageEnd(self):
        BaseDocTemplate.handle_pageEnd(self)

def _page_template(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(ACCENT_GRAY)
        canvas.drawString(2*cm, 1.2*cm,
            "RADAR ESTRATÉGICO — INFRAESTRUTURA COMBUSTÍVEIS | CONFIDENCIAL | Maio/2026")
        canvas.drawRightString(W - 2*cm, 1.2*cm, f"Página {doc.page}")
        canvas.setStrokeColor(BORDER_GRAY)
        canvas.setLineWidth(0.3)
        canvas.line(2*cm, 1.5*cm, W-2*cm, 1.5*cm)
    canvas.restoreState()

# ── CAPA ──────────────────────────────────────────────────────────────────────
def cover_page():
    story = []
    # Fundo azul escuro simulado com tabela
    cov = Table([['']], colWidths=[W - 4*cm], rowHeights=[3.5*cm])
    cov.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(sp(0.5))
    story.append(Paragraph("RADAR ESTRATÉGICO DE INFRAESTRUTURA", COVER_TITLE))
    story.append(Paragraph("COMBUSTÍVEIS LÍQUIDOS NO BRASIL — 2021–2046", COVER_TITLE))
    story.append(sp(0.3))
    story.append(Paragraph(
        "Análise estratégica para distribuidoras nacionais | Infraestrutura como variável competitiva",
        COVER_SUB))
    story.append(sp(0.2))
    story.append(hr(colors.HexColor('#3B82F6'), 1, 4, 8))
    story.append(Paragraph(
        "Elaborado com base em fontes públicas: ANP · ANTT · ANTAQ · Ministério dos Transportes · "
        "EPE · BNDES · PPI · comunicados de empresas · imprensa especializada",
        COVER_META))
    story.append(sp(0.3))
    story.append(Paragraph(
        f"Data de referência: Maio/2026  |  Horizonte de análise: 2021–2046  |  "
        "Uso interno — documento estratégico",
        COVER_TAG))
    story.append(PageBreak())
    return story

# ── BLOCO 1 — SUMÁRIO EXECUTIVO ───────────────────────────────────────────────
def bloco1():
    story = []
    story += sec("SUMÁRIO EXECUTIVO", "1")
    story.append(p(
        "Os próximos 10 anos representam uma janela de reconfiguração profunda da "
        "infraestrutura logística de combustíveis no Brasil. A combinação de novos "
        "terminais ferroviários, expansão acelerada de etanol de milho, aumento de "
        "mandato de biodiesel e surgimento de novos operadores logísticos privatiza "
        "e descentraliza o acesso à cadeia de suprimento. Distribuidoras que não "
        "monitorarem ativamente esses movimentos correm risco de dependência crescente "
        "de infraestrutura de terceiros e perda de margem em rotas onde hoje operam "
        "com vantagem de acesso.", BODY))
    story.append(sp(0.2))

    bullets_exec = [
        "<b>Últimos 5 anos — o que mudou o mercado:</b> "
        "Inauguração do terminal Raízen+Vibra em Santarém/PA (abr/2024, R$350mi, 2bi L/ano) "
        "criou o principal hub Arco Norte; Ultracargo Palmeirante/TO (set/2025, R$160mi) "
        "deslocou Porto Nacional como referência logística do MATOPIBA; INPASA Balsas/MA "
        "(ago/2025, R$2,5bi) tornou o Nordeste produtor de etanol de milho pela 1ª vez.",

        "<b>Próximos 10 anos — maior reconfiguração:</b> "
        "Transnordestina (fase 1 Piauí-Ceará ~2027) + TEMAPE Teresina (2028) criarão "
        "corredor ferroviário para combustíveis no PI/CE. Granel Química Santa Helena/GO "
        "(conclusão 2026) conecta GO ao corredor Norte-Sul com tancagem de biocombustíveis. "
        "FMT/Rumo (162km operacional 2H/2026) inicia a integração ferroviária do MT interior.",

        "<b>Produção de etanol de milho:</b> saltou de ~3bi L (2020) para 10bi L (2025) "
        "e deve atingir 11,5bi L (2026). Novas plantas INPASA (LEM/BA, Rondonópolis/MT), "
        "FS Campo Novo/MT e CerradinhoBio/Neomille (GO) ampliam oferta mas também "
        "concentram poder de precificação nos produtores.",

        "<b>Biodiesel — pressão estrutural crescente:</b> B15 em vigor jan/2026; B20 "
        "previsto 2030; B25 em 2035. Capacidade instalada nacional: 42.600 m³/dia. "
        "Centro-Oeste+Sul controlam >70% da produção. Distribuidoras precisam garantir "
        "acesso à mistura biodiesel em regiões onde a oferta local é escassa.",

        "<b>Pecém/CE — hub multivetorial:</b> Parque de Tancagem (R$430mi, inauguração "
        "ago/2027) + GLP (R$1bi+, fusão Ultragaz+Supergasbras) + Hub H2V (Stolthaven, "
        "$135mi USD) + Transnordestina chegando no porto. Pecém deve se tornar o mais "
        "relevante terminal primário do Nordeste para múltiplos produtos.",

        "<b>FIOL — risco BA:</b> FIOL 1 (Ilhéus-Caetité) paralisada desde mar/2025 "
        "(Bamin/Cazaquistão inadimplente). FIOL 2 em obras com leilão de concessão "
        "previsto ago/2026. Bahia MATOPIBA segue sem conectividade ferroviária plena "
        "por pelo menos mais 5 anos — janela de vulnerabilidade logística.",

        "<b>Ferrovia Açailândia-Barcarena (535km):</b> leilão previsto 2026. Quando "
        "operacional (~2032+), criará corredor independente da Carajás (Vale) para "
        "Vila do Conde/PA — abre nova rota de cabotagem de combustíveis Norte.",

        "<b>Miritituba-Santarém-Barcarena:</b> corredor hidroviário consolida-se como "
        "rota de retorno — derivados chegam via cabotagem/Itaqui, voltam biocombustíveis "
        "MT para Belém/PA e Norte. Volume de combustíveis no Tapajós cresce 40% em 2025.",

        "<b>SAF/BioQAV e HVO (diesel renovável):</b> RPBC Cubatão — Petrobras inicia "
        "licitação 2H/2026; obras fim 2026; operação 2029+. 16.000 bpd de capacidade "
        "(BioQAV+HVO). Novo produto que disputará espaço logístico com diesel fóssil.",

        "<b>Santos STS08 bloqueado:</b> maior licitação de granéis líquidos do país "
        "(Santos/SP) suspensa pelo TCU desde ago/2025. Congela nova tancagem primária "
        "no maior porto nacional — pressiona distribuidoras que dependem de Cubatão/Santos.",

        "<b>Concentração logística crescente:</b> Ultracargo, Raízen, Vibra e VLI "
        "controlam crescente fatia dos terminais primários nos eixos MATOPIBA, Arco Norte "
        "e Nordeste. Risco de dependência estrutural para distribuidoras regionais que "
        "não têm tancagem própria ou acordos de pool.",

        "<b>Eletrificação — impacto assimétrico:</b> EPE projeta 3,7mi EVs até 2035 "
        "(23% dos novos emplacamentos leve). Gasolina/etanol A: impacto em 10-15 anos. "
        "Diesel para cargas rodoviárias: praticamente imune até 2040+. Biodiesel e "
        "etanol para aviação (SAF): crescimento, não queda.",

        "<b>Ganham poder logístico:</b> operadores de terminais independentes (Ultracargo, "
        "Granel Química, Blue Terminals, TEMAPE), produtores verticalizados (INPASA, FS), "
        "ferrovias (VLI, Rumo) que integram oferta+logística+distribuição.",

        "<b>Regiões que ganham competitividade:</b> MATOPIBA (MA/TO/PI), "
        "Centro-Oeste MT/GO (etanol milho), Ceará (hub Pecém), Norte PA (Arco Norte). "
        "<b>Regiões em risco:</b> interior BA (FIOL 1 paralisada), Piauí interior "
        "(até Transnordestina/TEMAPE operacionais ~2028), MT sul (até FMT Rumo ~2030).",

        "<b>Oportunidade estratégica imediata:</b> distribuidoras com presença no eixo "
        "Palmeirante–Balsas–Teresina podem estruturar pools de tancagem antes que "
        "operadores maiores consolidem posição. Janela de 2-3 anos antes da chegada "
        "plena da Transnordestina e maturação de TEMAPE.",
    ]
    for b in bullets_exec:
        story.append(Paragraph(f"▸  {b}", BULLET_S))
        story.append(sp(0.15))

    story.append(PageBreak())
    return story

# ── BLOCO 2 — LINHA DO TEMPO ──────────────────────────────────────────────────
def bloco2():
    story = []
    story += sec("LINHA DO TEMPO DOS PROJETOS", "2")
    story.append(p(
        "Tabela organizada por horizonte temporal. Status: ✅ Operacional | 🔨 Em obras | "
        "📋 Licitado/Autorizado | 📢 Anunciado | 🔬 Em estudo | ⚠️ Incerto.", BODY))
    story.append(sp(0.2))

    hdrs = ["Horizonte", "Projeto / Ativo", "Local", "Tipo", "Status",
            "Players", "Capacidade", "Impacto Estratégico"]
    widths = [1.8*cm, 3.5*cm, 2.2*cm, 2.0*cm, 1.5*cm, 2.5*cm, 2.0*cm, 4.5*cm]

    rows = [
        # ÚLTIMOS 5 ANOS
        ("Últ. 5 anos", "Raízen+Vibra — Base Santarém", "Santarém/PA",
         "Terminal liquid.", "✅ Oper.", "Raízen, Vibra",
         "120mi L armaz.\n2bi L/ano mov.",
         "Hub Arco Norte. Navio → balsas AM/PA/MT norte. Principal primário do Norte."),
        ("Últ. 5 anos", "Ultracargo — Terminal Palmeirante", "Palmeirante/TO",
         "Terminal rodo-ferrov.", "✅ Oper. set/25",
         "Ultracargo (Grupo Ultra)", "23.000 m³ (13 tanques)",
         "Substitui Porto Nacional para 35% MATOPIBA. Diesel+gasolina+etanol. VLI→Itaqui."),
        ("Últ. 5 anos", "INPASA Balsas — Biorrefinaria", "Balsas/MA",
         "Usina+terminal etanol", "✅ Oper. ago/25",
         "INPASA", "925mi L/ano etanol\n2mi ton milho",
         "Maior biorrefinaria etanol milho AL. Nordeste vira produtor. Novo ponto captação."),
        ("Últ. 5 anos", "VLI — Expansão T.P. São Luís", "São Luís/MA",
         "Terminal portuário", "✅ Oper.",
         "VLI Logística", "R$ 80mi invest.",
         "Reforça Itaqui como hub primário Nordeste/Norte. Modal ferroviário consolidado."),
        ("Últ. 5 anos", "Granel Química — Terminal Santos", "Santos/SP",
         "Terminal liquid.", "✅ Oper.",
         "Granel Química (Odfjell)", "Não identificado pub.",
         "Terminal existente reforça posição sudeste. Base de referência SP/SP."),
        ("Últ. 5 anos", "Transnordestina — Operação Parcial", "PI→CE",
         "Ferrovia", "✅ Parcial dez/25",
         "FTL, Transnordestina", "79% fase 1 conc.",
         "Milho, sorgo, calcário já em trânsito. Infraestrutura base para TEMAPE Teresina."),
        ("Últ. 5 anos", "TEMAPE — Aprovação ANTT Teresina", "Teresina/PI",
         "Terminal ferrov.", "📋 Aprov. mar/25",
         "TEMAPE (Terminais Marítimos de Pernambuco)", "27.000 m³, 15 plat. ferrov.",
         "1º contrato Investidor Associado Brasil. Transformará logística PI/CE interior."),
        ("Últ. 5 anos", "CerradinhoBio/Neomille — Expansão", "Chapadão Céu/GO",
         "Usina etanol milho", "📢 Anunc. R$140mi",
         "CerradinhoBio", "+30% → 1,2mi ton/ano",
         "Mais etanol milho em GO/MS. Oportunidade compra adicional ponto captação GO."),
        ("Últ. 5 anos", "Pecém — Pedra Fundamental Tancagem", "São Gonçalo/CE",
         "Parque de tancagem", "🔨 Em obras fev/25",
         "Consórcio privado (BNB R$343mi)", "R$ 430mi total",
         "Inaugura ago/2027. Posicionará Pecém como hub primário múltiplo NE."),

        # PRÓXIMOS 10 ANOS
        ("Próx. 10 anos", "Pecém — Parque de Tancagem Combustíveis", "São Gonçalo/CE",
         "Terminal liquid.", "🔨 Obras → ago/27",
         "Consórcio privado; CIPP S.A.", "R$ 430mi (BNB R$343mi)",
         "Hub primário NE multiproduto. Conexão com Transnordestina e H2V. Alta prioridade monit."),
        ("Próx. 10 anos", "Transnordestina — Conclusão Fase 1", "Paes Landim/PI→Pecém/CE",
         "Ferrovia", "🔨 80% exec. → 2027",
         "FTL, Ministério Transp., BNDES", "527km fase 1; R$1,7bi desemb. 2025",
         "Liga PI ao porto Pecém. Viabiliza TEMAPE. Redefine custo logístico NE."),
        ("Próx. 10 anos", "TEMAPE — Terminal Ferrov. Teresina", "Teresina/PI",
         "Terminal ferrov.", "📋 Obras 2025→op. 2028",
         "TEMAPE, FTL (Transnordestina)", "27.000 m³, 140.000 ton/ano",
         "Primeiro terminal ferroviário PI. Novo primário regional. Ameaça bases São Luís/Fortaleza."),
        ("Próx. 10 anos", "Granel Química — Santa Helena/GO", "Santa Helena/GO",
         "Terminal rodo-ferrov.", "🔨 Obras → fin.2025/2026",
         "Granel Química (Odfjell)", "36mi L (6 tanques × 6mi L), 1mi ton/ano",
         "Novo hub GO sudoeste. Biocombustíveis+combustíveis+químicos. Norte-Sul integrado."),
        ("Próx. 10 anos", "INPASA — Luís Eduardo Magalhães/BA", "LEM/BA",
         "Usina etanol milho", "🔨 Em obras → 3T/2026",
         "INPASA", "~R$ 2bi; capac. similar Balsas",
         "Etanol milho no MATOPIBA baiano. Novo ponto captação BA. Compra direta na usina."),
        ("Próx. 10 anos", "FS Bioenergia — Campo Novo Parecis/MT", "Campo Novo/MT",
         "Usina etanol milho", "🔨 Em obras → dez/2026",
         "FS Bioenergia", "~1bi L adicionais",
         "MT consolida polo etanol milho. Nova oferta para distribuidoras MT/RO/PA."),
        ("Próx. 10 anos", "INPASA — Nova Mutum/MT (expansão)", "Nova Mutum/MT",
         "Usina etanol milho", "🔨 Em obras → nov/2026",
         "INPASA", "Expansão existente",
         "Mais volume etanol milho MT disponível para compra no centro do estado."),
        ("Próx. 10 anos", "INPASA — Rondonópolis/MT (nova planta)", "Rondonópolis/MT",
         "Usina etanol milho", "📢 Anunc. → 1T/2027",
         "INPASA", "Parte do ciclo R$3,5bi",
         "Posiciona Rondonópolis como hub etanol MT sul. Integra com FMT/Rumo futura."),
        ("Próx. 10 anos", "RRP Energia — Tapurah/MT", "Tapurah/MT",
         "Usina etanol milho", "📋 BNDES R$1bi aprov.",
         "RRP Energia, BNDES", "459mi L etanol/ano\n1mi ton milho/ano",
         "Novo produtor independente MT. Mais oferta, mais barganha para distribuidoras."),
        ("Próx. 10 anos", "Ferrovia Estadual MT (Rumo/FMT) — trecho 1", "Rondonópolis→BR-070/MT",
         "Ferrovia", "🔨 Em obras → 2H/2026",
         "Rumo S.A., BNDES R$2bi", "162km; 10mi ton/ano",
         "Integração modal MT sul. Base para corredor multimodal combustíveis MT→Santos."),
        ("Próx. 10 anos", "FMT/Rumo — chegada Lucas do Rio Verde", "Lucas do Rio Verde/MT",
         "Ferrovia", "📢 Previsto ~2030",
         "Rumo S.A.", "743km total",
         "Transforma Lucas RV em hub multimodal. Conecta maior produtor etanol milho MT."),
        ("Próx. 10 anos", "FIOL 2 — Leilão Concessão", "Caetité→LEM/Barreiras/BA",
         "Ferrovia", "📋 Leilão ago/2026",
         "Min. Transportes, futura concess.", "~500km; R$507mi invest. parcial",
         "Se executada, liga BA ao corredor ferroviário MT. Viabiliza logística MATOPIBA BA."),
        ("Próx. 10 anos", "Ferrovia Açailândia-Barcarena", "Açailândia/MA→Barcarena/PA",
         "Ferrovia", "📋 Leilão previsto 2026",
         "Ministério Transportes", "535km; R$8,5bi/ano potenc.",
         "Corredor independente da Vale/Carajás. Nova rota combustíveis PA/MA via Vila do Conde."),
        ("Próx. 10 anos", "Blue Terminals — TGL Vila Velha/ES", "Vila Velha/ES",
         "Terminal liquid.", "📢 Anunc. → 2H/2027",
         "Blue Terminals", "R$340mi; 16 tanques (10+6)",
         "Novo primário ES/SE. Telemetria, sistemas antivazamento. Alternativa ao Rio/Santos."),
        ("Próx. 10 anos", "RPBC — BioQAV + HVO (Petrobras)", "Cubatão/SP",
         "Planta refino renovável", "📢 Licit. 2H/2026 → op. 2029+",
         "Petrobras", "16.000 bpd (BioQAV + diesel renovável)\n950k ton/ano matéria-prima",
         "SAF+HVO no SP. Novo produto logístico (diesel renovável) em escala nacional 2029+."),
        ("Próx. 10 anos", "Biodiesel B20 — Mandato 2030", "Nacional",
         "Mandato mistura", "📋 Previsto lei",
         "ANP, MAPA", "Demanda ~12mi ton/ano estimada",
         "Pressão adicional sobre infraestrutura de armazenagem mistura. Distribuidoras precisam tanques B100."),
        ("Próx. 10 anos", "Pecém — Hub H2V (Stolthaven/GES)", "São Gonçalo/CE",
         "Terminal amônia/H2V", "📋 Pré-contrato renov. jun/25",
         "Stolthaven, GES, CIPP", "$135mi USD (Banco Mundial+CIF)",
         "Posiciona Pecém como 1º hub H2V Brasil. Corredor dutos 2028+. Produto do futuro."),

        # PRÓXIMOS 20 ANOS
        ("Próx. 20 anos", "FIOL 3 — Barreiras→Mara Rosa/GO", "BA→GO",
         "Ferrovia", "🔬 Em estudo",
         "Depende FIOL 2", "Extensão FIOL 2 →GO",
         "Fecha corredor BA-GO-MT. Redefiniria logística MATOPIBA completo se executado."),
        ("Próx. 20 anos", "Mandato E35 e E30 consolidado", "Nacional",
         "Mandato biocombustível", "🔬 E30 vigente 2026",
         "MAPA, MME, ANP", "Projeção etanol milho 18-20bi L/2030",
         "Etanol como produto central da mistura gasolina. Oportunidade ou ameaça por captação."),
        ("Próx. 20 anos", "Biodiesel B25 — Mandato 2035", "Nacional",
         "Mandato mistura", "🔬 Lei prevista",
         "ANP, MAPA", "~13-15mi ton/ano estimado",
         "Mercado biodiesel quase dobra vs. B12. Infraestrutura armazenagem B100 vira crítica."),
        ("Próx. 20 anos", "Eletrificação Frota Leve — Impacto Gasolina", "Nacional",
         "Tendência mercado", "🔬 EPE: 3,7mi EVs 2035",
         "EPE (cenário base)", "23% novos emplacam. 2035",
         "Redução gradual gasolina/etanol carro. Diesel/biodiesel seguro até 2040. SAF cresce."),
        ("Próx. 20 anos", "HVO / Diesel Verde em escala", "Nacional",
         "Produto novo", "🔬 RPBC start 2029",
         "Petrobras, mercado privado", "16.000 bpd start",
         "Diesel renovável compete com fóssil. Distribuidoras precisam de nova logística de produto."),
        ("Próx. 20 anos", "Interiorização etanol milho — Norte/NE", "MA, TO, PA, BA",
         "Expansão industrial", "📢 INPASA já iniciou",
         "INPASA, futuros entrantes", "Produção NE+Norte crescente",
         "Etanol deixa de ser 'produto do Sul/CO'. Lógica de abastecimento regional muda."),
    ]

    story.append(make_table(hdrs, rows, widths, small=True))
    story.append(sp(0.2))
    story.append(p(
        "Fontes: ANP, ANTT, ANTAQ, Ministério dos Transportes, BNDES, PPI, Petrobras, CIPP S.A., "
        "VLI Logística, Ultracargo, Raízen, INPASA, FS Bioenergia, Granel Química, TEMAPE, "
        "NovaCana, PortoseNavios, CPG Click Petróleo e Gás, BrazilJournal, Agência Gov, "
        "Gov.br Transportes, AgênciaInfra, NoticiasAgricolas. Mai/2026.", NOTE_S))
    story.append(PageBreak())
    return story

# ── BLOCO 3 — MAPA ESTRATÉGICO POR REGIÃO ─────────────────────────────────────
def bloco3():
    story = []
    story += sec("MAPA ESTRATÉGICO POR REGIÃO", "3")
    story.append(p(
        "Análise das mudanças logísticas e competitivas por macrorregião, com foco em "
        "impactos reais sobre acesso a produto, custo logístico e poder de barganha "
        "das distribuidoras.", BODY))
    story.append(sp(0.2))

    hdrs = ["Estado/Região", "Projetos Relevantes", "Produto\nImpactado",
            "Mudança Logística Esperada", "Players Beneficiados",
            "Riscos", "Oportunidades para Distribuidora"]
    widths = [1.8*cm, 3.5*cm, 1.5*cm, 3.5*cm, 2.5*cm, 2.5*cm, 3.7*cm]

    rows = [
        ("MARANHÃO (MA)", "INPASA Balsas (✅ ago/25)\nVLI São Luís R$80mi\nFerr. Açailândia-Barcarena (leilão 2026)",
         "Etanol milho\nDiesel S10", "Nordeste vira produtor de etanol milho. Balsas como polo. Futuro corredor ferrov. MA-PA independente da Vale.",
         "INPASA, VLI, Ultracargo", "INPASA com poder de precificação na usina. Concentração logística VLI.",
         "Compra etanol diretamente na INPASA Balsas. Pool tancagem em São Luís antes da consolidação."),
        ("PIAUÍ (PI)", "TEMAPE Teresina (aprovado ANTT mar/25, op. 2028)\nTransnordestina (op. parcial dez/25, fase 1 ~2027)",
         "Diesel\nGasolina\nEtanol", "Terminal ferroviário primário em Teresina muda completamente a lógica de abastecimento. PI deixa de depender de rodovias longas.",
         "TEMAPE, FTL, Raízen, Vibra", "Dependência de TEMAPE como operador único até 2028+. FTL como controladora do ramal.",
         "Parceria ou arrendamento de tancagem no TEMAPE antes da operação plena. Posicionamento antecipado em Teresina."),
        ("CEARÁ (CE)", "Pecém Tancagem (🔨 obras, aug/2027)\nTransnordestina chegando\nPecém Hub H2V",
         "Diesel\nGasolina\nEtanol\nBiodiesel\nGLP", "Pecém se torna hub multiproduto NE. Primeiro terminal ferroviário integrado ao porto do CE.",
         "Consórcio Pecém, Ultragaz+Supergasbras, Stolthaven", "Concentração no CIPP. Novos players de H2V podem disputar espaço portuário.",
         "Presença antecipada no parque de tancagem. Acordos de pool com operadores do Pecém."),
        ("BAHIA (BA)", "INPASA LEM/BA (🔨 → 3T/2026)\nFIOL 2 (leilão ago/26)\nFIOL 1 PARALISADA",
         "Etanol milho\nDiesel", "INPASA LEM cria ponto de captação BA. FIOL 1 paralisada deixa BA sem ferrovia oeste por anos.",
         "INPASA, futuro concessionário FIOL", "Risco: BA MATOPIBA isolada logisticamente por 5+ anos sem FIOL 1. Custo rodoviário alto.",
         "Compra antecipada etanol milho da INPASA LEM. Monitorar concessão FIOL 2."),
        ("TOCANTINS (TO)", "Ultracargo Palmeirante (✅ set/25)\nFMT/Rumo sul MT (indir.)\nVLI Norte-Sul",
         "Diesel S10\nGasolina\nEtanol", "Palmeirante substitui Porto Nacional para 35% região. Hub rodo-ferroviário consolidado com VLI.",
         "Ultracargo, VLI", "Dependência do Ultracargo como único terminal rodo-ferroviário na região.",
         "Negociar condições pool/tancagem com Ultracargo. Porto Nacional pode ter espaço residual."),
        ("PARÁ (PA)", "Raízen+Vibra Santarém (✅ abr/24)\nMiritituba crescendo\nFerr. Açailândia-Barcarena (leilão 2026)\nBarcarena — porto",
         "Diesel\nEtanol\nBiodiesel", "Santarém como hub Arco Norte. Miritituba cresce (biocomb. MT→PA). Futuro corredor ferrov. PA independente.",
         "Raízen, Vibra, Hidrovias do Brasil, CDP", "Raízen+Vibra controlam o maior terminal PA. Dependência dual.",
         "Pool com Raízen ou Vibra em Santarém. Monitorar novos arrendamentos CDP."),
        ("MATO GROSSO (MT)", "FS Campo Novo (→ dez/26)\nINPASA Nova Mutum (→ nov/26)\nINPASA Rondonópolis (→ 1T/27)\nRRP Tapurah (BNDES)\nFMT/Rumo (162km → 2H/26; Lucas RV 2030)",
         "Etanol milho\nBiodiesel\nDiesel S10", "MT vira o maior polo etanol milho do Brasil. FMT transforma multimodalidade. Lucas RV como futuro hub ferroviário.",
         "INPASA, FS Bioenergia, RRP, Rumo", "Concentração oferta etanol milho em poucos produtores. Poder de precificação nas usinas.",
         "Contratos antecipados de fornecimento etanol milho. Participar da estrutura logística Lucas RV."),
        ("GOIÁS (GO)", "Granel Química Santa Helena (🔨 → 2026)\nCerradinhoBio/Neomille Chapadão Céu (exp. → ago/26)\nAnápolis hub DAIA",
         "Etanol milho\nBiodiesel\nCombustíveis", "Santa Helena abre novo hub rodo-ferroviário GO sudoeste. Mais etanol milho em GO disponível.",
         "Granel Química, CerradinhoBio, IBG", "Granel Química como único operador terminal Santa Helena. Dependência de slot.",
         "Arrendamento espaço no terminal Granel Santa Helena. Acordos diretos CerradinhoBio."),
        ("ESPÍRITO SANTO (ES)", "Blue Terminals TGL Vila Velha (→ 2H/2027)\nPorto de Vitória expansão",
         "Diesel\nGasolina\nEtanol\nBiodiesel", "Novo terminal primário ES. Alternativa ao Santos/RJ para distribuidoras SE e partes MG.",
         "Blue Terminals", "Projeto ainda em fase inicial — risco execução. Até 2027 sem alternativa.",
         "Monitorar processo Blue Terminals. Avaliar posição SE quando inaugurar."),
        ("SÃO PAULO (SP)", "RPBC BioQAV+HVO (→ 2029+)\nSantos STS08 BLOQUEADO TCU",
         "Diesel renovável\nSAF\nDiesel fóssil", "RPBC vai criar diesel renovável (HVO) em escala 2029+. Santos congela novas tancagens enquanto TCU não libera.",
         "Petrobras (RPBC), futuro concessio. STS08", "Santos STS08 bloqueado cria escassez de tancagem primária SP.",
         "Monitorar retomada STS08. Avaliar parcerias em terminais existentes Santos enquanto espera."),
        ("NORDESTE INTERIOR\n(RN,PB,PE,AL,SE)", "Transnordestina (em construção)\nBases existentes Ipiranga/Vibra/Raízen",
         "Diesel S10\nGasolina", "Transnordestina quando pronta muda custo logístico de quase todos os estados NE.",
         "FTL, Raízen, Vibra, Ipiranga", "FTL com poder sobre frete ferroviário NE.",
         "Mapear rotas impactadas pela Transnordestina antes da operação plena."),
    ]

    story.append(make_table(hdrs, rows, widths, small=True))
    story.append(sp(0.3))
    story.append(PageBreak())
    return story

# ── BLOCO 4 — IMPLICAÇÕES PARA DISTRIBUIDORAS ─────────────────────────────────
def bloco4():
    story = []
    story += sec("ANÁLISE DE IMPLICAÇÕES PARA DISTRIBUIDORAS", "4")
    story.append(p(
        "Esta seção trata infraestrutura como variável competitiva. O objetivo não é "
        "listar obras, mas avaliar como cada mudança reposiciona o poder de barganha, "
        "o custo logístico e o acesso a produto das distribuidoras que operam nos "
        "mercados impactados.", BODY))

    # Alta prioridade
    story.append(sp(0.2))
    story.append(sub("4.1  Projetos de ALTA PRIORIDADE"))
    story.append(p(
        "Critérios: alta probabilidade de execução, impacto direto em custo ou acesso a produto, "
        "horizonte de 1 a 5 anos, risco de concentração logística ou exclusão de corredor.", BODY))

    hdrs_pr = ["Projeto", "Por que Alta Prioridade", "Risco Concreto", "Recomendação"]
    widths_pr = [3.5*cm, 5.5*cm, 4.0*cm, 5.0*cm]
    rows_pr = [
        ("Ultracargo Palmeirante/TO\n(✅ Operacional set/25)",
         "Já opera. Cobre 35% do MATOPIBA. Elimina Porto Nacional como referência. VLI integrado.",
         "Distribuidoras sem posição no Palmeirante pagam mais por frete rodoviário ou dependem do Ultracargo como único terminal.",
         "Negociar imediatamente acordos de pool ou tancagem com Ultracargo. Avaliar impacto em bases Porto Nacional."),
        ("INPASA Balsas/MA\n(✅ Operacional ago/25)",
         "Maior biorrefinaria etanol milho AL. Nova oferta no Nordeste. Preço competitivo vs. Centro-Oeste.",
         "Distribuidoras sem contrato direto com INPASA pagam prêmio ou compram via intermediários.",
         "Buscar contrato de fornecimento direto com INPASA Balsas. Avaliar custo logístico MA vs. CO."),
        ("Granel Química Santa Helena/GO\n(🔨 → conclusão 2026)",
         "Terminal rodo-ferroviário GO sudoeste. Norte-Sul integrado. 8º terminal Odfjell no Brasil. Confiabilidade operacional alta.",
         "Distribuidoras GO/BA que não tiverem acesso ao terminal dependem de Goiânia e Anápolis, com custo logístico maior.",
         "Avaliar cessão de espaço ou arrendamento de tancagem no terminal Santa Helena."),
        ("Pecém Parque Tancagem/CE\n(🔨 obras → ago/2027)",
         "Hub multiproduto CE com Transnordestina chegando. R$430mi de capacidade nova. BNB como financiador.",
         "Se não houver posição no Pecém, distribuidoras CE terão que comprar de quem tiver acesso ao terminal.",
         "Monitorar estrutura de acesso. Contato com CIPP S.A. para avaliar modalidade de uso. Alta urgência."),
        ("TEMAPE Teresina/PI\n(📋 Autorizado → op. 2028)",
         "Único terminal ferroviário PI. Produto vem pela Transnordestina. ANTT já aprovou.",
         "TEMAPE potencialmente monopolista em Teresina até 2028+. Distribuidoras sem posição pagam tarifa cheia.",
         "Avaliar parceria antecipada com TEMAPE. Explorar modalidade de cessão de tancagem."),
        ("Transnordestina (fase 1 ~2027)\n(🔨 79% executada)",
         "Liga PI ao Porto Pecém por ferrovia. Operação parcial já dez/2025 (grãos). Diesel virá em seguida.",
         "Quando plenamente operacional, muda o custo logístico de todo o NE. Distribuidoras fora do corredor perdem.",
         "Mapear quais bases e clientes serão impactados pela rota ferroviária. Renegociar contratos de frete preventivamente."),
    ]
    story.append(make_table(hdrs_pr, rows_pr, widths_pr, small=True))
    story.append(sp(0.3))

    # Média prioridade
    story.append(sub("4.2  Projetos de MÉDIA PRIORIDADE"))
    story.append(p(
        "Critérios: execução provável mas com incerteza de prazo, impacto em 5-10 anos, "
        "ou impacto regional mais limitado.", BODY))

    rows_med = [
        ("INPASA LEM/BA (→ 3T/2026)\nFS Campo Novo/MT (→ dez/2026)",
         "Novas fontes de etanol milho BA e MT. Ampliam oferta e potencialmente reduzem preços de compra.",
         "Poder de precificação concentrado nos produtores.",
         "Contratos antecipados de fornecimento. Avaliar custo de retirada."),
        ("FMT/Rumo — 162km (→ 2H/2026)\nLucas RV 2030",
         "Integração modal MT. Transformará logística do Centro-Oeste em 5-10 anos.",
         "Lucas RV hoje sem ferrovia. Distribuidoras dependem de rodovia.",
         "Monitorar evolução das obras e planejar posição logística em Lucas RV."),
        ("FIOL 2 — Leilão ago/2026",
         "Se licitada e executada, liga BA ao corredor ferroviário nacional.",
         "Prazo incerto. FIOL 1 paralisada cria risco histórico de não execução.",
         "Monitorar resultado do leilão. Baixo investimento de atenção por ora."),
        ("Blue Terminals — Vila Velha/ES (→ 2H/2027)",
         "Novo terminal primário ES. Alternativa ao Santos para SE.",
         "Risco de execução. Prazo até 2027 sem alternativa.",
         "Acompanhar licenciamento. Avaliar posição ES quando mais claro."),
        ("Raízen+Vibra Santarém/PA\n(✅ Operacional abr/24)",
         "Pool Raízen+Vibra no Arco Norte. Novo modelo de operação conjunta.",
         "Dois grandes players dividem o primário PA. Poder sobre distribuidoras regionais.",
         "Avaliar custo de operar pelo pool vs. posição própria em Santarém."),
        ("Ferrovia Açailândia-Barcarena\n(leilão 2026)",
         "Corredor alternativo ao EFC/Vale para PA. 535km de nova conectividade.",
         "Prazo longo (pós-2030). Alta incerteza regulatória.",
         "Monitorar resultado do leilão. Potencial de longo prazo para abastecimento PA."),
    ]
    story.append(make_table(hdrs_pr, rows_med, widths_pr, small=True))
    story.append(sp(0.3))

    # Baixa prioridade
    story.append(sub("4.3  Projetos de BAIXA PRIORIDADE (monitorar, não agir agora)"))
    rows_bx = [
        ("RPBC BioQAV+HVO (→ 2029+)", "Operação pós-2029. Produto novo (HVO) requer nova logística.", "Monitorar evolução. Avaliar quando produto estiver disponível."),
        ("Pecém Hub H2V / Amônia Verde", "Produto de longo prazo. Não afeta cadeia combustíveis nos próximos 10 anos diretamente.", "Apenas monitorar. Relevante pós-2035."),
        ("Santos STS08 — Bloqueado TCU", "Maior licitação paralisada. Sem prazo de retomada.", "Monitorar TCU. Pode surgir oportunidade se desbloqueado."),
        ("FIOL 3 (Barreiras→Mara Rosa/GO)", "Dependente de FIOL 2. Horizonte 20 anos.", "Baixíssima materialidade atual."),
        ("Biodiesel B25 / 2035", "10 anos. Impacto estrutural na armazenagem de B100.", "Incluir no planejamento de longo prazo de tancagem."),
    ]
    hdrs_bx = ["Projeto", "Por que Baixa Prioridade", "Recomendação"]
    widths_bx = [3.5*cm, 7.0*cm, 7.5*cm]
    story.append(make_table(hdrs_bx, rows_bx, widths_bx, small=True))

    story.append(sp(0.3))
    story.append(sub("4.4  Análise Temática — Temas Transversais"))
    story.append(sp(0.1))

    temas = [
        ("<b>Dependência de terminais de terceiros:</b> "
         "Distribuidoras que não têm tancagem primária própria ou contratos de pool "
         "em terminais como Palmeirante, Pecém, Santarém e Santa Helena/GO correm risco "
         "crescente de dependência de preço e disponibilidade. O modelo de 'comprar e retirar' "
         "de terminais de grandes players se tornará progressivamente mais caro à medida "
         "que esses operadores consolidam posição."),
        ("<b>Etanol de milho como variável de custo:</b> "
         "Com etanol de milho representando 33% da produção nacional (2025) e crescendo "
         "para ~42% até 2035 (EPE), distribuidoras que não estruturarem acesso direto aos "
         "produtores (INPASA, FS, CerradinhoBio, RRP) perdem margem para quem consegue "
         "comprar na usina. A interiorização da produção (Balsas, LEM, Lucas RV) muda "
         "completamente a lógica geográfica de captação."),
        ("<b>Biodiesel — infraestrutura de mistura:</b> "
         "A progressão B15→B20 (2030)→B25 (2035) exige capacidade de armazenagem de B100 "
         "próxima aos pontos de mistura. Distribuidoras que não tiverem tanques adequados "
         "ou acordos com usinas de biodiesel próximas serão pressionadas em margem."),
        ("<b>Pool logístico como oportunidade:</b> "
         "O modelo Raízen+Vibra em Santarém sinaliza que operações conjuntas de terminal "
         "reduzem custo fixo e ampliam cobertura. Distribuidoras médias poderiam estruturar "
         "pools em regiões onde nenhum player grande está consolidado "
         "(ex: eixo Palmeirante–Porto Nacional, interior PI pré-TEMAPE)."),
        ("<b>Ferrovias como ativo estratégico:</b> "
         "A chegada da Transnordestina, VLI Norte-Sul e FMT/Rumo não é apenas logística "
         "de grãos — é também o canal de combustíveis do futuro. Distribuidoras que "
         "entenderem as rotas ferroviárias como variáveis de custo de frete conseguirão "
         "negociar com mais eficiência tanto a compra como a entrega."),
    ]
    for t in temas:
        story.append(Paragraph(f"▸  {t}", BULLET_S))
        story.append(sp(0.15))

    story.append(PageBreak())
    return story

# ── BLOCO 5 — MATRIZ OPORTUNIDADES E AMEAÇAS ──────────────────────────────────
def bloco5():
    story = []
    story += sec("MATRIZ FINAL DE OPORTUNIDADES E AMEAÇAS", "5")
    story.append(p(
        "Cada linha representa um projeto ou região com avaliação binária de oportunidade "
        "e ameaça, urgência de ação e recomendação prática para a distribuidora.", BODY))
    story.append(sp(0.2))

    hdrs = ["Projeto / Região", "Oportunidade", "Ameaça",
            "Urgência", "Horizonte", "Recomendação"]
    widths = [3.2*cm, 4.0*cm, 3.5*cm, 1.8*cm, 1.8*cm, 4.7*cm]

    rows = [
        ("Ultracargo Palmeirante/TO",
         "Novo ponto primário rodo-ferrov. MATOPIBA. Acesso a diesel+etanol via VLI.",
         "Monopólio de fato regional. Distribuidoras sem posição dependem de frete rodoviário extra.",
         "IMEDIATA", "0–2 anos",
         "Buscar pool ou arrendamento. Renegociar base Porto Nacional."),
        ("INPASA Balsas/MA",
         "Compra direta etanol milho no Nordeste. Preço competitivo vs. Centro-Oeste.",
         "INPASA com poder de precificação. Pode excluir clientes menores.",
         "IMEDIATA", "0–2 anos",
         "Contrato de fornecimento direto INPASA. Avaliar volume mínimo e logística."),
        ("Granel Química Santa Helena/GO",
         "Terminal rodo-ferroviário go sudoeste. Biocombustíveis+combustíveis. Infraestrutura confiável Odfjell.",
         "Granel Química como único operador. Dependência de slot e tarifa.",
         "1–3 anos", "0–3 anos",
         "Avaliar cessão de espaço ou arrendamento. Presença antecipada."),
        ("Pecém Parque Tancagem/CE",
         "Hub multiproduto NE com ferrovia. Oportunidade de pool no CE. Preço importado competitivo.",
         "Concentração no CIPP. Novo operador pode ditar condições de acesso.",
         "1–3 anos", "2027",
         "Contato CIPP S.A. Avaliar modalidade de uso. Estudar presença antes da inauguração."),
        ("TEMAPE Teresina/PI",
         "Primeiro terminal ferroviário PI. Custo logístico menor pós-2028. Produto via Transnordestina.",
         "TEMAPE monopolista em Teresina. FTL controlando ramal.",
         "1–3 anos", "2028",
         "Avaliar parceria ou cessão de tancagem com TEMAPE antecipadamente."),
        ("Transnordestina PI→CE (~2027)",
         "Corredor ferroviário NE. Custo frete diesel PI/CE cai. Abre mercado.",
         "FTL detém poder sobre frete ferroviário NE. Redefine quem é competitivo.",
         "1–3 anos", "2027",
         "Mapear rotas impactadas. Renegociar contratos de frete preventivamente."),
        ("INPASA LEM/BA (→ 3T/2026)",
         "Novo ponto captação etanol milho BA. Reduz custo logístico para distribuidoras BA.",
         "INPASA poder de precificação BA similar a Balsas.",
         "1–3 anos", "2026",
         "Contrato antecipado de fornecimento com INPASA LEM."),
        ("FMT/Rumo MT (trecho 1 → 2H/2026)",
         "Integração modal MT. Custo frete CO cai. Lucas RV futuramente hub multimodal.",
         "Rumo com poder sobre frete MT→Santos.",
         "3–10 anos", "2026→2030",
         "Monitorar evolução. Planejar posição logística Lucas RV para horizonte 2030."),
        ("FIOL 2 — Leilão ago/2026",
         "Se executada, liga BA ao corredor ferroviário. Novo acesso MATOPIBA BA.",
         "Alta incerteza. FIOL 1 paralisada cria precedente de não execução.",
         "3–10 anos", "2026→2032+",
         "Monitorar resultado leilão. Não agir antes de confirmação."),
        ("Ferrovia Açailândia-Barcarena",
         "Corredor alternativo PA independente de Vale/Carajás. Novo acesso Vila do Conde.",
         "Longo prazo. Alta incerteza de prazo.",
         "3–10 anos", "2026→2032+",
         "Monitorar. Potencial relevante para abastecimento PA no longo prazo."),
        ("Raízen+Vibra Santarém/PA",
         "Pool existente. Acesso ao maior hub combustíveis Arco Norte.",
         "Dois grandes players monopolizam primário PA. Termos desfavoráveis.",
         "IMEDIATA", "Atual",
         "Avaliar custo pool vs. alternativa própria. Negociar condições de acesso."),
        ("Blue Terminals Vila Velha/ES",
         "Novo primário ES. Alternativa Santos/RJ para distribuidoras SE.",
         "Risco execução. Sem alternativa até 2027+.",
         "3–10 anos", "2027",
         "Monitorar licenciamento. Avaliar posição ES quando viável."),
        ("RPBC BioQAV+HVO (→ 2029+)",
         "Diesel renovável em escala. Novo produto de alto valor para distribuidoras.",
         "Lógica de produto nova. Infraestrutura de armazenagem precisa adaptação.",
         "3–10 anos", "2029",
         "Incluir no planejamento de produto. Avaliar infraestrutura HVO antecipadamente."),
        ("Etanol de milho — Expansão geral",
         "Mais oferta, mais opções de compra, preços potencialmente mais competitivos.",
         "Concentração em poucos produtores (INPASA, FS) com poder de precificação.",
         "IMEDIATA", "Contínuo",
         "Diversificar fornecedores de etanol milho. Incluir na estratégia de suprimento."),
        ("Biodiesel B15→B20→B25",
         "Volume maior. Margem de mistura. Oportunidade de armazenagem B100.",
         "Pressão de custo de aquisição B100. Infraestrutura de tanques B100 inadequada.",
         "1–3 anos", "2026→2035",
         "Avaliar investimento em tancagem B100 própria ou pool. Acordos com usinas biodiesel."),
        ("Santos STS08 — Bloqueado",
         "Se desbloqueado, nova tancagem primária SP. Oportunidade de posição.",
         "Congela nova tancagem primária SP indefinidamente.",
         "3–10 anos", "Incerto",
         "Monitorar TCU. Se desbloqueado, avaliar participação rapidamente."),
        ("FIOL 1 — BA Interior\n(PARALISADA)",
         "Nenhuma imediata.",
         "BA MATOPIBA isolada logisticamente. Custo rodoviário permanece alto por 5+ anos.",
         "IMEDIATA", "Risco atual",
         "Reavaliar rentabilidade de rotas BA interior. Considerar alternativas rodoviárias."),
        ("Eletrificação Frota Leve",
         "Diesel seguro até 2040+. SAF e HVO como oportunidades.",
         "Gasolina/etanol A leve: redução gradual demanda em 10-15 anos.",
         "10+ anos", "2035+",
         "Monitorar EPE. Incorporar cenários no planejamento de longo prazo de mix de produto."),
    ]

    story.append(make_table(hdrs, rows, widths, small=True))
    story.append(PageBreak())
    return story

# ── BLOCO 6 — 10 PERGUNTAS ESTRATÉGICAS ──────────────────────────────────────
def bloco6():
    story = []
    story += sec("RESPOSTAS ÀS 10 PERGUNTAS ESTRATÉGICAS", "6")
    story.append(sp(0.15))

    perguntas = [
        (
            "1. Quais são os 10 projetos mais relevantes para o mercado de combustíveis líquidos no Brasil?",
            [
                "Ultracargo Palmeirante/TO — redefine logística MATOPIBA já em operação",
                "INPASA Balsas/MA — primeiro produtor etanol milho NE, escala industrial",
                "Raízen+Vibra Santarém/PA — hub Arco Norte, 2bi L/ano",
                "Transnordestina PI→CE — corredor ferroviário NE (op. 2027)",
                "Pecém Parque Tancagem/CE — hub multiproduto NE (ago/2027)",
                "TEMAPE Teresina/PI — primeiro terminal ferroviário PI (2028)",
                "Granel Química Santa Helena/GO — terminal rodo-ferroviário GO (2026)",
                "INPASA LEM/BA — novo polo produção etanol milho MATOPIBA BA (2026)",
                "FMT/Rumo — ferrovia MT (162km 2H/2026; Lucas RV 2030)",
                "RPBC BioQAV+HVO Petrobras — diesel renovável+SAF em escala (2029+)",
            ]
        ),
        (
            "2. Quais projetos podem mudar a competitividade no Norte, Nordeste e Centro-Oeste?",
            [
                "Norte: Raízen+Vibra Santarém (já mudou). Ferrovia Açailândia-Barcarena (futuro). Miritituba crescendo.",
                "Nordeste: Transnordestina + TEMAPE Teresina + Pecém Tancagem = tríade que redefine NE em 3-5 anos.",
                "Centro-Oeste: FMT/Rumo + múltiplas plantas etanol milho MT/GO = novo eixo logístico Central-Oeste 2026-2030.",
                "O eixo MATOPIBA (MA+TO+PI+BA) será o de maior transformação na próxima década.",
            ]
        ),
        (
            "3. Quais projetos estão mais conectados à expansão do etanol de milho?",
            [
                "INPASA Balsas/MA (✅ ago/25) — produtor no Nordeste",
                "INPASA LEM/BA (→ 3T/2026) — produtor no MATOPIBA baiano",
                "FS Campo Novo/MT (→ dez/2026) — expansão polo MT",
                "INPASA Nova Mutum/MT (→ nov/2026) + Rondonópolis (→ 1T/2027)",
                "CerradinhoBio/Neomille Chapadão Céu/GO (→ ago/2026)",
                "RRP Energia Tapurah/MT (BNDES aprovado)",
                "Ultracargo Palmeirante (infraestrutura logística para escoamento)",
                "Transnordestina (futuro corredor milho→etanol→Pecém)",
                "FMT/Rumo (corredor MT produção→porto)",
            ]
        ),
        (
            "4. Quais projetos estão mais conectados ao aumento de biodiesel?",
            [
                "Mandato B15 (jan/2026 — já ativo), B20 (2030), B25 (2035) são o driver primário.",
                "Grupo Potencial Lapa/PR: complexo R$600mi → 1,62bi L/ano biodiesel (obras 2025-2026)",
                "Capacidade instalada nacional: 42.600 m³/dia — Centro-Oeste e Sul >70% da oferta.",
                "Infraestrutura crítica: terminais de armazenagem B100 próximos às bases de mistura.",
                "Risco para distribuidoras: comprar B100 de regiões distantes eleva custo de mistura.",
            ]
        ),
        (
            "5. Quais projetos podem reduzir dependência de infraestrutura tradicional?",
            [
                "TEMAPE Teresina: PI deixa de depender de caminhões-tanque de São Luís ou Fortaleza.",
                "Granel Santa Helena/GO: GO sudoeste tem ponto regional sem precisar de Goiânia.",
                "Ultracargo Palmeirante: MATOPIBA TO/MA tem opção local sem Porto Nacional.",
                "INPASA Balsas e LEM: NE deixa de importar todo etanol do Centro-Oeste.",
                "FMT/Rumo + Lucas RV (2030): MT interior não depende apenas de rodovia BR-163.",
            ]
        ),
        (
            "6. Quais projetos podem aumentar dependência de players específicos?",
            [
                "Ultracargo Palmeirante: único terminal rodo-ferroviário MATOPIBA TO — dependência de preço de tarifa.",
                "Raízen+Vibra Santarém: pool duopólico no PA. Dois players definem acesso ao Arco Norte.",
                "TEMAPE Teresina: primeiro e único terminal ferroviário PI até anos pós-2028.",
                "VLI no corredor Norte-Sul: controla ramal que alimenta Palmeirante e futuro TEMAPE.",
                "INPASA: maior produtor etanol milho com presença em Balsas, Nova Mutum, LEM, Rondonópolis — poder de precificação crescente.",
                "FTL (Transnordestina): controlará frete ferroviário de todo o NE quando concluída.",
            ]
        ),
        (
            "7. Onde podem surgir oportunidades de investimento, pool, parceria ou cessão de espaço?",
            [
                "IMEDIATAS: Palmeirante (pool Ultracargo), Balsas (contrato INPASA), Santarém (negociar pool Raízen+Vibra).",
                "CURTO PRAZO: Santa Helena/GO (cessão Granel Química), Pecém (posição antes de ago/2027).",
                "MÉDIO PRAZO: TEMAPE Teresina (parceria antecipada), Blue Terminals Vila Velha/ES.",
                "LONGO PRAZO: Lucas do Rio Verde MT (hub multimodal 2030), FIOL 2 BA (se aprovada).",
                "Cessão de espaço em bases próprias para produtores de etanol milho em busca de armazenagem regional.",
            ]
        ),
        (
            "8. Quais regiões deveriam estar no radar estratégico imediato?",
            [
                "Tocantins (MATOPIBA) — Palmeirante já opera; Porto Nacional em reposicionamento.",
                "Maranhão — Balsas com INPASA; São Luís como hub portuário; Açailândia hub ferrovia.",
                "Piauí — Teresina pré-TEMAPE; janela de 2 anos antes da chegada ferroviária.",
                "Ceará — Pecém como hub; Transnordestina se aproximando; janela antes de 2027.",
                "Goiás — Santa Helena terminal em conclusão; Anápolis hub DAIA.",
                "Pará — Santarém consolidado; Miritituba crescendo; corredor Arco Norte.",
            ]
        ),
        (
            "9. Quais projetos parecem relevantes mas ainda são incertos?",
            [
                "FIOL 1 (Ilhéus-Caetité/BA): paralisada, sem data de retomada — não contar com ela.",
                "FIOL 2 leilão ago/2026: depende de TCU e ANTT. Histórico de atrasos.",
                "Ferrovia Açailândia-Barcarena: leilão previsto 2026 mas prazo de conclusão é 2032+.",
                "Santos STS08: bloqueado pelo TCU desde ago/2025, sem data de retomada.",
                "FIOL 3 (Barreiras→Mara Rosa/GO): horizonte 20 anos, depende de FIOL 2.",
                "E35 (etanol gasolina): em estudo, sem data de vigência confirmada.",
                "Mandato biodiesel B25 2035: não está ainda formalizado em lei.",
            ]
        ),
        (
            "10. Quais informações ainda precisam de aprofundamento?",
            [
                "Capacidade exata e modalidade de acesso ao Parque de Tancagem do Pecém (operador, tarifa, prazo).",
                "Detalhes operacionais do TEMAPE Teresina: tarifa ferroviária, mix de produtos, quem pode usar o terminal.",
                "Situação contratual real de FIOL 1: processo de rescisão com Bamin, prazo para nova licitação.",
                "Santos STS08: análise do TCU, cronograma de retomada, quem são os candidatos.",
                "Blue Terminals Vila Velha: estado atual do licenciamento ambiental e ANTAQ.",
                "RRP Energia Tapurah: cronograma de obras pós-BNDES e conectividade logística planejada.",
                "Custo real de tarifa de armazenagem nos terminais Ultracargo, Granel Química e TEMAPE.",
                "Expansão de armazenagem biodiesel B100 nas bases existentes das distribuidoras.",
                "Impacto do E30 (vigente jan/2026) na necessidade de tancagem de etanol nas bases.",
            ]
        ),
    ]

    for num, (pergunta, respostas) in enumerate(perguntas):
        story.append(sub(pergunta))
        story += bullets(respostas)
        if num < len(perguntas) - 1:
            story.append(sp(0.2))

    story.append(PageBreak())
    return story

# ── BLOCO 7 — FIM DO S500 E CONSOLIDAÇÃO DO S10 ───────────────────────────────
def bloco7():
    story = []
    story += sec("FIM DO DIESEL S500 E CONSOLIDAÇÃO DO S10", "7")
    story.append(p(
        "O encerramento da produção de diesel S500 e a dedicação exclusiva ao S10 representa "
        "uma das maiores mudanças operacionais para distribuidoras e bases de combustíveis "
        "dos últimos 15 anos. A transição não é apenas regulatória — impacta diretamente "
        "tancagem, logística, contratos com clientes rurais, infraestrutura de mistura "
        "biodiesel e a rentabilidade de bases que historicamente operavam volumes relevantes "
        "de S500 para o agronegócio e uso industrial.", BODY))
    story.append(sp(0.2))

    story.append(sub("7.1  Contexto Regulatório e Cronograma ANP"))
    story.append(p(
        "O diesel S10 (≤10 ppm de enxofre) é o combustível exigido pelos motores Euro 6 "
        "(PROCONVE P8) e tem sido a referência para vias urbanas e rodovias desde 2012. "
        "O S500 (≤500 ppm) sobreviveu como alternativa legal para aplicações fora de estrada: "
        "tratores agrícolas, maquinário de construção, embarcações fluviais e geradores "
        "estacionários. A ANP (Res. nº 798/2019 e atualizações) vem progressivamente "
        "restringindo e padronizando as especificações, com trajetória clara de eliminação "
        "do S500 para uso geral.", BODY))
    story.append(sp(0.15))

    hdrs_reg = ["Período", "Marco Regulatório / Fato", "Impacto na Cadeia"]
    widths_reg = [2.5*cm, 8.0*cm, 7.5*cm]
    rows_reg = [
        ("2012–2013", "S10 torna-se obrigatório para diesel rodoviário nas regiões Sudeste, Sul, CO e capitais NE/N.",
         "Bases rodoviárias já adaptadas há mais de 10 anos. S500 relegado ao segmento agrícola/industrial."),
        ("2019", "ANP Resolução 798/2019 consolida especificações de diesel S10 e S500. PROCONVE P8 (Euro 6) sinalizado para 2022.",
         "Confirmação de que S10 é o produto-padrão de longo prazo. S500 sem perspectiva de crescimento."),
        ("2022–2024", "PROCONVE P8 entra em vigor. Novos caminhões e ônibus exigem S10 obrigatoriamente.",
         "Frota nova 100% S10. S500 perde relevância progressiva no diesel rodoviário. Volume S500 concentra em frotas antigas e uso rural."),
        ("Jan/2026", "B15 em vigor (biodiesel). ANP intensifica monitoramento de qualidade e restringe comercialização S500 em postos rodoviários.",
         "Mistura biodiesel B15 é feita sobre base S10. S500 não compõe mandato de mistura obrigatória na cadeia rodoviária."),
        ("2026–2027 (previsto)", "Encerramento progressivo da produção de S500 nas refinarias Petrobras. Refinarias convertem capacidade para S10.",
         "Oferta de S500 cai. Distribuidoras que ainda operam S500 precisam definir prazo e rota de transição para S10."),
        ("2028–2030 (projeção)", "S500 disponível apenas em circuitos restritos (estoque, importação). Mercado brasileiro unificado em S10.",
         "Tancagem dedicada a S500 precisa ser reconvertida. Clientes rurais migram para S10. Infraestrutura logística simplificada."),
    ]
    story.append(make_table(hdrs_reg, rows_reg, widths_reg, small=True))
    story.append(sp(0.3))

    story.append(sub("7.2  Por Que as Refinarias Estão Abandonando o S500"))
    temas_refino = [
        "<b>Investimento em HDS (hidrodessulfurização):</b> produzir S10 exige unidades HDS com maior pressão e temperatura. "
        "Uma vez investido — como Petrobras fez em REPLAN, REVAP, REPAR, RNEST e REDUC — não há incentivo para "
        "manter produção paralela de S500. O custo de oportunidade de produzir S500 em refinaria configurada para S10 é zero ou negativo.",

        "<b>Eficiência operacional:</b> manter dois produtos diesel na mesma refinaria (S10 e S500) implica gestão de "
        "tanques separados, controle de mistura e risco de contaminação. Com o mercado S500 encolhendo, a escala "
        "não justifica a complexidade operacional.",

        "<b>Pressão regulatória e ESG:</b> enxofre é poluente — emissões de SO₂ formam chuva ácida e material "
        "particulado (PM2.5). S10 reduz emissões de enxofre em 98% vs. S500. Financiadores (BNDES, bancos "
        "internacionais) e investidores pressionam Petrobras para eliminar combustíveis de alta emissão.",

        "<b>Alinhamento com biocombustíveis:</b> biodiesel B15→B20→B25 é misturado ao S10. Ter S500 na cadeia "
        "criaria produto de mistura fora de especificação ou exigiria lotes paralelos de biodiesel S500 — "
        "operacionalmente inviável em escala. O fim do S500 é pré-requisito para o aumento de mandato de biodiesel.",

        "<b>PROCONVE P8 e frotas novas:</b> qualquer caminhão, ônibus ou máquina fabricada pós-2022 opera "
        "exclusivamente com S10. A demanda por S500 é estruturalmente declinante — apenas estoque de máquinas antigas.",
    ]
    for t in temas_refino:
        story.append(Paragraph(f"▸  {t}", BULLET_S))
        story.append(sp(0.12))
    story.append(sp(0.2))

    story.append(sub("7.3  Impactos na Infraestrutura das Distribuidoras"))
    story.append(p(
        "O fim do S500 não é só uma mudança de produto — é uma operação de reconversão de "
        "ativos logísticos. Bases que operavam volumes relevantes de S500 precisam de ação "
        "estruturada nos próximos 2–3 anos.", BODY))
    story.append(sp(0.15))

    hdrs_inf = ["Componente", "Situação Atual (S500 ainda ativo)", "Após Fim do S500 (S10 exclusivo)",
                "Ação Necessária", "Prazo"]
    widths_inf = [2.5*cm, 3.8*cm, 3.8*cm, 3.5*cm, 1.4*cm]
    rows_inf = [
        ("Tancagem dedicada S500",
         "Tanks separados para S500 em bases rurais/agrícolas. Produto diferente do S10.",
         "Tanques ociosos ou mal aproveitados. S500 deixa de ser recebido do primário.",
         "Limpeza e certificação para S10. Avaliar conversão para biodiesel B100 ou etanol.",
         "2026–2028"),
        ("Mistura biodiesel",
         "S500 não entra na mistura obrigatória ANP. Mandatos B15+ são sobre S10.",
         "100% da base diesel para mistura é S10. Simplificação operacional.",
         "Nenhuma. Operação de mistura já é sobre S10 na maioria das bases.",
         "Imediata"),
        ("Contratos de fornecimento",
         "Contratos com Petrobras, distribuidoras primárias ou importadores incluem volumes S500.",
         "S500 sai do portfólio. Contratos precisam ser renegociados para S10 exclusivo.",
         "Renegociar contratos com primário. Ajustar volumes S10 para cobrir demanda migrada do S500.",
         "2026–2027"),
        ("Logística e transporte",
         "Caminhões-tanque operam com S10 e S500 em cargas separadas ou sequenciais.",
         "Carga unificada S10. Eliminação do risco de contaminação cruzada S500/S10.",
         "Atualizar procedimentos operacionais. Revisão de rotas e frequência de abastecimento.",
         "2027"),
        ("Laboratório e qualidade",
         "Análise regular de enxofre para verificar produto (S10 vs. S500 vs. contaminado).",
         "Apenas verificação de conformidade S10. Simplificação analítica.",
         "Atualizar protocolo de qualidade. Garantir que tanques reconvertidos não contaminem S10.",
         "2026–2027"),
        ("Infraestrutura de recebimento",
         "Braços/mangotes/plataformas de recebimento S500 em terminais rurais.",
         "Toda infraestrutura recebe S10. Eliminação de etiquetagem dupla.",
         "Padronização de braços e identificação visual. Sem custo adicional relevante.",
         "2027"),
        ("Terminais novos (Palmeirante, TEMAPE, Pecém, Santa Helena)",
         "Projetados para S10 como produto principal. S500 não é premissa de projeto.",
         "100% S10 desde o primeiro dia de operação. Sem necessidade de adaptação.",
         "Nenhuma. Confirmação que projeto não inclui tancagem S500 nas especificações.",
         "N/A"),
    ]
    story.append(make_table(hdrs_inf, rows_inf, widths_inf, small=True))
    story.append(sp(0.3))

    story.append(sub("7.4  Impacto Comercial por Segmento de Cliente"))
    story.append(p(
        "O S500 era o produto de referência para o agronegócio, construção civil e "
        "embarcações fluviais. A migração forçada desses segmentos para S10 tem "
        "implicações diretas de preço, operação de equipamento e relação comercial "
        "das distribuidoras com seus maiores clientes industriais.", BODY))
    story.append(sp(0.15))

    hdrs_com = ["Segmento", "Volume S500 Estimado", "Impacto da Transição",
                "Risco para a Distribuidora", "Oportunidade"]
    widths_com = [2.5*cm, 2.5*cm, 4.0*cm, 3.5*cm, 4.5*cm]
    rows_com = [
        ("Agronegócio (tratores, colheitadeiras, irrigação)",
         "~30–40% do total S500 nacional. MATOPIBA concentra maior parte.",
         "S10 sobe ~3–8% vs. S500 na ponta. Motores antigos podem ter desgaste adicional por menor lubrificidade.",
         "Perda de cliente que migre para concorrente com S500 em estoque. Reclamações de equipamento.",
         "Reposicionamento como fornecedor de 'diesel limpo'. Vender S10 + aditivo lubrificante (produto de maior margem)."),
        ("Construção civil e mineração",
         "~20–25% do S500. Uso em escavadeiras, britadores, geradores.",
         "Maquinário moderno já homologado para S10. Equipamentos mais antigos: verificar fabricante.",
         "Gestão de frotas mistas (equipamentos antigos com S500, novos com S10).",
         "Contrato de abastecimento direto para obras com S10. Pool de tanques móveis."),
        ("Embarcações fluviais (hidrovias)",
         "~15% S500. Tapajós, Madeira, Tocantins, Paraguai.",
         "Motores navais certificados para S500. Migração exige homologação ou troca de motor.",
         "Armadores que resistam à transição e busquem S500 importado.",
         "Ser o primeiro a ofertar S10 certificado para uso embarcações fluviais. Diferenciação de produto."),
        ("Geração distribuída (geradores estacionários)",
         "~10–15% S500. Indústria, hospitais, condomínios.",
         "Geradores modernos já usam S10. Modelos antigos precisam de adaptação de filtros.",
         "Mínimo. Geradores são facilmente adaptáveis ou substituídos.",
         "Oferta de S10 + contrato de manutenção de filtros. Parceria com assistência técnica."),
        ("Setor pesqueiro (embarcações costeiras)",
         "~5–10% S500. Uso por pescadores artesanais e industriais.",
         "Alta dependência de preço. S10 encarece operação de pesca artesanal.",
         "Pressão política para manutenção do S500 em zonas pesqueiras. ANP pode criar exceções temporárias.",
         "Monitorar regulação ANP para setor pesqueiro. Posição como fornecedor de porto pesqueiro com S10."),
    ]
    story.append(make_table(hdrs_com, rows_com, widths_com, small=True))
    story.append(sp(0.3))

    story.append(sub("7.5  Interseção S10 × MATOPIBA × Terminais Novos"))
    story.append(p(
        "A coincidência temporal entre o fim do S500 e a inauguração de novos terminais "
        "em regiões de alto consumo agrícola (Palmeirante/TO, TEMAPE Teresina/PI, "
        "Santa Helena/GO, INPASA LEM/BA) cria uma janela estratégica única: "
        "os terminais chegam prontos para S10 no exato momento em que o "
        "S500 será descontinuado. Distribuidoras que posicionarem sua base logística "
        "nesses novos terminais já nascem com a infraestrutura certa, sem legado.", BODY))
    story.append(sp(0.15))

    cruzamentos = [
        "<b>Palmeirante/TO (Ultracargo, ✅ set/25):</b> 23.000 m³ projetados para diesel S10 + "
        "gasolina + etanol. Região serve MATOPIBA com alta intensidade de uso agrícola. "
        "Distribuidoras com posição no Palmeirante entram direto no S10 sem legado de tanques S500.",

        "<b>TEMAPE Teresina/PI (op. 2028):</b> 27.000 m³ + ferrovia Transnordestina. Todo produto "
        "que chegará por trilho (de Pecém/CE) será S10. PI deixa de ser abastecido por "
        "caminhões com mix S500/S10 — passa a receber S10 ferroviário puro.",

        "<b>INPASA Balsas/MA + LEM/BA:</b> as biorrefinarias produzem etanol milho mas também "
        "consomem diesel S10 na colheita e processo industrial. São clientes finais de alto "
        "volume de S10, e ao mesmo tempo produtores de etanol que disputam espaço logístico "
        "nos mesmos terminais. Distribuidora pode vender S10 para a INPASA e comprar "
        "etanol milho dela — relação comercial dupla.",

        "<b>Granel Química Santa Helena/GO (→ 2026):</b> terminal rodo-ferroviário projetado para "
        "biocombustíveis e combustíveis. Sem infraestrutura S500 no projeto. "
        "GO sudoeste é região intensiva em agricultura mecanizada — principal usuário de "
        "S500 que precisará migrar para S10. Terminal chega como facilitador da transição.",

        "<b>Biodiesel B15→B25 sobre base S10:</b> toda a expansão do mandato de biodiesel "
        "acontece sobre diesel S10 como base. O fim do S500 é, portanto, um pré-requisito "
        "operacional para a escalada dos mandatos. Distribuidoras que ainda operem S500 em "
        "2027+ terão dificuldade de conformidade com os mandatos de mistura ANP.",
    ]
    for c in cruzamentos:
        story.append(Paragraph(f"▸  {c}", BULLET_S))
        story.append(sp(0.12))
    story.append(sp(0.25))

    story.append(sub("7.6  Recomendações Práticas — O Que Fazer Agora"))
    story.append(sp(0.1))

    hdrs_rec = ["Ação", "Prioridade", "Prazo", "Detalhamento"]
    widths_rec = [3.5*cm, 1.8*cm, 1.8*cm, 11.0*cm]
    rows_rec = [
        ("Inventário de tancagem S500 por base",
         "CRÍTICA", "Imediata",
         "Mapear volume e % da tancagem dedicada a S500. Identificar bases mais expostas. "
         "Calcular custo de reconversão (limpeza, certificação) vs. custo de manutenção de dois produtos."),
        ("Revisão de contratos de fornecimento primário",
         "CRÍTICA", "6–12 meses",
         "Renegociar volumes S500 com Petrobras ou distribuidoras primárias. "
         "Antecipar migração de volumes para S10 antes que S500 saia de linha e deixe bases desabastecidas."),
        ("Plano de migração de clientes rurais/agrícolas",
         "ALTA", "6–18 meses",
         "Identificar top 20% clientes por volume de S500. Comunicar transição. "
         "Oferecer S10 + aditivo lubrificante como produto de substituição com valor agregado. "
         "Evitar perda de cliente por falta de planejamento."),
        ("Reconversão de tanques S500 → S10 ou B100",
         "ALTA", "12–24 meses",
         "Tanques S500 reconvertidos para S10 ampliam tancagem do produto que crescerá. "
         "Alternativa: converter para B100 (biodiesel), cujo volume aumenta com B15→B20→B25. "
         "Verificar compatibilidade de revestimento interno e selo ABNT."),
        ("Posicionamento nos novos terminais",
         "ALTA", "Imediata → 2027",
         "Terminais novos (Palmeirante, Pecém, Santa Helena, TEMAPE) são 100% S10. "
         "Garantir posição nesses terminais é garantir a infraestrutura S10 certa para o futuro. "
         "Distribuidoras sem posição em bases legadas de S500 estão em vantagem — não precisam reconverter."),
        ("Adequação do protocolo de qualidade",
         "MÉDIA", "12 meses",
         "Atualizar procedimentos de análise laboratorial para eliminar rotinas S500. "
         "Reforçar verificação de contaminação cruzada durante o período de transição "
         "(tanques que tiveram S500 e passam a receber S10 são risco de não-conformidade)."),
        ("Comunicação regulatória e monitoramento ANP",
         "MÉDIA", "Contínuo",
         "Acompanhar publicações ANP sobre prazo definitivo de encerramento do S500. "
         "Participar de audiências públicas. Ter jurídico mapeando impacto de resolução final. "
         "Evitar ser pego de surpresa por decreto com prazo curto de adequação."),
        ("Revisão de rentabilidade de rotas rurais",
         "MÉDIA", "6–18 meses",
         "Rotas atendidas hoje exclusivamente por S500 podem se tornar antieconômicas se "
         "o volume migrar para S10 com margem menor ou se clientes rurais trocarem de fornecedor. "
         "Reavaliar custo de atendimento vs. margem real por rota."),
    ]
    story.append(make_table(hdrs_rec, rows_rec, widths_rec, small=True))
    story.append(sp(0.25))

    story.append(sub("7.7  Síntese — S500 como Janela de Oportunidade, Não Só Ameaça"))
    sintese = [
        "<b>Simplificação logística:</b> um produto diesel no portfólio reduz complexidade operacional, "
        "risco de contaminação, custo de laboratório e número de SKUs. Para distribuidoras com "
        "operação diversificada, o fim do S500 é uma simplificação bem-vinda.",

        "<b>Produto de maior valor:</b> S10 tem margem unitária melhor que S500 na maioria das regiões. "
        "A migração de volumes S500 → S10 pode melhorar a rentabilidade bruta por litro, "
        "especialmente em regiões onde o S500 era vendido com desconto para competir.",

        "<b>Alinhamento com biocombustíveis:</b> a trajetória B15→B20→B25 é estrutural. "
        "Quanto antes as bases estiverem 100% S10, mais elas estão prontas para escalar "
        "o mandato de biodiesel sem complicação operacional.",

        "<b>Novos terminais como catalisadores:</b> Palmeirante, TEMAPE, Pecém e Santa Helena chegam "
        "no timing perfeito — 100% S10 no momento em que o mercado rural precisa migrar. "
        "Distribuidoras posicionadas nesses terminais oferecem a solução ao cliente, "
        "não o problema.",

        "<b>Risco real — cliente rural sem alternativa preparada:</b> a maior ameaça é perder "
        "clientes do agronegócio para distribuidoras que mantenham S500 em estoque ou "
        "importação irregular por mais tempo. O timing da transição precisa ser gerenciado "
        "com comunicação proativa, não reativa.",
    ]
    for s in sintese:
        story.append(Paragraph(f"▸  {s}", BULLET_S))
        story.append(sp(0.12))

    story.append(PageBreak())
    return story


# ── FONTES ────────────────────────────────────────────────────────────────────
def fontes():
    story = []
    story += sec("FONTES CONSULTADAS", "8")
    story.append(sp(0.1))

    lista_fontes = [
        "<b>ANP — Agência Nacional do Petróleo, Gás Natural e Biocombustíveis:</b> autorizações de operação, dados de produção biocombustíveis. www.gov.br/anp",
        "<b>EPE — Empresa de Pesquisa Energética:</b> PDE 2035, projeções eletrificação frota, etanol de milho. www.epe.gov.br",
        "<b>ANTT — Agência Nacional de Transportes Terrestres:</b> aprovação TEMAPE/Transnordestina (Investidor Associado mar/2025). www.antt.gov.br",
        "<b>ANTAQ — Agência Nacional de Transportes Aquaviários:</b> arrendamentos e autorizações portuárias. www.antaq.gov.br",
        "<b>Ministério dos Transportes / Gov.br:</b> FIOL 2 (edital set/2025), Transnordestina, FMT, Ferrovia Açailândia-Barcarena. www.gov.br/transportes",
        "<b>PPI — Programa de Parcerias de Investimentos:</b> Corredor Leste-Oeste, FIOL. ppi.gov.br",
        "<b>BNDES:</b> aprovação R$2bi FMT/Rumo, R$1bi RRP Energia Tapurah. agenciadenoticias.bndes.gov.br",
        "<b>CIPP S.A. / Complexo do Pecém:</b> tancagem, Hub H2V, Stolthaven, contratos. complexodopecem.com.br",
        "<b>Governo do Estado do Ceará / SDE-CE:</b> parque de tancagem Pecém, Transnordestina. ceara.gov.br",
        "<b>Petrobras:</b> RPBC BioQAV+HVO, SAF. agencia.petrobras.com.br / eixos.com.br",
        "<b>Ultracargo:</b> Palmeirante/TO, terminal inauguração set/2025. ultracargo.com.br",
        "<b>VLI Logística:</b> Terminal Portuário São Luís, Norte-Sul. vli-logistica.com.br",
        "<b>INPASA:</b> Balsas/MA, Nova Mutum/MT, Rondonópolis/MT, LEM/BA. noticiasagricolas.com.br / cpgclick / movimentoeconomico.com.br",
        "<b>FS Bioenergia:</b> Campo Novo do Parecis, ciclo expansão 2026-2027.",
        "<b>CerradinhoBio / Neomille:</b> Chapadão do Céu/GO. comprerural.com / novacana.com",
        "<b>Granel Química:</b> Santa Helena/GO, terminal rodo-ferroviário. portosenavios.com.br / empreenderemgoias.com.br",
        "<b>TEMAPE:</b> Terminal Teresina, aprovação ANTT. diario.dopovo.com.br / agenciagov.ebc.com.br",
        "<b>Blue Terminals:</b> Vila Velha/ES. portosenavios.com.br",
        "<b>Prefeitura de Santarém / CDP:</b> Raízen+Vibra terminal, R$350mi. santarem.pa.gov.br",
        "<b>Portal da Navegação / Gov.br Portos:</b> Miritituba/Tapajós, Arco Norte. portaldanavegacao.com / gov.br/portos",
        "<b>BrazilJournal / CPG Click / NovaCana / PortoseNavios / AgênciaInfra:</b> cobertura setorial cruzada.",
        "<b>ABIOVE / BiodieselBR:</b> capacidade instalada biodiesel, mandato B15. abiove.org.br",
        "<b>FMT — Ferrovia Estadual de Mato Grosso / Rumo:</b> obras 743km, Lucas RV. ferroviamt.com.br / cpgclick.com.br",
        "<b>SEAMA-ES / Gov.ES:</b> licença prévia terminal líquidos Vila Velha. seama.es.gov.br",
        f"<i>Data de corte da pesquisa: Maio/2026. Dados verificados em múltiplas fontes cruzadas.</i>",
    ]

    for f in lista_fontes:
        story.append(Paragraph(f"• {f}", BULLET_S))
        story.append(sp(0.05))

    story.append(sp(0.5))
    story.append(hr(MID_BLUE, 1.5, 4, 4))
    story.append(p(
        "Este relatório foi produzido com base em fontes públicas verificadas. Informações sobre "
        "capacidades, investimentos e prazos refletem o que estava disponível em fontes públicas "
        "em maio/2026. Onde não foi possível identificar dado público confiável, "
        "indicamos 'não identificado em fonte pública'. Hipóteses estratégicas estão "
        "claramente sinalizadas. Uso interno confidencial.", NOTE_S))
    return story

# ── MONTAGEM COMPLETA ─────────────────────────────────────────────────────────
def build_story():
    story = []
    story += cover_page()
    story += bloco1()
    story += bloco2()
    story += bloco3()
    story += bloco4()
    story += bloco5()
    story += bloco6()
    story += bloco7()
    story += fontes()
    return story

def generate_pdf(output_path):
    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2.2*cm,
        bottomMargin=2.2*cm,
    )

    cover_frame = Frame(0, 0, W, H, leftPadding=2*cm, rightPadding=2*cm,
                        topPadding=2.5*cm, bottomPadding=2*cm, id='cover')
    normal_frame = Frame(doc.leftMargin, doc.bottomMargin,
                         doc.width, doc.height, id='normal')

    cover_template = PageTemplate(id='Cover', frames=[cover_frame],
                                  onPage=lambda c, d: None)
    normal_template = PageTemplate(id='Normal', frames=[normal_frame],
                                   onPage=_page_template)

    doc.addPageTemplates([cover_template, normal_template])
    doc.pageTemplates[0] = cover_template
    doc.pageTemplates[1] = normal_template

    story = build_story()
    doc.build(story)
    print(f"PDF gerado: {output_path}")

if __name__ == '__main__':
    output = '/home/user/claudin2/Radar_Infraestrutura_Combustiveis_2026.pdf'
    generate_pdf(output)
