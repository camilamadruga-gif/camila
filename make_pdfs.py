#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 HRFlowable, Table, TableStyle, Preformatted)
from reportlab.platypus import KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import re

ACCENT = colors.HexColor('#C8843A')
TEXT   = colors.HexColor('#2C1A0E')
MUTED  = colors.HexColor('#8B6F5E')
BG     = colors.HexColor('#FDF6F0')
BORDER = colors.HexColor('#E8D5C4')

W, H = A4

def make_styles():
    base = getSampleStyleSheet()
    s = {}

    s['h1'] = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=20,
                              textColor=ACCENT, spaceAfter=6, spaceBefore=16,
                              leading=26)
    s['h2'] = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=14,
                              textColor=TEXT, spaceAfter=4, spaceBefore=14,
                              leading=20, borderPad=0)
    s['h3'] = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11,
                              textColor=MUTED, spaceAfter=4, spaceBefore=10,
                              leading=16)
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=10,
                                textColor=TEXT, spaceAfter=6, leading=16,
                                wordWrap='CJK')
    s['bullet'] = ParagraphStyle('bullet', fontName='Helvetica', fontSize=10,
                                  textColor=TEXT, spaceAfter=3, leading=15,
                                  leftIndent=16, bulletIndent=4,
                                  wordWrap='CJK')
    s['sub_bullet'] = ParagraphStyle('sub_bullet', fontName='Helvetica', fontSize=10,
                                      textColor=TEXT, spaceAfter=3, leading=15,
                                      leftIndent=32, bulletIndent=20,
                                      wordWrap='CJK')
    s['code'] = ParagraphStyle('code', fontName='Courier', fontSize=9,
                                textColor=TEXT, spaceAfter=4, leading=14,
                                backColor=colors.HexColor('#F5EDE4'),
                                leftIndent=10, rightIndent=10,
                                borderPad=6)
    s['blockquote'] = ParagraphStyle('blockquote', fontName='Helvetica-Oblique',
                                      fontSize=10, textColor=MUTED,
                                      leftIndent=16, spaceAfter=6, leading=15,
                                      borderColor=ACCENT, borderWidth=2,
                                      borderPad=6)
    s['footer'] = ParagraphStyle('footer', fontName='Helvetica', fontSize=8,
                                  textColor=MUTED, alignment=TA_CENTER)
    return s


def inline_fmt(text):
    """Convert inline markdown (**bold**, `code`) to ReportLab markup."""
    # bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # inline code
    text = re.sub(r'`([^`]+)`', r'<font name="Courier" color="#C8843A">\1</font>', text)
    # escape ampersands that are not already entities
    text = re.sub(r'&(?!amp;|lt;|gt;|#)', '&amp;', text)
    return text


def parse_table(lines):
    """Parse markdown table lines into a list of rows."""
    rows = []
    for line in lines:
        if re.match(r'\s*\|[-:\s|]+\|\s*$', line):
            continue  # separator row
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cells)
    return rows


def build_table_flowable(rows, styles):
    if not rows:
        return None
    col_count = max(len(r) for r in rows)
    # Pad rows
    padded = [r + [''] * (col_count - len(r)) for r in rows]
    # Convert cells to Paragraphs
    data = []
    for ri, row in enumerate(padded):
        r_data = []
        for cell in row:
            st = ParagraphStyle('tc_h' if ri == 0 else 'tc',
                                 fontName='Helvetica-Bold' if ri == 0 else 'Helvetica',
                                 fontSize=9, textColor=TEXT if ri > 0 else colors.white,
                                 leading=13, wordWrap='CJK')
            r_data.append(Paragraph(inline_fmt(cell), st))
        data.append(r_data)

    avail_w = W - 4 * cm
    col_w = avail_w / col_count

    ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG]),
        ('GRID',       (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING',  (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
    ])
    t = Table(data, colWidths=[col_w] * col_count)
    t.setStyle(ts)
    return t


def md_to_flowables(md_text, styles):
    flowables = []
    lines = md_text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]

        # Blank line
        if not line.strip():
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        # HR ---
        if re.match(r'^---+\s*$', line):
            flowables.append(Spacer(1, 4))
            flowables.append(HRFlowable(width='100%', thickness=1, color=BORDER))
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        # Heading 1
        if line.startswith('# '):
            text = line[2:].strip()
            flowables.append(Paragraph(inline_fmt(text), styles['h1']))
            i += 1
            continue

        # Heading 2
        if line.startswith('## '):
            text = line[3:].strip()
            flowables.append(Paragraph(inline_fmt(text), styles['h2']))
            i += 1
            continue

        # Heading 3
        if line.startswith('### '):
            text = line[4:].strip()
            flowables.append(Paragraph(inline_fmt(text), styles['h3']))
            i += 1
            continue

        # Code block
        if line.strip().startswith('```'):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            code_text = '\n'.join(code_lines)
            flowables.append(Preformatted(code_text, styles['code']))
            flowables.append(Spacer(1, 4))
            continue

        # Table
        if line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            rows = parse_table(table_lines)
            t = build_table_flowable(rows, styles)
            if t:
                flowables.append(Spacer(1, 4))
                flowables.append(t)
                flowables.append(Spacer(1, 8))
            continue

        # Blockquote
        if line.startswith('> '):
            text = line[2:].strip()
            flowables.append(Paragraph(inline_fmt(text), styles['blockquote']))
            i += 1
            continue

        # Sub-bullet (starts with spaces + -)
        if re.match(r'^   +- ', line):
            text = re.sub(r'^   +- ', '', line).strip()
            flowables.append(Paragraph('&bull;  ' + inline_fmt(text), styles['sub_bullet']))
            i += 1
            continue

        # Bullet
        if line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            flowables.append(Paragraph('&bull;  ' + inline_fmt(text), styles['bullet']))
            i += 1
            continue

        # Numbered list
        m = re.match(r'^(\d+)\. (.+)', line)
        if m:
            num, text = m.group(1), m.group(2).strip()
            flowables.append(Paragraph(
                f'<b>{num}.</b>  {inline_fmt(text)}', styles['bullet']))
            i += 1
            continue

        # Normal paragraph
        flowables.append(Paragraph(inline_fmt(line), styles['body']))
        i += 1

    return flowables


def add_header_footer(canvas, doc):
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(2*cm, H - 1.5*cm, W - 2*cm, H - 1.5*cm)
    # Brand in header
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(ACCENT)
    canvas.drawString(2*cm, H - 1.2*cm, 'Confei')
    # Page number
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(W - 2*cm, 1.2*cm, f'Página {doc.page}')
    canvas.restoreState()


def convert(md_path, pdf_path, title):
    styles = make_styles()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title=title,
        author='Confei'
    )

    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    story = md_to_flowables(md, styles)
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f'Gerado: {pdf_path}')


if __name__ == '__main__':
    convert('manual-admin.md',       'manual-admin.pdf',       'Confei — Manual da Administradora')
    convert('manual-testadoras.md',  'manual-testadoras.pdf',  'Confei — Guia das Testadoras Beta')
