from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable
from reportlab.lib.colors import HexColor

# Color palette
ROSE = HexColor('#E8557A')
ROSE_LIGHT = HexColor('#FDF0F4')
ROSE_DARK = HexColor('#C03060')
DARK = HexColor('#1A1A2E')
GRAY = HexColor('#6B7280')
GRAY_LIGHT = HexColor('#F3F4F6')
WHITE = HexColor('#FFFFFF')
GOLD = HexColor('#F59E0B')
TEAL = HexColor('#0D9488')
TEAL_LIGHT = HexColor('#F0FDFA')

class RoundedBox(Flowable):
    def __init__(self, width, height, bg_color, border_color=None, radius=6):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.border_color = border_color
        self.radius = radius

    def draw(self):
        self.canv.setFillColor(self.bg_color)
        if self.border_color:
            self.canv.setStrokeColor(self.border_color)
            self.canv.setLineWidth(0.5)
        else:
            self.canv.setStrokeColor(self.bg_color)
        self.canv.roundRect(0, 0, self.width, self.height, self.radius, fill=1, stroke=1)

class NumberBadge(Flowable):
    def __init__(self, number, color):
        Flowable.__init__(self)
        self.number = number
        self.color = color
        self.width = 22
        self.height = 22

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.circle(11, 11, 11, fill=1, stroke=0)
        self.canv.setFillColor(WHITE)
        self.canv.setFont('Helvetica-Bold', 11)
        self.canv.drawCentredString(11, 7, str(self.number))

def build_pdf(output_path, data):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=18*mm,
        leftMargin=18*mm,
        topMargin=12*mm,
        bottomMargin=18*mm,
        title="Audit Instagram – " + data.get('business_name', 'Votre Compte'),
    )

    W = A4[0] - 36*mm
    story = []

    # ── COVER HEADER ──────────────────────────────────────────────────────────
    def add_header():
        # Header background bar (drawn inline via Table)
        header_data = [[
            Paragraph(
                f'<font color="#FFFFFF" size="20"><b>Audit Instagram</b></font>',
                ParagraphStyle('hdr', fontName='Helvetica-Bold', fontSize=20, textColor=WHITE, alignment=TA_LEFT)
            ),
            Paragraph(
                f'<font color="#FFFFFF" size="11">@{data.get("instagram", "votre_compte")}</font>',
                ParagraphStyle('sub', fontName='Helvetica', fontSize=11, textColor=WHITE, alignment=TA_RIGHT)
            )
        ]]
        t = Table(header_data, colWidths=[W*0.65, W*0.35])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), ROSE),
            ('TOPPADDING', (0,0), (-1,-1), 14),
            ('BOTTOMPADDING', (0,0), (-1,-1), 14),
            ('LEFTPADDING', (0,0), (0,-1), 16),
            ('RIGHTPADDING', (-1,0), (-1,-1), 16),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(t)
        story.append(Spacer(1, 10))

        # Sub-header info strip
        info_data = [[
            Paragraph(f'<b>{data.get("business_name","Votre business")}</b>', ParagraphStyle('info', fontName='Helvetica-Bold', fontSize=11, textColor=DARK)),
            Paragraph(f'{data.get("goal","Acquisition clients")}', ParagraphStyle('info2', fontName='Helvetica', fontSize=10, textColor=GRAY, alignment=TA_CENTER)),
            Paragraph(f'Score global : <b><font color="#E8557A">{data.get("score","72")}/100</font></b>', ParagraphStyle('score', fontName='Helvetica', fontSize=11, textColor=DARK, alignment=TA_RIGHT)),
        ]]
        t2 = Table(info_data, colWidths=[W*0.4, W*0.35, W*0.25])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), GRAY_LIGHT),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (0,-1), 14),
            ('RIGHTPADDING', (-1,0), (-1,-1), 14),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, HexColor('#E5E7EB')),
        ]))
        story.append(t2)
        story.append(Spacer(1, 18))

    add_header()

    # ── SECTION HELPER ────────────────────────────────────────────────────────
    def section_title(text, accent=ROSE):
        story.append(Spacer(1, 8))
        bar_data = [[Paragraph(f'<b>{text}</b>',
            ParagraphStyle('stitle', fontName='Helvetica-Bold', fontSize=13, textColor=WHITE))]]
        t = Table(bar_data, colWidths=[W])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), accent),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))

    def body_text(text):
        story.append(Paragraph(text, ParagraphStyle('body', fontName='Helvetica', fontSize=10.5, textColor=DARK, leading=16, spaceAfter=4)))

    def bullet_item(text, color=ROSE):
        bullet_style = ParagraphStyle('bullet', fontName='Helvetica', fontSize=10.5, textColor=DARK, leading=15,
                                       leftIndent=18, firstLineIndent=-14, spaceAfter=3)
        story.append(Paragraph(f'<font color="#{format(int(color.red*255),"02x")}{format(int(color.green*255),"02x")}{format(int(color.blue*255),"02x")}">●</font>  {text}', bullet_style))

    def two_col_table(left_items, right_items, left_title, right_title):
        left_content = f'<b>{left_title}</b><br/><br/>' + '<br/>'.join([f'● {i}' for i in left_items])
        right_content = f'<b>{right_title}</b><br/><br/>' + '<br/>'.join([f'● {i}' for i in right_items])
        tdata = [[
            Paragraph(left_content, ParagraphStyle('tc', fontName='Helvetica', fontSize=10, textColor=DARK, leading=15)),
            Paragraph(right_content, ParagraphStyle('tc2', fontName='Helvetica', fontSize=10, textColor=DARK, leading=15)),
        ]]
        t = Table(tdata, colWidths=[W*0.48, W*0.48], spaceBefore=4)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), ROSE_LIGHT),
            ('BACKGROUND', (1,0), (1,-1), TEAL_LIGHT),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('COLPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    def score_bar(label, score, max_score=10):
        pct = score / max_score
        bar_w = W - 120
        filled = bar_w * pct
        row_data = [[
            Paragraph(label, ParagraphStyle('sl', fontName='Helvetica', fontSize=10, textColor=DARK)),
            Paragraph(f'<b><font color="#E8557A">{score}/{max_score}</font></b>',
                      ParagraphStyle('sv', fontName='Helvetica-Bold', fontSize=10, textColor=ROSE, alignment=TA_RIGHT)),
        ]]
        t = Table(row_data, colWidths=[W*0.75, W*0.25])
        t.setStyle(TableStyle([
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t)

    def mistake_box(num, title, detail):
        icon_col = Paragraph(f'<font size="18">⚠</font>', ParagraphStyle('ic', fontName='Helvetica', fontSize=18, textColor=GOLD, alignment=TA_CENTER))
        title_p = Paragraph(f'<b>Erreur #{num} — {title}</b>', ParagraphStyle('mt', fontName='Helvetica-Bold', fontSize=11, textColor=DARK))
        detail_p = Paragraph(detail, ParagraphStyle('md', fontName='Helvetica', fontSize=10, textColor=GRAY, leading=14))
        t = Table([[icon_col, [title_p, Spacer(1,3), detail_p]]], colWidths=[30, W-30])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor('#FFFBEB')),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (0,-1), 8),
            ('LEFTPADDING', (1,0), (1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, HexColor('#FDE68A')),
        ]))
        story.append(t)
        story.append(Spacer(1, 5))

    def action_box(num, title, detail, color=TEAL):
        num_p = Paragraph(f'<b><font color="#FFFFFF">{num:02d}</font></b>',
                          ParagraphStyle('nb', fontName='Helvetica-Bold', fontSize=11, textColor=WHITE, alignment=TA_CENTER))
        title_p = Paragraph(f'<b>{title}</b>', ParagraphStyle('at', fontName='Helvetica-Bold', fontSize=11, textColor=DARK))
        detail_p = Paragraph(detail, ParagraphStyle('ad', fontName='Helvetica', fontSize=10, textColor=GRAY, leading=14))
        num_cell = Table([[num_p]], colWidths=[28])
        num_cell.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), color),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('ROUNDEDCORNERS', [4,4,4,4]),
        ]))
        t = Table([[num_cell, [title_p, Spacer(1,3), detail_p]]], colWidths=[36, W-36])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), TEAL_LIGHT),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (0,-1), 4),
            ('LEFTPADDING', (1,0), (1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, HexColor('#99F6E4')),
        ]))
        story.append(t)
        story.append(Spacer(1, 5))

    def post_idea_card(num, title, hook, why):
        t = Table([[
            Paragraph(f'💡 Idée #{num}', ParagraphStyle('pi_h', fontName='Helvetica-Bold', fontSize=10, textColor=ROSE)),
            Paragraph(f'', ParagraphStyle('empty')),
        ]], colWidths=[W*0.5, W*0.5])
        story.append(t)
        inner = [
            Paragraph(f'<b>{title}</b>', ParagraphStyle('pit', fontName='Helvetica-Bold', fontSize=11, textColor=DARK, spaceAfter=4)),
            Paragraph(f'<i>Hook :</i> {hook}', ParagraphStyle('pih', fontName='Helvetica-Oblique', fontSize=10, textColor=GRAY, leading=14, spaceAfter=4)),
            Paragraph(f'<i>Pourquoi ça convertit :</i> {why}', ParagraphStyle('piw', fontName='Helvetica', fontSize=10, textColor=DARK, leading=14)),
        ]
        card = Table([[inner]], colWidths=[W])
        card.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), ROSE_LIGHT),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
            ('RIGHTPADDING', (0,0), (-1,-1), 14),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, HexColor('#FBCFE8')),
        ]))
        story.append(card)
        story.append(Spacer(1, 6))

    # ── SECTION 1 : SCORES ────────────────────────────────────────────────────
    section_title("01 — Scores de performance")
    scores = data.get('scores', {
        'Positionnement & niche': 7,
        'Bio & conversion profil': 5,
        'Qualité du contenu': 6,
        'Déclencheurs psychologiques': 4,
        'Parcours de réservation': 5,
    })
    for label, score in scores.items():
        score_bar(label, score)
    story.append(Spacer(1, 6))

    # ── SECTION 2 : ANALYSE ───────────────────────────────────────────────────
    section_title("02 — Analyse de positionnement")
    body_text(data.get('positioning_analysis',
        "Votre compte présente un positionnement <b>généraliste</b> qui dilue votre attractivité. "
        "La transformation promise n'est pas visible dès la première seconde. Le profil attire actuellement "
        "des prospects <i>price-sensitive</i> au lieu de clients premium capables d'investir dans vos services."))
    story.append(Spacer(1, 4))

    two_col_table(
        data.get('profile_weaknesses', [
            "Bio orientée service, pas client",
            "Aucun CTA clair au-dessus du fold",
            "Highlights non structurés",
            "Absence de preuve sociale visible",
        ]),
        data.get('content_weaknesses', [
            "Contenu qui montre, pas qui vend",
            "Pas de hooks textuels forts",
            "Manque de cohérence visuelle",
            "Zéro contenu de repositionnement prix",
        ]),
        "⚠ Faiblesses profil",
        "⚠ Faiblesses contenu"
    )

    # ── SECTION 3 : 3 ERREURS ─────────────────────────────────────────────────
    section_title("03 — 3 Erreurs critiques qui vous coûtent des clients")
    for i, (title, detail) in enumerate(data.get('mistakes', [
        ("Bio ego-centrique", "Votre bio parle de vous, pas de la transformation que vous offrez. Le prospect cherche ce qu'il gagne, pas qui vous êtes."),
        ("Absence d'urgence et de rareté", "Aucun levier de scarcity visible : pas de 'agenda chargé', pas de délai de réponse, rien qui signale la demande."),
        ("Contenu sans désir", "Vos posts montrent le résultat final sans raconter le voyage. Pas d'émotion, pas d'aspiration, pas de déclenchement d'achat.")
    ]), start=1):
        mistake_box(i, title, detail)

    # ── SECTION 4 : 5 ACTIONS ─────────────────────────────────────────────────
    section_title("04 — 5 Actions prioritaires", accent=TEAL)
    for i, (title, detail) in enumerate(data.get('actions', [
        ("Réécrire la bio en 3 lignes ROI", "Ligne 1 : résultat transformatif. Ligne 2 : preuve (chiffre ou social proof). Ligne 3 : CTA direct vers lien de réservation."),
        ("Créer un highlight 'Avant/Après'", "Structurez vos meilleurs résultats dans un highlight dédié. C'est votre vitrine de conversion N°1."),
        ("Ajouter un hook visuel sur chaque post", "Les 3 premières secondes décident du scroll. Texte en overlay sur la miniature : posez une question douloureuse."),
        ("Publier du contenu de valeur perçue", "1 post/semaine éducatif sur les soins, les matériaux premium, les coulisses de votre expertise. Justifie vos prix."),
        ("Activer le levier de rareté en story", "Story hebdo : 'Il me reste 2 créneaux cette semaine.' Capturez l'urgence sans être agressif.")
    ]), start=1):
        action_box(i, title, detail)

    # ── SECTION 5 : IDÉES DE POSTS ────────────────────────────────────────────
    section_title("05 — 3 Idées de posts conçus pour les réservations")
    for i, (title, hook, why) in enumerate(data.get('post_ideas', [
        (
            "Le vrai coût d'un mauvais soin",
            "« Voici ce qui arrive quand on choisit le prix plutôt que la qualité... »",
            "Repositionne votre prix comme investissement, pas comme dépense. Élimine la concurrence low-cost."
        ),
        (
            "Avant/Après + histoire client réelle",
            "« Elle m'a dit qu'elle avait honte de ses mains. Voilà ce qu'on a fait en 90 min. »",
            "Combinaison émotion + résultat tangible = post le plus partagé et le plus générateur de DM."
        ),
        (
            "Routine des coulisses",
            "« Ce que je fais avant chaque cliente pour que vos résultats durent 3 semaines de plus »",
            "Démontre l'expertise, justifie le prix premium, crée une relation de confiance pré-achat."
        )
    ]), start=1):
        post_idea_card(i+1, title, hook, why)

    # ── FOOTER / UPSELL ───────────────────────────────────────────────────────
    story.append(Spacer(1, 12))
    footer_data = [[
        Paragraph(
            '<b>Prêt(e) à passer à l\'étape suivante ?</b><br/>'
            '<font size="10" color="#6B7280">Cet audit identifie les problèmes. L\'accompagnement les résout — en 30 jours.</font>',
            ParagraphStyle('ft', fontName='Helvetica', fontSize=11, textColor=DARK, leading=16)
        ),
        Paragraph(
            '<b>Coaching Stratégique Instagram</b><br/>'
            '<font color="#E8557A" size="12"><b>97€/mois</b></font><br/>'
            '<font size="9" color="#6B7280">Réservez votre appel découverte →</font>',
            ParagraphStyle('fu', fontName='Helvetica', fontSize=10, textColor=DARK, leading=14, alignment=TA_RIGHT)
        ),
    ]]
    t = Table(footer_data, colWidths=[W*0.6, W*0.4])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (0,-1), 16),
        ('RIGHTPADDING', (-1,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TEXTCOLOR', (0,0), (-1,-1), WHITE),
    ]))
    story.append(t)

    doc.build(story)
    print(f"PDF généré : {output_path}")


# Sample data for demo
sample_data = {
    "instagram": "coiffure_paris_marie",
    "business_name": "Marie — Salon de Coiffure Premium, Paris 11e",
    "goal": "Acquisition clients premium & visibilité locale",
    "score": "68",
    "scores": {
        "Positionnement & niche": 6,
        "Bio & conversion profil": 4,
        "Qualité du contenu": 7,
        "Déclencheurs psychologiques": 3,
        "Parcours de réservation": 5,
    },
    "positioning_analysis": (
        "Votre compte oscille entre salon de coiffure généraliste et spécialiste coloriste, "
        "ce qui dilue votre attractivité. Aucune spécialisation premium n'est communiquée dès l'arrivée. "
        "Le profil attire actuellement des prospects <b>price-sensitive</b> alors que votre travail "
        "justifie clairement un positionnement haut de gamme. La transformation offerte (couleur naturelle, "
        "technique balayage avancée) n'est visible qu'après défilement approfondi — trop tard."
    ),
    "profile_weaknesses": [
        "Bio orientée service, pas transformation",
        "Aucun CTA clair — lien en bio non trackable",
        "Highlights non structurés (12 catégories)",
        "Zéro chiffre ou preuve sociale en bio",
    ],
    "content_weaknesses": [
        "Photos de résultats sans mise en contexte",
        "Hooks textuels absents — aucun arrêt du scroll",
        "Incohérence filtre/palette entre posts",
        "Aucun contenu d'autorité ou éducatif",
    ],
    "mistakes": [
        ("Bio auto-centrée", "Vous décrivez votre salon, vos services, votre adresse. Le prospect cherche CE QU'IL VA OBTENIR, pas où vous êtes. Chaque ligne de bio doit répondre à la question : 'Qu'est-ce que j'y gagne ?'"),
        ("Contenu sans désir ni émotion", "Vos posts montrent de belles photos mais ne racontent pas d'histoire. Aucun prospect ne se projette. La beauté seule ne convertit pas — la narration, si."),
        ("Parcours de réservation flou", "Il faut 4 clics minimum pour réserver. Chaque friction supplémentaire = clients perdus. Votre lien en bio redirige vers une page générale du site, pas vers un formulaire de réservation direct.")
    ],
    "actions": [
        ("Réécrire la bio en format ROI", "Ligne 1 : résultat transformatif (ex: 'Spécialiste couleur naturelle & balayage invisible'). Ligne 2 : preuve sociale (ex: '+200 clientes satisfaites depuis 2019'). Ligne 3 : CTA direct vers Calendly ou Doctolib."),
        ("Créer le highlight 'Résultats' comme vitrine", "Sélectionnez vos 10 meilleurs avant/après. Vignette rose sobre. Ce highlight seul peut doubler votre taux de DM en 30 jours."),
        ("Ajouter un hook textuel sur chaque Reel", "Format prouvé : '[Douleur client]' ou question provocante en overlay. Ex : 'Votre coloriste vous dit toujours la même chose ?'"),
        ("Publier 1 post de valeur par semaine", "Sujet : pourquoi votre technique coûte plus cher et vaut chaque centime. Format carrousel 5 slides. Ce contenu filtre les mauvais clients et attire les bons."),
        ("Story de rareté hebdomadaire", "Chaque lundi : 'Agenda semaine — il reste X créneaux.' Screenshot de l'agenda flou visible. Résultat : les clientes hésitantes réservent par peur de manquer.")
    ],
    "post_ideas": [
        (
            "Le vrai coût d'un mauvais soin colorant",
            "« Ce que vous payez 40€ moins cher vous coûtera 200€ à réparer »",
            "Repositionne votre prix comme investissement, élimine la comparaison avec les salons low-cost. Génère des partages dans les groupes de beauté locaux."
        ),
        (
            "Transformation réelle avec histoire cliente",
            "« Elle avait honte de sortir sans chapeau depuis 2 ans. Voilà ce qu'on a créé ensemble en une séance. »",
            "Émotion + résultat tangible = combinaison maximale pour les sauvegardes et les DM entrants. Format Reel vertical 30s."
        ),
        (
            "Les 3 questions à poser avant de choisir un salon",
            "« La plupart des femmes ne les posent jamais... et le regrettent »",
            "Contenu d'autorité qui vous positionne en experte, crée de la confiance sans parler de vous directement, et génère des sauvegardes massives."
        )
    ]
}

build_pdf('/mnt/user-data/outputs/audit_instagram_template.pdf', sample_data)
