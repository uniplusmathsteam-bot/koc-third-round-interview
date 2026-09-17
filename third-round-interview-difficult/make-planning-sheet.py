"""Builds the one-page planning sheet the candidate fills in before building.

Run: python make-planning-sheet.py
Output: "Special Lines Tool - Planning Sheet.docx" beside this script.

Everything is sized to stay on a single A4 page, so if you add a question,
drop a writing line somewhere else.
"""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

INK = RGBColor(0x16, 0x21, 0x1D)
MUTED = RGBColor(0x5E, 0x6B, 0x65)
GREEN = RGBColor(0x0B, 0x6B, 0x53)
RULE = "C9C4B8"
BOX = "D9D6CC"

SANS = "Aptos"
SERIF = "Georgia"


def run(paragraph, text, *, size=10, bold=False, italic=False, color=MUTED,
        font=SANS, spacing=None):
    r = paragraph.add_run(text)
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    if spacing is not None:
        # Letter-spacing, in twentieths of a point.
        r._element.get_or_add_rPr().append(
            _el("w:spacing", {"w:val": str(int(spacing * 20))})
        )
    # East Asian font, so the Chinese glyphs do not fall back to a serif.
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft JhengHei")
    return r


def _el(tag, attrs=None):
    element = OxmlElement(tag)
    for key, value in (attrs or {}).items():
        element.set(qn(key), value)
    return element


def spacing(paragraph, *, before=0, after=0, line=None):
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    if line is not None:
        fmt.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        fmt.line_spacing = Pt(line)
    return paragraph


def rule_below(paragraph, color=RULE):
    """Draws a writing rule under a paragraph.

    Word treats a run of paragraphs carrying identical borders as one group and
    suppresses the internal edges, so a bottom border alone only draws under the
    last line of a box. "between" is the edge it uses inside the group.
    """
    borders = _el("w:pBdr")
    edge = {"w:val": "single", "w:sz": "6", "w:space": "1", "w:color": color}
    borders.append(_el("w:bottom", edge))
    borders.append(_el("w:between", edge))
    paragraph._p.get_or_add_pPr().append(borders)
    return paragraph


def writing_line(container, *, height=19, gap=7, color=RULE):
    """An empty paragraph with a rule under it, for writing on."""
    paragraph = container.add_paragraph()
    spacing(paragraph, after=gap, line=height)
    return rule_below(paragraph, color)


def shade(cell, fill):
    cell._tc.get_or_add_tcPr().append(_el("w:shd", {
        "w:val": "clear", "w:color": "auto", "w:fill": fill,
    }))


def cell_margins(cell, *, top=80, left=140, bottom=80, right=140):
    margins = _el("w:tcMar")
    for side, value in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        margins.append(_el(f"w:{side}", {"w:w": str(value), "w:type": "dxa"}))
    cell._tc.get_or_add_tcPr().append(margins)


def box(document, width_mm, *, fill=None, border=BOX):
    """A one-cell table used as a bordered panel."""
    table = document.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Mm(width_mm)

    borders = _el("w:tblBorders")
    for side in ("top", "left", "bottom", "right"):
        borders.append(_el(f"w:{side}", {
            "w:val": "single", "w:sz": "8", "w:space": "0", "w:color": border,
        }))
    borders.append(_el("w:insideH", {"w:val": "none"}))
    borders.append(_el("w:insideV", {"w:val": "none"}))
    table._tbl.tblPr.append(borders)

    if fill:
        shade(cell, fill)
    cell_margins(cell)

    # The cell arrives with one empty paragraph; reuse it for the first line.
    cell.paragraphs[0]._p.getparent().remove(cell.paragraphs[0]._p)
    return cell


def question(document, width_mm, number, title_en, title_zh, guidance, *,
             lead=None, lines=5):
    cell = box(document, width_mm)

    heading = cell.add_paragraph()
    spacing(heading, after=1, line=15)
    run(heading, f"{number} · ", size=11, bold=True, color=GREEN)
    run(heading, title_en, size=11, bold=True, color=INK)

    chinese = cell.add_paragraph()
    spacing(chinese, after=3, line=14)
    run(chinese, title_zh, size=9, bold=True, color=GREEN)

    hint = cell.add_paragraph()
    spacing(hint, after=8, line=12)
    run(hint, guidance, size=8.5, italic=True, color=MUTED)

    if lead:
        prompt = cell.add_paragraph()
        spacing(prompt, after=4, line=19)
        run(prompt, lead, size=10.5, color=INK, font=SERIF)
        rule_below(prompt)
        lines -= 1

    for index in range(lines):
        writing_line(cell, gap=4 if index < lines - 1 else 1)

    gap = document.add_paragraph()
    spacing(gap, line=6)
    return cell


def build(path):
    document = Document()

    section = document.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(13)
    section.bottom_margin = Mm(12)
    section.left_margin = Mm(17)
    section.right_margin = Mm(17)
    width_mm = 210 - 17 - 17

    style = document.styles["Normal"]
    style.font.name = SANS
    style.font.size = Pt(10)
    style.font.color.rgb = INK

    eyebrow = document.add_paragraph()
    spacing(eyebrow, after=2, line=12)
    run(eyebrow, "UNIPLUS EDUCATION · KOC FINAL ROUND · DIFFICULT", size=8,
        bold=True, color=GREEN, spacing=1.1)

    title = document.add_paragraph()
    spacing(title, after=2, line=26)
    run(title, "Interactive Tool — Planning Sheet", size=21, color=INK, font=SERIF)

    subtitle = document.add_paragraph()
    spacing(subtitle, after=10, line=13)
    run(subtitle, "Topic: Special Lines and Centres · S3 JM28 (QUE)  |  10 minutes  |  "
                  "Fill this in before you open Cursor, and hand it in with your HTML file.",
        size=9, color=MUTED)

    # Name and date on one line, as a borderless two-column table.
    details = document.add_table(rows=1, cols=2)
    details.autofit = False
    for cell, label in zip(details.row_cells(0), ("Name  姓名", "Date  日期")):
        cell.width = Mm(width_mm / 2)
        cell_margins(cell, top=0, left=0, bottom=40, right=140)
        paragraph = cell.paragraphs[0]
        spacing(paragraph, line=17)
        run(paragraph, f"{label}  ", size=9, bold=True, color=MUTED)
        run(paragraph, " " * 40, size=9, color=MUTED)
        borders = _el("w:pBdr")
        borders.append(_el("w:bottom", {
            "w:val": "single", "w:sz": "6", "w:space": "2", "w:color": RULE,
        }))
        paragraph._p.get_or_add_pPr().append(borders)

    gap = document.add_paragraph()
    spacing(gap, line=8)

    question(
        document, width_mm, "1", "The idea of the tool", "工具的構思",
        "Summarise it in two or three sentences. What does the student see, and what do "
        "they actually do? “The student drags…”, “the student picks…”, “then the tool…”.",
        lines=5,
    )

    question(
        document, width_mm, "2", "What result do you want this tool to achieve?",
        "你想這個工具達到什麼結果？",
        "One specific thing about special lines or centres — not “understand centres better”. "
        "Finish the sentence, then say how you would know a student had got there.",
        lead="After using this tool, a student can",
        lines=5,
    )

    question(
        document, width_mm, "3", "How is this better than teaching with pen and paper?",
        "這樣比用紙筆教好在哪裡？",
        "Name the one thing your tool does that a teacher with a whiteboard cannot do as "
        "well, and why that matters for this topic. “The same, but on a screen” is not an answer.",
        lines=5,
    )

    footer = box(document, width_mm, fill="F1F5EF", border="CBD9CF")
    line = footer.add_paragraph()
    spacing(line, after=0, line=13)
    run(line, "Before you hand this in:  ", size=8.5, bold=True, color=GREEN)
    run(line, "the idea fits in 50 minutes  ·  the student has to commit to an answer  ·  "
              "the tool says why an answer is wrong  ·  you checked the geometry yourself — "
              "the JM28 QUE set has no answer key",
        size=8.5, color=MUTED)

    document.save(path)
    return path


if __name__ == "__main__":
    out = Path(__file__).with_name("Special Lines Tool - Planning Sheet.docx")
    print("wrote", build(out))
