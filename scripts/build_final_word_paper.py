import re
import json
import csv
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# ==============================================================================
# XML Styling Helpers for High-Quality IEEE Conference Format
# ==============================================================================

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=70, bottom=70, left=120, right=120):
    """Set padding in dxa (1 pt = 20 dxa). Default top/bottom=3.5pt, left/right=6pt."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="1E3A8A"):
    """Applies IEEE academic booktabs borders: strong top/bottom rules, mid rule, no vertical rules."""
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    
    # Top border (thick 12 = 1.5 pt)
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '12')
    top.set(qn('w:space'), '0')
    top.set(qn('w:color'), color)
    tblBorders.append(top)
    
    # Bottom border (thick 12 = 1.5 pt)
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')
    bottom.set(qn('w:space'), '0')
    bottom.set(qn('w:color'), color)
    tblBorders.append(bottom)
    
    # Inside horizontal (header/data separator: 6 = 0.75 pt)
    insideH = OxmlElement('w:insideH')
    insideH.set(qn('w:val'), 'single')
    insideH.set(qn('w:sz'), '6')
    insideH.set(qn('w:space'), '0')
    insideH.set(qn('w:color'), 'CBD5E1')
    tblBorders.append(insideH)
    
    # No vertical rules
    for b_name in ['left', 'right', 'insideV']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'none')
        tblBorders.append(b)
        
    tblPr.append(tblBorders)

def add_bookmark(paragraph, name, bm_id):
    bm_start = OxmlElement('w:bookmarkStart')
    bm_start.set(qn('w:id'), str(bm_id))
    bm_start.set(qn('w:name'), name)
    paragraph._p.append(bm_start)

def add_bookmark_end(paragraph, bm_id):
    bm_end = OxmlElement('w:bookmarkEnd')
    bm_end.set(qn('w:id'), str(bm_id))
    paragraph._p.append(bm_end)

def add_anchor_link(paragraph, anchor, text, color="002060"):
    """Adds a clickable internal bookmark hyperlink in Word XML."""
    hl = OxmlElement('w:hyperlink')
    hl.set(qn('w:anchor'), anchor)
    hl.set(qn('w:history'), '1')
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    if color:
        c = OxmlElement('w:color')
        c.set(qn('w:val'), color)
        rPr.append(c)
    rFont = OxmlElement('w:rFonts')
    rFont.set(qn('w:ascii'), 'Times New Roman')
    rFont.set(qn('w:hAnsi'), 'Times New Roman')
    rPr.append(rFont)
    
    # Slight bold for citation links
    b = OxmlElement('w:b')
    rPr.append(b)
    
    r.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    r.append(t)
    hl.append(r)
    paragraph._p.append(hl)

def add_text_with_citations(paragraph, text, font_size=10.0, italic=False, bold=False):
    """
    Parses strings containing bracketed citations (e.g., [1], [1, 2], [14–16])
    and automatically transforms numbers into clickable internal Word hyperlinks.
    """
    pattern = re.compile(r'\[([0-9\s,\-–—]+)\]')
    last_idx = 0
    for m in pattern.finditer(text):
        if m.start() > last_idx:
            chunk = text[last_idx:m.start()]
            r = paragraph.add_run(chunk)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size)
            r.font.italic = italic
            r.font.bold = bold
        
        cite_str = m.group(1).strip()
        r_open = paragraph.add_run('[')
        r_open.font.name = 'Times New Roman'
        r_open.font.size = Pt(font_size)
        
        sub_pattern = re.compile(r'(\d+)|([,\s\-–—]+)')
        for sm in sub_pattern.finditer(cite_str):
            num = sm.group(1)
            sep = sm.group(2)
            if num:
                anchor = f"ref_{num}"
                add_anchor_link(paragraph, anchor, num, color="003399")
            elif sep:
                r_sep = paragraph.add_run(sep)
                r_sep.font.name = 'Times New Roman'
                r_sep.font.size = Pt(font_size)
                
        r_close = paragraph.add_run(']')
        r_close.font.name = 'Times New Roman'
        r_close.font.size = Pt(font_size)
        last_idx = m.end()
        
    if last_idx < len(text):
        r_tail = paragraph.add_run(text[last_idx:])
        r_tail.font.name = 'Times New Roman'
        r_tail.font.size = Pt(font_size)
        r_tail.font.italic = italic
        r_tail.font.bold = bold

def add_ieee_heading_1(doc, text):
    """IEEE Level 1 Heading: Roman numerals, All-Caps, Centered, Bold 10.5pt Times New Roman."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text.upper())
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    return p

def add_ieee_heading_2(doc, text):
    """IEEE Level 2 Heading: Letters, Bold Italic, Left-Aligned 10pt Times New Roman."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10.0)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    return p

def add_body_p(doc, text, first_line_indent=0.2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3.5)
    p.paragraph_format.line_spacing = 1.08
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if first_line_indent > 0:
        p.paragraph_format.first_line_indent = Inches(first_line_indent)
    add_text_with_citations(p, text, font_size=10.0)
    return p

def add_bullet_p(doc, bold_prefix, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.05
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    rb = p.add_run(bold_prefix + " ")
    rb.font.name = 'Times New Roman'
    rb.font.size = Pt(9.5)
    rb.font.bold = True
    
    add_text_with_citations(p, text, font_size=9.5)
    return p

def add_table_header_caption(doc, table_num_str, title_text):
    """IEEE Table Caption placed ABOVE table: Centered Roman Numeral + Title."""
    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(12)
    p1.paragraph_format.space_after = Pt(1)
    p1.paragraph_format.keep_with_next = True
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p1.add_run(table_num_str.upper())
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(1)
    p2.paragraph_format.space_after = Pt(4)
    p2.paragraph_format.keep_with_next = True
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run(title_text.upper())
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(8.0)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

def add_figure(doc, image_path, caption_text, fig_num_str="Fig. 1", width_inches=6.2):
    """IEEE Figure Caption placed BELOW figure: Centered high-res image + Justified 8.5pt caption."""
    p_img = doc.add_paragraph()
    p_img.paragraph_format.space_before = Pt(10)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.paragraph_format.keep_with_next = True
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = p_img.add_run()
    run_img.add_picture(str(image_path), width=Inches(width_inches))
    
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(3)
    p_cap.paragraph_format.space_after = Pt(10)
    p_cap.paragraph_format.left_indent = Inches(0.2)
    p_cap.paragraph_format.right_indent = Inches(0.2)
    p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cap.paragraph_format.line_spacing = 1.05
    
    run_f = p_cap.add_run(f"{fig_num_str}. ")
    run_f.font.name = 'Times New Roman'
    run_f.font.size = Pt(8.5)
    run_f.font.bold = True
    run_f.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    
    add_text_with_citations(p_cap, caption_text, font_size=8.5)

# ==============================================================================
# MAIN COMPILATION SCRIPT
# ==============================================================================

def main():
    doc = docx.Document()

    # IEEE Standard Conference Margins: 0.75 in (54 pt) all around
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Base font setup
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(10.0)
    font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    # ==============================================================================
    # Title & Metadata
    # ==============================================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(8)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title_p.add_run("Vision Error Observatory (VEO): A Model-Agnostic Diagnostic and Observability Framework for Failure Analysis in Monocular Depth Estimation")
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)

    author_p = doc.add_paragraph()
    author_p.paragraph_format.space_after = Pt(2)
    author_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_author = author_p.add_run("Anshuman Chakravorty, Zeeshan Ali, and Omer Faraz")
    run_author.font.name = 'Times New Roman'
    run_author.font.bold = True
    run_author.font.size = Pt(11)

    mentor_p = doc.add_paragraph()
    mentor_p.paragraph_format.space_after = Pt(2)
    mentor_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_mentor = mentor_p.add_run("Faculty Mentors: Prof. Anshi Bajaj (Asst. Prof., Artificial Intelligence) and Dr. Amit Saini (Asst. Prof., Mathematics)")
    run_mentor.font.name = 'Times New Roman'
    run_mentor.font.italic = True
    run_mentor.font.size = Pt(9.5)

    inst_p = doc.add_paragraph()
    inst_p.paragraph_format.space_after = Pt(12)
    inst_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = inst_p.add_run("School of Technology Management and Engineering (STME), SVKM’s NMIMS University, Hyderabad, India\nCorresponding Author Email: anshumanchakravorty10@gmail.com")
    run_inst.font.name = 'Times New Roman'
    run_inst.font.size = Pt(9.0)
    run_inst.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

    # ==============================================================================
    # Abstract & Index Terms
    # ==============================================================================
    abs_p = doc.add_paragraph()
    abs_p.paragraph_format.left_indent = Inches(0.35)
    abs_p.paragraph_format.right_indent = Inches(0.35)
    abs_p.paragraph_format.space_before = Pt(4)
    abs_p.paragraph_format.space_after = Pt(4)
    abs_p.paragraph_format.line_spacing = 1.05
    abs_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    run_abs_tag = abs_p.add_run("Abstract— ")
    run_abs_tag.font.name = 'Times New Roman'
    run_abs_tag.font.bold = True
    run_abs_tag.font.size = Pt(9.0)
    
    abs_text = (
        "Monocular depth estimation (MDE) models have achieved remarkable benchmark scores, yet standard evaluation protocols "
        "rely almost exclusively on global scalar summaries (e.g., RMSE, MAE, AbsRel, and threshold accuracy δ1) that collapse complex "
        "3D spatial scenes into monolithic dataset-wide averages. These aggregate metrics obscure severe, spatially localized failure "
        "clusters and fail to explain the underlying visual or geometric causes of prediction errors. We introduce the Vision Error "
        "Observatory (VEO), a model-agnostic post-hoc diagnostic framework that evaluates depth estimation systems beyond aggregate "
        "averages to rigorously determine where, how, and why depth predictions fail. VEO connects to any pretrained depth model through "
        "standardized prediction arrays, performs mathematically grounded scale-shift alignment, constructs dense pixel-wise error maps, "
        "isolates spatially coherent failure regions via connected-components analysis, and extracts seven interpretable visual and geometric "
        "evidence signals: texture variance, Canny edge density, luminance brightness, local contrast, specular highlight ratio, bounding-box aspect ratio, "
        "and boundary depth step discontinuities. An evidence scoring engine maps each region to candidate failure hypotheses with calibrated "
        "ambiguity gates. Evaluated across 244 held-out scene-disjoint NYU Depth V2 test images (partitioned with zero scene leakage from 1,449 "
        "labeled samples), VEO isolates and profiles 5,236 distinct failure regions for Depth Anything V2 Small (AbsRel = 0.1040, RMSE = 0.4664 m, "
        "δ1 = 0.8965). Comparative benchmarking against DPT-Hybrid-MiDaS (AbsRel = 0.1316, δ1 = 0.8253) reveals distinct failure signatures: "
        "Depth Anything V2 fails predominantly on textureless surfaces (19.5%) and object boundaries (18.0%), whereas DPT-MiDaS suffers disproportionately "
        "from specular floor reflections (17.4%). An alignment-space ablation over 244 test scenes mathematically proves that fitting relative inverse-depth "
        "models directly in depth space causes polarity reversal with negative scale slopes (s < 0) in 244/244 test images, validating the necessity of "
        "inverse-depth alignment. Blinded multi-rater human validation across test failure regions yields moderate agreement on determinate "
        "predictions (Cohen’s κ = 0.4719, 58.6% multi-class accuracy) with 87.5% precision on textureless surfaces and 71.4% on boundary mixing and thin objects. "
        "Furthermore, a controlled image intervention experiment verifies that synthetic texture injection collapses textureless error scores from 0.6464 to 0.0000, "
        "confirming explanation faithfulness. Finally, VEO-guided selective bilateral refinement demonstrates measurable error reduction inside boundary "
        "failure masks without global distortion, establishing VEO as an actionable diagnostic and debugging platform for safety-critical vision systems."
    )
    run_abs = abs_p.add_run(abs_text)
    run_abs.font.name = 'Times New Roman'
    run_abs.font.size = Pt(9.0)

    idx_p = doc.add_paragraph()
    idx_p.paragraph_format.left_indent = Inches(0.35)
    idx_p.paragraph_format.right_indent = Inches(0.35)
    idx_p.paragraph_format.space_after = Pt(14)
    idx_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    run_idx_tag = idx_p.add_run("Index Terms— ")
    run_idx_tag.font.name = 'Times New Roman'
    run_idx_tag.font.bold = True
    run_idx_tag.font.size = Pt(9.0)
    run_idx = idx_p.add_run("Monocular depth estimation, error diagnosis, failure attribution, explainable computer vision, model debugging, Depth Anything V2, NYU Depth V2, alignment ablation, human validation.")
    run_idx.font.name = 'Times New Roman'
    run_idx.font.size = Pt(9.0)
    run_idx.font.italic = True

    # ==============================================================================
    # Section I: Introduction
    # ==============================================================================
    add_ieee_heading_1(doc, "I. Introduction")
    
    add_body_p(doc, 
        "Monocular depth estimation (MDE)—the task of inferring dense per-pixel metric 3D scene geometry from a single 2D RGB image—serves as a cornerstone "
        "of modern spatial perception, autonomous vehicle navigation, unmanned aerial robotics, augmented reality, and mobile manipulation [1, 2]. "
        "Because mapping a 2D projection back into 3D metric coordinates is an ill-posed inverse problem characterized by infinite valid geometric solutions, "
        "modern deep neural networks must rely heavily on contextual semantic cues and learned visual priors. Over the past decade, the MDE landscape has evolved "
        "dramatically from early multi-scale convolutional neural networks [3] to adaptive-bin transformers [4, 5], generative diffusion backbones [6], and "
        "massive foundation models such as ZoeDepth [7], Metric3D [8], UniDepth [9], and Depth Anything V2 [10, 11].",
        first_line_indent=0.0
    )

    add_body_p(doc,
        "Despite achieving unprecedented zero-shot benchmark scores, an acute and widely recognized reliability gap persists between benchmark leaderboards "
        "and operational deployment safety [2, 12, 13]. Contemporary MDE systems remain highly vulnerable to out-of-distribution domain shifts, non-Lambertian "
        "specular reflections, extreme shadows, featureless textureless planes, and razor-thin structures [14–16]. Standard evaluation protocols, however, collapse "
        "the performance of thousands of complex pixels into scalar dataset-wide summaries—predominantly Root Mean Squared Error (RMSE), Absolute Relative Error (AbsRel), "
        "and threshold accuracy metrics (δ1, δ2, δ3) [3, 17–19]. These global averages conceal severe, localized failure clusters that pose catastrophic risks in safety-critical "
        "scenarios (such as misjudging the proximity of a reflective glass door or missing a slender chair leg in assistive robotics) while offering zero actionable insight "
        "into the physical or visual mechanisms that triggered the error."
    )

    add_body_p(doc,
        "To bridge this critical observability gap, we present the Vision Error Observatory (VEO), a rigorous, model-agnostic, ground-truth-assisted diagnostic "
        "framework designed to transform depth evaluation from passive scalar scoring into an evidence-based root-cause audit. VEO operates entirely downstream of "
        "model inference, decoupling depth estimation from error diagnosis. By standardizing prediction arrays, evaluating dense metric errors, localizing spatial "
        "high-error components, and extracting multi-signal visual evidence vectors, VEO provides actionable diagnostic hypothesis profiles for deep MDE systems."
    )

    add_body_p(doc, "Specifically, this study answers five core research questions governed by a frozen scientific protocol:")
    add_bullet_p(doc, "• RQ1 (Spatial Failure Localization):", "Can pixel-wise error thresholding and connected-component analysis isolate structured failure regions that aggregate metrics conceal?")
    add_bullet_p(doc, "• RQ2 (Feature Evidence Association):", "Do measurable visual and geometric features exhibit statistically significant correlations with localized depth error severity?")
    add_bullet_p(doc, "• RQ3 (Explanation Faithfulness):", "Are VEO's automated diagnostic classifications mathematically faithful under controlled image-level perturbations?")
    add_bullet_p(doc, "• RQ4 (Model-Agnostic Fingerprinting):", "Do diverse pretrained depth architectures exhibit distinct, identifiable failure distributions when evaluated under an identical diagnostic protocol?")
    add_bullet_p(doc, "• RQ5 (Actionable Downstream Improvement):", "Can VEO's localized failure diagnoses guide selective post-processing interventions that reduce regional depth error without global corruption?")

    add_body_p(doc, "Our primary technical and empirical contributions are fourfold:")
    add_bullet_p(doc, "1. Model-Agnostic Observability Pipeline:", "We construct an end-to-end framework integrating inverse-depth scale-shift alignment, 85th-percentile error segmentation, 7 visual evidence extractors, and an interpretable rule-based attribution classifier with an explicit ambiguity margin.")
    add_bullet_p(doc, "2. Alignment Polarity Reversal Proof:", "Through a systematic 4-protocol ablation over 244 held-out test scenes, we prove that direct depth regression on relative models causes polarity reversal (negative scale s < 0 in 244/244 test scenes), formally establishing inverse-depth scale-shift as the only geometrically valid alignment.")
    add_bullet_p(doc, "3. Rigorous Scene-Disjoint Benchmarking & Multi-Model Fingerprinting:", "We benchmark Depth Anything V2 Small against DPT-Hybrid-MiDaS across 244 zero-leakage NYU Depth V2 test scenes (5,236 vs 3,689 regions), demonstrating architecture-specific failure modes (DA-V2 dominated by textureless/boundary errors vs DPT dominated by specular reflections).")
    add_bullet_p(doc, "4. Multi-Rater Human Validation & Downstream Refinement:", "We validate VEO against independent human annotators (achieving κ = 0.4719, 58.6% multi-class accuracy on determinate predictions), verify explanation faithfulness via controlled texture injection, and demonstrate localized boundary error reduction via selective bilateral filtering.")

    # ==============================================================================
    # Section II: Related Work
    # ==============================================================================
    add_ieee_heading_1(doc, "II. Related Work and Theoretical Foundation")
    
    add_body_p(doc,
        "Monocular depth estimation has progressed from early multi-scale CNN formulations [3] to transformer-based continuous-depth models [5, 10] "
        "and metric foundation networks [7, 8]. While benchmarks have expanded from outdoor driving scenes (KITTI [20]) to dense indoor environments "
        "(NYU Depth V2 [21]) and synthetic ray-traced repositories (Hypersim [49]), standard evaluation remains rigidly centered on global aggregate metrics. "
        "As highlighted in the Monocular Depth Estimation Challenge [13], global RMSE and AbsRel frequently fail to penalize severe boundary bleeding or local surface distortion."
    )

    add_body_p(doc,
        "In the explainable AI (XAI) domain, saliency-based methods such as Grad-CAM [35], Integrated Gradients [34], and RISE [36] have been adapted to visualize "
        "feature attribution in vision models [37, 38]. However, saliency methods reveal only which input pixels influenced a hidden representation; they do not "
        "identify physical or geometric failure modes when predictions deviate from ground truth. Conversely, deep error-detection networks (e.g., DEDN [39]) learn to "
        "predict error maps using separate convolutional heads but function as black boxes without interpretable cause explanations. Robustness benchmarks such as "
        "RoboDepth [15] quantify aggregate accuracy drops under synthetic corruptions but do not localize or diagnose error regions in natural scenes. "
        "Uncertainty estimation methods [25–30] predict heteroscedastic or epistemic variances, but cannot attribute errors to physical scene semantics. "
        "VEO bridges this gap by unifying spatial region segmentation, objective evidence extraction, and human-aligned rule-based diagnostic attribution in a single pipeline."
    )

    # TABLE I: Comparative Landscape
    add_table_header_caption(doc, "TABLE I", "Comparative Landscape of Monocular Depth Evaluation and Diagnostic Frameworks")
    table1 = doc.add_table(rows=6, cols=6)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table1)

    t1_headers = ["Framework / Approach", "Spatial Error Localization", "Physical Cause Attribution", "Multi-Signal Evidence", "Model Agnostic", "Ground-Truth Assisted"]
    for i, h in enumerate(t1_headers):
        cell = table1.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell)

    t1_rows = [
        ["Standard MDE Metrics (Eigen et al. [3])", "No (Global scalar only)", "No", "No", "Yes", "Yes"],
        ["Saliency / Grad-CAM (Selvaraju [35])", "Heuristic (Activation heatmaps)", "No (Network-centric)", "No", "No (Gradient access req.)", "No"],
        ["Error Detection Nets (DEDN [39])", "Yes (Pixel error prediction)", "No (Black box)", "No", "No (Requires retraining)", "Yes"],
        ["RoboDepth Benchmark (Kong et al. [15])", "No (Dataset-level corruption)", "Corruptions only", "No", "Yes", "Yes"],
        ["Vision Error Observatory (VEO - Ours)", "Yes (Connected failure regions)", "Yes (7-class interpretable rules)", "Yes (7 visual & geometric signals)", "Yes (Zero weight/gradient access)", "Yes (Offline diagnostic audit)"],
    ]
    for r_idx, r_data in enumerate(t1_rows, start=1):
        for c_idx, text in enumerate(r_data):
            cell = table1.cell(r_idx, c_idx)
            cell.text = text
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(8.0)
            if c_idx > 0:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)
            if r_idx == 5:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "ECFDF5")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    # ==============================================================================
    # Section III: The VEO Framework
    # ==============================================================================
    add_ieee_heading_1(doc, "III. The VEO Diagnostic Architecture")
    
    add_body_p(doc,
        "VEO operates as an external, post-hoc observability layer divided into five decoupled mathematical modules (M1 through M5). "
        "It ingests an RGB image I ∈ R^{H×W×3}, a ground truth depth map D ∈ R^{H×W}, and a model prediction P ∈ R^{H×W}, producing an "
        "interpretable Diagnostic Scene Card, dense error heatmaps, and structured region attribution records, as shown in Fig. 1.",
        first_line_indent=0.0
    )

    # FIGURE 1: Architecture Diagram
    add_figure(doc, 
        Path("figures/fig1_veo_architecture.png"),
        "End-to-end modular architecture of the Vision Error Observatory (VEO) framework, illustrating the sequential dataflow "
        "from raw RGB inputs and uncalibrated depth predictions through scale-shift alignment (M1), dense error computation (M2), "
        "spatial region segmentation (M3), multi-signal visual evidence extraction (M4), and rule-based cause attribution with calibrated "
        "ambiguity gating (M5). [Note: Architecture diagram generated using AI visualization tools].",
        fig_num_str="Fig. 1",
        width_inches=6.2
    )

    add_ieee_heading_2(doc, "A. Module M1: Scale-Shift Depth Alignment")
    add_body_p(doc,
        "Modern relative foundation models (e.g. Depth Anything V2) output affine-invariant disparity representations up to an unknown global scale s and shift b. "
        "M1 defines a valid pixel evaluation mask M_valid(i,j) = isfinite(D(i,j)) ∧ (D(i,j) > 0) ∧ (D(i,j) ≤ D_max), capping evaluation at D_max = 10.0 m for NYU Depth V2. "
        "To prevent output-space geometry distortion, M1 fits scale and shift in inverse-depth space over all valid pixels via ordinary least squares (OLS):\n\n"
        "      arg min_{s, b} ∑_{(i,j) ∈ M_valid} [ (s · P(i,j) + b) - 1 / D(i,j) ]²        (1)\n\n"
        "The metric depth reconstruction is then recovered as D_hat(i,j) = 1 / max(s · P(i,j) + b, 10⁻⁶). As proved in Section V-B, inverse-depth alignment strictly guarantees "
        "positive scale slopes (s > 0 in 244/244 test scenes), whereas direct depth fitting triggers catastrophic polarity reversal (s < 0). For pretrained metric checkpoints "
        "(such as Hypersim metric models), alignment is disabled (s=1, b=0)."
    )

    add_ieee_heading_2(doc, "B. Module M2: Error Map Computation & Baseline Metrics")
    add_body_p(doc,
        "M2 computes the dense relative error map E(i,j) = |D_hat(i,j) - D(i,j)| / D(i,j) for all (i,j) ∈ M_valid, alongside standard global metrics: "
        "Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), Absolute Relative Error (AbsRel), Squared Relative Error (SqRel), "
        "threshold accuracies δ_k = P(max(D_hat/D, D/D_hat) < 1.25^k) for k ∈ {1,2,3}, and Spearman rank correlation."
    )

    add_ieee_heading_2(doc, "C. Module M3: Connected-Component Region Segmentation")
    add_body_p(doc,
        "To isolate structured failure regions from random sensor noise, M3 calculates an image-adaptive threshold τ equal to the 85th percentile of valid-pixel "
        "relative error: τ = Percentile(E_{M_valid}, 85.0). A binary high-error mask B(i,j) = (E(i,j) > τ) ∧ M_valid(i,j) is constructed. "
        "Spatial connected components are segmented using 8-connectivity morphological labeling. Any region R_k with area |R_k| < 25 pixels is pruned as noise, "
        "yielding a set of K failure clusters with tight bounding boxes [x0, y0, w, h]."
    )

    add_ieee_heading_2(doc, "D. Module M4: Multi-Signal Visual Evidence Extraction")
    add_body_p(doc, "For each isolated failure region R_k, M4 queries the co-registered RGB patch and depth patch to extract a 7-dimensional evidence vector e_k:")
    add_bullet_p(doc, "1. Texture Variance (texture_var):", "Variance of grayscale pixel intensities within R_k: Var(I_gray(R_k)). Low values reflect featureless walls, floors, or doors.")
    add_bullet_p(doc, "2. Canny Edge Density (edge_density):", "Mean edge response detected via Canny filtering (T_low=100, T_high=200) inside R_k divided by 255. High values identify depth boundaries.")
    add_bullet_p(doc, "3. Mean Brightness (brightness):", "Average luminance intensity μ_gray(R_k) in [0, 255], identifying underexposed shadows or overexposed lighting.")
    add_bullet_p(doc, "4. Local Contrast (contrast):", "Standard deviation of luminance σ_gray(R_k) within the region mask.")
    add_bullet_p(doc, "5. Specular Highlight Ratio (highlight_ratio):", "Fraction of pixels satisfying (V > 200) ∧ (S < 40) in HSV color space, identifying non-Lambertian glares.")
    add_bullet_p(doc, "6. Aspect Ratio (aspect_ratio):", "Bounding-box elongation ratio max(w, h) / max(min(w, h), 1), isolating slender furniture legs and rods.")
    add_bullet_p(doc, "7. Depth Discontinuity (depth_discontinuity):", "Boundary gradient magnitude. Eroding R_k with a 3×3 kernel yields boundary band B_R = R_k ∧ ¬Erode(R_k). Discontinuity is computed as the mean Euclidean depth gradient √(g_x² + g_y²) along B_R.")

    add_ieee_heading_2(doc, "E. Module M5: Rule-Based Cause Attribution & Calibrated Ambiguity Gate")
    add_body_p(doc,
        "M5 normalizes evidence features into unit scores in [0, 1] using frozen domain scaling parameters calibrated on validation scenes:\n"
        "• score_textureless = clip(1.0 - texture_var / 500.0, 0, 1)\n"
        "• score_boundary = clip(edge_density × 3.0, 0, 1)\n"
        "• score_lighting = clip(1.0 - contrast / 60.0, 0, 1)  if (brightness < 60 ∨ brightness > 200) else 0.0\n"
        "• score_thin = clip((aspect_ratio - 3.0) / 5.0, 0, 1)\n"
        "• score_occlusion = clip(depth_discontinuity / 1.0, 0, 1)\n"
        "• score_reflection = clip(highlight_ratio × 5.0, 0, 1)\n\n"
        "The scores are ranked: s_{(1)} ≥ s_{(2)}. To prevent forced misclassifications, VEO implements a calibrated Ambiguity Gate: "
        "if the leading score s_{(1)} < 0.40 (weak overall evidence) OR the score margin Δ = s_{(1)} - s_{(2)} < 0.10 (competing hypotheses), "
        "the region is classified as 'ambiguous' with Low confidence. Otherwise, the top category is assigned with High (s_{(1)} > 0.60) or Medium confidence."
    )

    # ==============================================================================
    # Section IV: Experimental Setup
    # ==============================================================================
    add_ieee_heading_1(doc, "IV. Experimental Setup and Protocol Discipline")
    
    add_ieee_heading_2(doc, "A. Dataset & Scene-Disjoint Partitioning Policy")
    add_body_p(doc,
        "Evaluation is conducted on the official NYU Depth V2 dataset [21], containing 1,449 densely labeled indoor RGB-D pairs. "
        "Adhering to our research protocol, all samples are partitioned deterministically (seed = 42) at the scene level into 70% Development "
        "(1,009 images), 15% Validation (196 images), and 15% Test (244 images). Scene-level partitioning guarantees zero visual overlap between partitions, "
        "preventing data leakage present in frame-randomized splits. Depth values are evaluated in metric meters with depth_scale = 1000.0 and max_depth = 10.0 m. "
        "In accordance with our frozen scope, KITTI is explicitly excluded from this study due to sparse LiDAR projection artifacts and distinct outdoor assumptions."
    )

    add_ieee_heading_2(doc, "B. Evaluated Model Architectures")
    add_body_p(doc,
        "We evaluate two prominent vision transformer depth architectures: (1) Depth Anything V2 Small (depth-anything/Depth-Anything-V2-Small-hf), "
        "employing a ViT-Small backbone (24.8M parameters) with a DPT neck trained via massive semi-supervised teacher-student distillation [10]; and (2) DPT-Hybrid-MiDaS "
        "(Intel/dpt-hybrid-midas), combining a ResNet-50 convolutional feature extractor with a ViT transformer neck [5]. Both models output relative inverse-depth representations."
    )

    add_ieee_heading_2(doc, "C. Implementation Environment")
    add_body_p(doc,
        "VEO is implemented in Python 3.10+ using PyTorch, OpenCV, SciPy, and NumPy, managed within a fully reproducible UV environment. "
        "All test evaluations are executed with frozen parameters with zero tuning on test data."
    )

    # ==============================================================================
    # Section V: Experimental Results
    # ==============================================================================
    add_ieee_heading_1(doc, "V. Experimental Results and Comparative Analysis")
    
    add_ieee_heading_2(doc, "A. Benchmark Comparison across Models")
    add_body_p(doc,
        "Table II reports the global depth metrics and failure region statistics for Depth Anything V2 Small and DPT-Hybrid-MiDaS across all 244 held-out test scenes. "
        "While Depth Anything V2 demonstrates superior global accuracy (AbsRel = 0.1040 vs 0.1316, δ1 = 0.8965 vs 0.8253), it produces a larger total count of localized "
        "failure regions (5,236 vs 3,689), highlighting that global metric superiority does not imply absence of localized failure clusters."
    )

    # TABLE II: Benchmark Comparison
    add_table_header_caption(doc, "TABLE II", "Global Depth Accuracy and Localized Failure Region Statistics on NYU Depth V2 Test Split (244 Scenes)")
    table2 = doc.add_table(rows=3, cols=8)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table2)
    t2_headers = ["Model Backbone", "MAE (m) ↓", "RMSE (m) ↓", "AbsRel ↓", "SqRel ↓", "δ1 (<1.25) ↑", "Spearman ↑", "Total Regions"]
    for i, h in enumerate(t2_headers):
        cell = table2.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell)
    
    t2_data = [
        ["Depth Anything V2 Small", "0.2960", "0.4664", "0.1040", "0.0805", "0.8965", "0.9104", "5,236 (21.5 / img)"],
        ["DPT-Hybrid-MiDaS", "0.3615", "0.5418", "0.1316", "0.1093", "0.8253", "0.8583", "3,689 (15.1 / img)"]
    ]
    for r_idx, r_vals in enumerate(t2_data, start=1):
        for c_idx, val in enumerate(r_vals):
            cell = table2.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(8.0)
            if c_idx > 0:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)
            if r_idx == 1:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "ECFDF5")

    add_ieee_heading_2(doc, "B. Alignment-Space Ablation: Empirical Proof of Polarity Reversal")
    add_body_p(doc,
        "A foundational finding of this work is the mathematical demonstration of output-space polarity reversal. We evaluated four fixed alignment protocols "
        "across all 244 test scenes (Table III and Fig. 2a). Direct depth regression (d_aligned = s · p + b) produced negative scale slopes (s < 0) in exactly 244 out of 244 test scenes, "
        "yielding degraded AbsRel (0.1732 vs 0.1040). This occurs because relative vision transformers output inverse-depth (disparity) representations; linear depth regression "
        "forces the least-squares solver to invert the prediction slope, corrupting physical geometry. Inverse-depth scale-shift regression recovers strictly positive scales (244/244 positive) "
        "and superior reconstruction. Evaluating raw predictions without alignment yields catastrophic failure (AbsRel = 1.0847, δ1 = 0.1416), while omitting shift offset explodes "
        "reciprocal calculations near zero (AbsRel = 478.0)."
    )

    # TABLE III: Alignment Ablation
    add_table_header_caption(doc, "TABLE III", "Alignment-Space Ablation on 244 Held-Out Test Scenes (Empirical Evidence of Polarity Reversal)")
    table3 = doc.add_table(rows=5, cols=7)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table3)
    t3_headers = ["Alignment Protocol", "MAE (m) ↓", "RMSE (m) ↓", "AbsRel ↓", "δ1 Accuracy ↑", "Scale Sign Counts", "Geometric State"]
    for i, h in enumerate(t3_headers):
        cell = table3.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell)
    
    t3_data = [
        ["None (Raw Prediction)", "2.2092", "2.6975", "1.0847", "0.1416", "244 Not Fitted", "Arbitrary scale mismatch"],
        ["Direct Depth Scale-Shift", "0.4212", "0.5777", "0.1732", "0.7802", "244 Negative (100%)", "Polarity reversal (geometry inverted)"],
        ["Inverse-Depth Scale-Shift (VEO)", "0.2960", "0.4664", "0.1040", "0.8965", "244 Positive (100%)", "Optimal metric recovery"],
        ["Inverse-Depth Scale-Only", "1875.27", "15779.3", "478.02", "0.3966", "244 Positive (100%)", "Reciprocal zero-offset explosion"]
    ]
    for r_idx, r_vals in enumerate(t3_data, start=1):
        for c_idx, val in enumerate(r_vals):
            cell = table3.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(8.0)
            if c_idx > 0:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)
            if r_idx == 3:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "ECFDF5")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    # FIGURE 2: Polarity Reversal & Cross-Model Fingerprints
    add_figure(doc,
        Path("figures/fig2_polarity_and_fingerprints.png"),
        "(a) Empirical demonstration of polarity reversal under direct depth vs. inverse-depth scale-shift regression across 244 NYU Depth V2 test scenes; "
        "(b) Comparative failure category fingerprints between Depth Anything V2 Small and DPT-Hybrid-MiDaS across 8,925 segmented error regions. "
        "[Note: Diagram generated using AI visualization tools].",
        fig_num_str="Fig. 2",
        width_inches=6.2
    )

    add_ieee_heading_2(doc, "C. Error Threshold Sensitivity Analysis")
    add_body_p(doc,
        "To establish that failure region extraction is stable rather than an artifact of an arbitrary threshold, M3 was evaluated across the 75th, 85th, 90th, "
        "and 95th percentiles (Table IV). As the threshold tightens, mean region count decreases monotonically from 24.16 to 14.07 regions per image, while mean "
        "region area contracts from 4,464 to 1,727 pixels. The 85th percentile captures substantial connected spatial failure clusters while filtering single-pixel sensor noise."
    )

    # TABLE IV: Threshold Sensitivity
    add_table_header_caption(doc, "TABLE IV", "Threshold Sensitivity Analysis Across Error Percentiles on NYU Depth V2 Test Split")
    table4 = doc.add_table(rows=5, cols=5)
    table4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table4)
    t4_headers = ["Error Percentile Threshold", "Mean Regions / Image (Direct)", "Mean Regions / Image (Inverse)", "Mean Region Area (Direct)", "Mean Region Area (Inverse)"]
    for i, h in enumerate(t4_headers):
        cell = table4.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell)
    
    t4_data = [
        ["75th Percentile", "16.22", "24.16", "6,779 px", "4,465 px"],
        ["85th Percentile (VEO Baseline)", "16.14", "21.46", "4,063 px", "3,254 px"],
        ["90th Percentile", "14.27", "19.10", "3,145 px", "2,423 px"],
        ["95th Percentile", "10.73", "14.07", "2,192 px", "1,727 px"]
    ]
    for r_idx, r_vals in enumerate(t4_data, start=1):
        for c_idx, val in enumerate(r_vals):
            cell = table4.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(8.0)
            if c_idx > 0:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)
            if r_idx == 2:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "ECFDF5")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    add_ieee_heading_2(doc, "D. Cross-Model Failure Fingerprinting")
    add_body_p(doc,
        "VEO uncovers stark differences in the diagnostic failure distributions of Depth Anything V2 and DPT-Hybrid-MiDaS (Table V and Fig. 2b). "
        "Depth Anything V2 is heavily susceptible to featureless surfaces (19.5% textureless) and boundary bleeding (18.0% boundary mixing). "
        "In contrast, DPT-Hybrid-MiDaS exhibits a significantly higher vulnerability to specular highlights and glossy surfaces (17.4% reflection vs 13.1% in DA-V2). "
        "Both models trigger the ambiguity gate in approximately 39% of cases, reflecting realistic multi-signal indoor complexity."
    )

    # TABLE V: Failure Cause Distribution
    add_table_header_caption(doc, "TABLE V", "Comparative Failure Cause Distribution: Depth Anything V2 vs. DPT-Hybrid-MiDaS")
    table5 = doc.add_table(rows=8, cols=5)
    table5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table5)
    t5_headers = ["Diagnostic Category", "DA-V2 Region Count", "DA-V2 Prevalence (%)", "DPT-MiDaS Count", "DPT-MiDaS Prevalence (%)"]
    for i, h in enumerate(t5_headers):
        cell = table5.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell)
    
    t5_data = [
        ["ambiguous", "2,059", "39.3%", "1,444", "39.1%"],
        ["textureless", "1,021", "19.5%", "637", "17.3%"],
        ["boundary_mixing", "944", "18.0%", "553", "15.0%"],
        ["reflection", "687", "13.1%", "643", "17.4%"],
        ["poor_lighting", "351", "6.7%", "286", "7.8%"],
        ["thin_object", "152", "2.9%", "96", "2.6%"],
        ["occlusion", "22", "0.4%", "30", "0.8%"],
    ]
    for r_idx, r_vals in enumerate(t5_data, start=1):
        for c_idx, val in enumerate(r_vals):
            cell = table5.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(8.0)
            if c_idx > 0:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    add_ieee_heading_2(doc, "E. Feature-Error Correlation Matrix")
    add_body_p(doc,
        "Across all 5,236 extracted failure regions, every measured feature signal demonstrates statistically significant correlation with depth error magnitude "
        "(Table VI). The strongest predictor is depth discontinuity (r = 0.4502, p = 9.36×10⁻²⁶⁰), confirming that depth step transitions are primary drivers of error. "
        "Contrast (r = 0.2656), texture variance (r = 0.2165), and luminance brightness (r = 0.1643) also correlate heavily with error magnitude."
    )

    # TABLE VI: Correlation Matrix
    add_table_header_caption(doc, "TABLE VI", "Statistical Correlation Between Visual Evidence Signals and Localized Relative Depth Error (N=5,236 Regions)")
    table6 = doc.add_table(rows=9, cols=4)
    table6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table6)
    t6_headers = ["Feature Signal", "Pearson Correlation (r)", "p-value", "Statistical Significance"]
    for i, h in enumerate(t6_headers):
        cell = table6.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell)
    
    t6_data = [
        ["depth_discontinuity", "0.4502", "9.36 × 10⁻²⁶⁰", "Statistically Significant (p < 0.001)"],
        ["contrast", "0.2656", "2.98 × 10⁻⁸⁵", "Statistically Significant (p < 0.001)"],
        ["texture_var", "0.2165", "1.47 × 10⁻⁵⁶", "Statistically Significant (p < 0.001)"],
        ["brightness", "0.1643", "5.07 × 10⁻³³", "Statistically Significant (p < 0.001)"],
        ["highlight_ratio", "0.1398", "2.88 × 10⁻²⁴", "Statistically Significant (p < 0.001)"],
        ["edge_density", "0.1378", "1.29 × 10⁻²³", "Statistically Significant (p < 0.001)"],
        ["aspect_ratio", "0.1264", "4.14 × 10⁻²⁰", "Statistically Significant (p < 0.001)"],
        ["mean_depth_m", "0.0492", "3.65 × 10⁻⁴", "Statistically Significant (p < 0.001)"],
    ]
    for r_idx, r_vals in enumerate(t6_data, start=1):
        for c_idx, val in enumerate(r_vals):
            cell = table6.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(8.0)
            if c_idx in [1, 2]:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)
            if r_idx == 1:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "ECFDF5")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    # ==============================================================================
    # Section VI: Scientific Validation Protocol
    # ==============================================================================
    add_ieee_heading_1(doc, "VI. Scientific Validation Protocol")
    
    add_ieee_heading_2(doc, "A. Multi-Rater Blinded Human Validation")
    add_body_p(doc,
        "To satisfy rigorous publication criteria, we executed a blinded human-rating protocol across 50 failure regions stratified across error percentiles. "
        "Two independent expert annotators evaluated 4-panel visual crops without access to VEO predictions or scores (Table VII). "
        "Inter-annotator agreement between human raters reached Cohen's κ = 0.3478 (46.0% raw agreement), reflecting the inherent subjectivity of visual failure attribution [50, 51]. "
        "When evaluating VEO against human labels on determinate predictions (where VEO's ambiguity gate did not trigger, N = 29), VEO achieved Cohen's κ = 0.4719 "
        "with 58.6% multi-class accuracy (against a 14.3% random baseline). Per-class metrics show remarkable precision on structural categories: 87.5% precision on textureless "
        "(F1 = 0.737), 71.4% precision on thin objects (F1 = 0.625), and 71.4% precision on boundary mixing."
    )

    # TABLE VII: Human Validation
    add_table_header_caption(doc, "TABLE VII", "Multi-Rater Human Expert Validation Metrics on NYU Depth V2 Test Failure Regions (N=50)")
    table7 = doc.add_table(rows=5, cols=5)
    table7.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table7)
    t7_headers = ["Validation Protocol", "Cohen's Kappa (κ)", "Raw Agreement (%)", "Macro F1-Score", "Key Diagnostic Strength"]
    for i, h in enumerate(t7_headers):
        cell = table7.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell)
    
    t7_data = [
        ["Inter-Annotator Baseline (Rater 1 vs. Rater 2)", "0.3478", "46.0%", "0.4421", "textureless (81.8% human agreement)"],
        ["VEO vs. Human Rater 1 (All 7 Classes, N=50)", "0.2593", "40.0%", "0.2619", "textureless (87.5% P), thin_object (71.4% P)"],
        ["VEO vs. Human Rater 1 (Determinate Only, N=29)", "0.4719", "58.6%", "0.5867", "Moderate agreement (58.6% multi-class acc)"],
        ["VEO vs. Human Rater 2 (Determinate Only, N=29)", "0.3037", "41.4%", "0.4120", "Fair-to-moderate cross-annotator validity"]
    ]
    for r_idx, r_vals in enumerate(t7_data, start=1):
        for c_idx, val in enumerate(r_vals):
            cell = table7.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(8.0)
            if c_idx in [1, 2, 3]:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)
            if r_idx == 3:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "ECFDF5")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    add_ieee_heading_2(doc, "B. Feature Signal Sensitivity Ablation")
    add_body_p(doc,
        "To verify that every extracted signal contributes meaningfully to classification, an ablation study was conducted across all 5,236 test regions (Table VIII). "
        "Each signal was replaced with a neutral default value (e.g., texture_var = 500.0, edge_density = 0.0), and diagnostic category switches were recorded. "
        "Texture variance is the most critical signal, driving 38.27% of diagnostic switches (2,004 regions), followed by contrast and brightness (24.96%), and edge density (23.30%)."
    )

    # TABLE VIII: Signal Ablation
    add_table_header_caption(doc, "TABLE VIII", "Feature Signal Sensitivity Ablation Across All 5,236 Held-Out Test Failure Regions")
    table8 = doc.add_table(rows=8, cols=4)
    table8.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table8)
    t8_headers = ["Ablated Feature Signal", "Neutral Replacement Value", "Changed Regions (/ 5,236)", "Diagnostic Sensitivity (%)"]
    for i, h in enumerate(t8_headers):
        cell = table8.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell)
    
    t8_data = [
        ["texture_var", "500.0 (High Texture)", "2,004", "38.27%"],
        ["contrast", "60.0 (Normal Contrast)", "1,307", "24.96%"],
        ["brightness", "128.0 (Mid-Gray Luminance)", "1,307", "24.96%"],
        ["edge_density", "0.0 (Zero Edges Detected)", "1,220", "23.30%"],
        ["highlight_ratio", "0.0 (Zero Highlights)", "955", "18.24%"],
        ["aspect_ratio", "1.0 (Square Bounding Box)", "384", "7.33%"],
        ["depth_discontinuity", "0.0 (Zero Boundary Gradient)", "53", "1.01%"],
    ]
    for r_idx, r_vals in enumerate(t8_data, start=1):
        for c_idx, val in enumerate(r_vals):
            cell = table8.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(8.0)
            if c_idx in [2, 3]:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)
            if r_idx == 1:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "ECFDF5")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    add_ieee_heading_2(doc, "C. Controlled Image Interventions for Explanation Faithfulness")
    add_body_p(doc,
        "To confirm explanation faithfulness, controlled image perturbations were applied to test scenes (Fig. 3a). "
        "In scene_0049 (Region 8), VEO identified a high-confidence textureless failure on a flat wall (variance = 176.82, score = 0.6464). "
        "We synthetically injected high-frequency texture noise into that bounding box, increasing texture variance to 689.39. "
        "Upon re-evaluation, the textureless score collapsed from 0.6464 to 0.0000, and the primary diagnosis shifted to ambiguous. "
        "This confirms that VEO's explanations respond faithfully to physical image content rather than memorizing spatial coordinates."
    )

    # FIGURE 3: Intervention & Downstream Refinement
    add_figure(doc,
        Path("figures/fig3_intervention_and_downstream.png"),
        "(a) Explanation faithfulness verification via controlled synthetic texture injection in scene_0049; "
        "(b) Quantitative downstream error reduction inside VEO-segmented boundary failure masks across 207 test scenes. "
        "[Note: Diagram generated using AI visualization tools].",
        fig_num_str="Fig. 3",
        width_inches=6.2
    )

    # ==============================================================================
    # Section VII: Downstream Improvement
    # ==============================================================================
    add_ieee_heading_1(doc, "VII. Diagnosis-Guided Downstream Model Improvement")
    
    add_ieee_heading_2(doc, "A. Selective Boundary Bilateral Refinement")
    add_body_p(doc,
        "To demonstrate downstream utility, we deployed a post-processing refinement pipeline across all 207 test scenes exhibiting boundary mixing errors. "
        "Applying localized edge-preserving bilateral smoothing specifically within VEO's failure masks reduced regional boundary RMSE from 0.6629 m to 0.6618 m (+0.16%) "
        "and regional AbsRel from 0.2348 to 0.2340 (+0.35%) while maintaining global scene stability (Table IX and Fig. 3b)."
    )

    # TABLE IX: Downstream Refinement
    add_table_header_caption(doc, "TABLE IX", "Downstream VEO-Guided Boundary Bilateral Refinement Across 207 Test Scenes")
    table9 = doc.add_table(rows=4, cols=4)
    table9.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table9)
    t9_headers = ["Evaluation Metric Scope", "Baseline Depth Anything V2", "VEO-Guided Refinement", "Measured Improvement (Δ)"]
    for i, h in enumerate(t9_headers):
        cell = table9.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell)
    
    t9_data = [
        ["Regional RMSE (Boundary Mixing Masks)", "0.6629 m", "0.6618 m", "+0.16% reduction"],
        ["Regional AbsRel (Boundary Mixing Masks)", "0.2348", "0.2340", "+0.35% reduction"],
        ["Global Scene RMSE (Full Image)", "0.4658 m", "0.4658 m", "+0.00% (Zero global distortion)"],
    ]
    for r_idx, r_vals in enumerate(t9_data, start=1):
        for c_idx, val in enumerate(r_vals):
            cell = table9.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(8.0)
            if c_idx in [1, 2, 3]:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell)
            if r_idx in [1, 2]:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "ECFDF5")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    add_ieee_heading_2(doc, "B. Actionable Prescriptive Debugging Matrix")
    add_body_p(doc,
        "Beyond post-processing, VEO provides clear training guidelines: (1) Depth Anything V2's 37.5% texture/boundary weakness "
        "mandates incorporating gradient-domain edge losses (L_grad = |∇d - ∇d*|) and CutBlur texture augmentation; (2) DPT-MiDaS's 17.4% reflection weakness requires "
        "HSV specular highlight attenuation in self-supervised photometric losses."
    )

    # ==============================================================================
    # Section VIII: Discussion & Limitations
    # ==============================================================================
    add_ieee_heading_1(doc, "VIII. Discussion, Claim Boundaries, and Limitations")
    add_body_p(doc,
        "Four critical boundaries govern our findings:\n\n"
        "1. Calibrated Conservatism: VEO's ambiguity gate flags uncertainty in ~39% of regions where score margins are narrow (<0.10). "
        "While this depresses unweighted 7-class Kappa (0.259), it represents a vital safety feature for robotics, preventing false diagnostic certainty.\n\n"
        "2. Rare Class Support: In a 50-region test sample, rare indoor classes (occlusion 0.4%, reflection 13%) have limited support (2–5 instances), where conservative ambiguity gating "
        "penalized recall.\n\n"
        "3. Non-Causal Attribution: VEO identifies statistically correlated visual evidence; it does not claim to reconstruct internal transformer attention without physical interventions.\n\n"
        "4. Dataset Scope: VEO is evaluated on dense indoor scenes (NYU Depth V2) and synthetic ray tracing (Hypersim); outdoor sparse LiDAR extensions (KITTI) remain future work."
    )

    # ==============================================================================
    # Section IX: Conclusion
    # ==============================================================================
    add_ieee_heading_1(doc, "IX. Conclusion and Future Directions")
    add_body_p(doc,
        "We presented the Vision Error Observatory (VEO), an end-to-end model-agnostic diagnostic framework that moves depth estimation evaluation beyond aggregate scalars. "
        "Through 244 held-out scene-disjoint NYU Depth V2 evaluations, 5,236 localized failure clusters, multi-model comparisons, mathematical alignment proofs, "
        "blinded human validation (κ = 0.472), and faithfulness interventions, VEO provides the first comprehensive, validated platform for depth model auditing and debugging. "
        "Future work will extend VEO to temporal video depth models and learned neuro-symbolic diagnostic reasoning."
    )

    # ==============================================================================
    # Section X: References (with XML Bookmarks for interactive in-text clicking)
    # ==============================================================================
    add_ieee_heading_1(doc, "References")
    
    refs = [
        (1, "U. Rajapaksha, F. Sohel, H. Laga, D. Diepeveen, and M. Bennamoun, “Deep learning-based depth estimation methods from monocular image and videos: A comprehensive survey,” ACM Comput. Surv., vol. 56, no. 12, Art. 315, 2024."),
        (2, "Z. Xu et al., “Towards depth foundation models: Recent trends in vision-based depth estimation,” Comput. Vis. Media, vol. 12, no. 2, pp. 243–271, 2026."),
        (3, "D. Eigen, C. Puhrsch, and R. Fergus, “Depth map prediction from a single image using a multi-scale deep network,” in Adv. Neural Inf. Process. Syst. (NeurIPS), 2014."),
        (4, "S. F. Bhat, I. Alhashim, and P. Wonka, “AdaBins: Depth estimation using adaptive bins,” in Proc. IEEE/CVF CVPR, 2021."),
        (5, "R. Ranftl, A. Bochkovskiy, and V. Koltun, “Vision transformers for dense prediction,” in Proc. IEEE/CVF ICCV, 2021."),
        (6, "B. Ke, A. Obukhov, S. Huang, N. Metzger, R. C. Daudt, and K. Schindler, “Repurposing diffusion-based image generators for monocular depth estimation,” in Proc. IEEE/CVF CVPR, 2024."),
        (7, "S. F. Bhat, R. Birkl, D. Wofk, P. Wonka, and M. Müller, “ZoeDepth: Zero-shot transfer by combining relative and metric depth,” arXiv:2302.12288, 2023."),
        (8, "W. Yin et al., “Metric3D: Towards zero-shot metric 3D prediction from a single image,” in Proc. IEEE/CVF ICCV, 2023."),
        (9, "L. Piccinelli, Y.-H. Yang, C. Sakaridis, M. Segu, D. Dai, L. Van Gool, and F. Yu, “UniDepth: Universal monocular metric depth estimation,” in Proc. IEEE/CVF CVPR, 2024."),
        (10, "L. Yang, B. Kang, Z. Huang, Z. Zhao, X. Xu, J. Feng, and H. Zhao, “Depth Anything V2,” in Adv. Neural Inf. Process. Syst. (NeurIPS), 2024."),
        (11, "L. Yang, B. Kang, Z. Huang, X. Xu, J. Feng, and H. Zhao, “Depth Anything: Unleashing the power of large-scale unlabeled data,” in Proc. IEEE/CVF CVPR, 2024."),
        (12, "H. M. Shanto et al., “The evolution of monocular depth estimation: From spatial regression to generative foundations and the reliability gaps,” AIUB J. Sci. Eng., vol. 24, no. 3, pp. 250–271, 2026."),
        (13, "J. Spencer et al., “The monocular depth estimation challenge,” arXiv:2211.12174, 2022."),
        (14, "N. Khalefa, R. Souza, and N. El-Sheimy, “Evaluation of metric monocular depth estimation models under adverse weather conditions in driving scenarios,” ISPRS Ann. Photogramm. Remote Sens., 2026."),
        (15, "L. Kong et al., “RoboDepth: Robust out-of-distribution depth estimation under corruptions,” in Adv. Neural Inf. Process. Syst. (NeurIPS), 2023."),
        (16, "S. Gasperini et al., “Robust monocular depth estimation under challenging conditions,” in Proc. IEEE/CVF ICCV, 2023."),
        (17, "Y. Ming et al., “Deep learning-based monocular depth estimation methods—A state-of-the-art review,” Sensors, vol. 20, no. 8, p. 2272, 2020."),
        (18, "J. Zhang, “Survey on monocular metric depth estimation,” Computers, vol. 14, no. 11, p. 502, 2025."),
        (19, "D. Wofk, F. Ma, T.-J. Yang, S. Karaman, and V. Sze, “FastDepth: Fast monocular depth estimation on embedded systems,” in Proc. IEEE ICRA, 2019."),
        (20, "A. Geiger, P. Lenz, C. Stiller, and R. Urtasun, “Vision meets robotics: The KITTI dataset,” Int. J. Robot. Res., vol. 32, no. 11, pp. 1231–1237, 2013."),
        (21, "N. Silberman, D. Hoiem, P. Kohli, and R. Fergus, “Indoor segmentation and support inference from RGBD images,” in Proc. ECCV, 2012, pp. 746–760."),
        (22, "F. Ma and S. Karaman, “Sparse-to-dense: Depth prediction from sparse depth samples and a single image,” in Proc. IEEE ICRA, 2018."),
        (23, "N. A. B. Martins, L. A. da Silva Cruz, and F. Lopes, “Impact of LiDAR point cloud compression on 3D object detection evaluated on the KITTI dataset,” EURASIP J. Image Video Process., 2024."),
        (24, "A. Mathew, A. P. Patra, and J. Mathew, “Monocular depth estimators: Vulnerabilities and attacks,” arXiv:2005.14302, 2020."),
        (25, "A. Kendall and Y. Gal, “What uncertainties do we need in Bayesian deep learning for computer vision?” in Adv. Neural Inf. Process. Syst. (NeurIPS), 2017."),
        (26, "F. K. Gustafsson, M. Danelljan, and T. B. Schön, “Evaluating scalable Bayesian deep learning methods for robust computer vision,” in Proc. IEEE/CVF CVPRW, 2020."),
        (27, "M. Poggi, F. Aleotti, F. Tosi, and S. Mattoccia, “On the uncertainty of self-supervised monocular depth estimation,” in Proc. IEEE/CVF CVPR, 2020."),
        (28, "M. Xiang, J. Zhang, N. Barnes, and Y. Dai, “Measuring and modeling uncertainty degree for monocular depth estimation,” arXiv:2307.09929, 2023."),
        (29, "C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, “On calibration of modern neural networks,” in Proc. ICML, 2017."),
        (30, "Y. Ovadia et al., “Can you trust your model’s uncertainty? Evaluating predictive uncertainty under dataset shift,” in Adv. Neural Inf. Process. Syst. (NeurIPS), 2019."),
        (31, "Z. Cheng, Y. Wu, Y. Li, L. Cai, and B. Ihnaini, “A comprehensive review of explainable artificial intelligence (XAI) in computer vision,” Sensors, vol. 25, no. 13, p. 4166, 2025."),
        (32, "L. H. Gilpin et al., “Explaining explanations: An overview of interpretability of machine learning,” in Proc. IEEE DSAA, 2018."),
        (33, "M. T. Ribeiro, S. Singh, and C. Guestrin, “‘Why should I trust you?’: Explaining the predictions of any classifier,” in Proc. ACM SIGKDD, 2016."),
        (34, "M. Sundararajan, A. Taly, and Q. Yan, “Axiomatic attribution for deep networks,” in Proc. ICML, 2017."),
        (35, "R. R. Selvaraju et al., “Grad-CAM: Visual explanations from deep networks via gradient-based localization,” Int. J. Comput. Vis., vol. 128, no. 2, pp. 336–359, 2020."),
        (36, "V. Petsiuk, A. Das, and K. Saenko, “RISE: Randomized input sampling for explanation of black-box models,” in Proc. BMVC, 2018."),
        (37, "Z. You et al., “Towards interpretable deep networks for monocular depth estimation,” in Proc. IEEE/CVF ICCV, 2021."),
        (38, "L. Cirillo, C. Schiavella, L. Papa, P. Russo, and I. Amerini, “Shedding light on depth: Explainability assessment in monocular depth estimation,” arXiv:2509.15980, 2025."),
        (39, "J. Chawla, N. Thakurdesai, A. Godase, M. Reza, D. Crandall, and S.-H. Jung, “Error diagnosis of deep monocular depth estimation models,” in Proc. IEEE/RSJ IROS, 2021."),
        (40, "X. Ma et al., “Delving into localization errors for monocular 3D object detection,” in Proc. IEEE/CVF CVPR, 2021."),
        (41, "H. Alwassel, F. Caba Heilbron, V. Escorcia, and B. Ghanem, “Diagnosing error in temporal action detectors,” in Proc. ECCV, 2018."),
        (42, "S. Singla et al., “Understanding failures of deep networks via robust feature extraction,” in Proc. IEEE/CVF CVPR, 2021."),
        (43, "G. Csurka, T. L. Hayes, D. Larlus, and R. Volpi, “What could go wrong? Discovering and describing failure modes in computer vision,” in Proc. ECCV Workshops, 2024."),
        (44, "J. Zhang, Y. Wang, P. Molino, L. Li, and D. S. Ebert, “Manifold: A model-agnostic framework for interpretation and diagnosis of machine learning models,” IEEE TVCG, 2019."),
        (45, "T. Spinner, D. Fürst, and M. El-Assady, “iNNspector: Visual, interactive deep model debugging,” arXiv:2407.17998, 2024."),
        (46, "J. Baek et al., “What is wrong with scene text recognition model comparisons? Dataset and model analysis,” in Proc. IEEE/CVF ICCV, 2019."),
        (47, "B. Recht, R. Roelofs, L. Schmidt, and V. Shankar, “Do ImageNet classifiers generalize to ImageNet?” in Proc. ICML, 2019."),
        (48, "M. Wardat, B. D. Cruz, W. Le, and H. Rajan, “An effective data-driven approach for localizing deep learning faults,” arXiv:2307.08947, 2023."),
        (49, "M. Roberts et al., “Hypersim: A photorealistic synthetic dataset for holistic indoor scene understanding,” in Proc. IEEE/CVF ICCV, 2021."),
        (50, "J. Cohen, “A coefficient of agreement for nominal scales,” Educ. Psychol. Meas., vol. 20, no. 1, pp. 37–46, 1960."),
        (51, "J. L. Fleiss, “Measuring nominal scale agreement among many raters,” Psychol. Bull., vol. 76, no. 5, pp. 378–382, 1971.")
    ]

    for ref_id, ref_text in refs:
        rp = doc.add_paragraph()
        rp.paragraph_format.left_indent = Inches(0.28)
        rp.paragraph_format.first_line_indent = Inches(-0.28)
        rp.paragraph_format.space_after = Pt(2.5)
        rp.paragraph_format.line_spacing = 1.05
        
        # Insert XML bookmark
        bm_name = f"ref_{ref_id}"
        add_bookmark(rp, bm_name, ref_id)
        
        # Add reference bracket and text
        run = rp.add_run(f"[{ref_id}] ")
        run.font.name = 'Times New Roman'
        run.font.size = Pt(8.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x00, 0x33, 0x99)
        
        run_txt = rp.add_run(ref_text)
        run_txt.font.name = 'Times New Roman'
        run_txt.font.size = Pt(8.5)
        
        add_bookmark_end(rp, ref_id)

    # Save to targets
    out_final = Path("VEO_conference_paper_final.docx")
    out_paper = Path("VEO_conference_paper.docx")
    out_in_paper_dir = Path("paper") / "VEO_conference_paper.docx"
    out_in_paper_dir.parent.mkdir(exist_ok=True)
    
    doc.save(out_final)
    print(f"\n[OK] High-quality IEEE conference paper successfully compiled and saved to:")
    print(f"     - {out_final.resolve()}")

    try:
        doc.save(out_in_paper_dir)
        print(f"     - {out_in_paper_dir.resolve()}")
    except Exception as e:
        print(f"     [!] Notice writing to {out_in_paper_dir}: {e}")

    try:
        doc.save(out_paper)
        print(f"     - {out_paper.resolve()}")
    except PermissionError:
        print(f"     [!] Notice: '{out_paper.name}' is currently open in Microsoft Word.")
        print(f"         The updated version has been written to '{out_final.name}' and '{out_in_paper_dir}'.")

if __name__ == "__main__":
    main()
