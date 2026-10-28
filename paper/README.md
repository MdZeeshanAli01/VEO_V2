> **Errata (phase 0 revision):** some claims in this v1 document are overstated or incorrect, including the headline human-agreement figure and Figure 2(a). See [ERRATA_V1.md](../docs/ERRATA_V1.md) for the corrections.

# VEO Conference Manuscript Package

This directory contains the finalized, publication-ready research paper for the Vision Error Observatory (VEO) framework, formatted according to IEEE Computer Society conference specifications.

---

## Document Artifacts

| Document | Format | Description | Status |
| :--- | :---: | :--- | :---: |
| **`VEO_conference_paper.docx`** | Microsoft Word (`.docx`) | Primary submission manuscript. Formatted in IEEE double-column/standard conference style (Times New Roman, 0.75-inch margins, Roman-numeral headings, 9 styled booktabs tables, 3 embedded 300-DPI technical figures, and 51 interactive OpenXML bookmark-linked citations). | **Final / Publication-Ready** |
| **`VEO_conference_paper.pdf`** | Adobe PDF (`.pdf`) | Compiled PDF version of the complete manuscript for rapid viewing, distribution, and submission portals. | **Final / Publication-Ready** |
| **`archive/VEO_conference_paper_original_backup.docx`** | Microsoft Word (`.docx`) | Preserved historical preliminary draft for audit trail and version provenance. | **Archived** |

---

## Paper Specifications

- **Title:** Vision Error Observatory (VEO): A Model-Agnostic Diagnostic and Observability Framework for Failure Analysis in Monocular Depth Estimation
- **Authors:** Anshuman Chakravorty, Zeeshan Ali, Omer Faraz
- **Faculty Mentors:** Prof. Anshi Bajaj, Dr. Amit Saini
- **Affiliation:** School of Technology Management and Engineering (STME), SVKM’s NMIMS University, Hyderabad, India
- **Corresponding Email:** anshumanchakravorty10@gmail.com
- **Word Count:** 5,020 words
- **Tables:** 9 formal academic tables (Tables I–IX)
- **Figures:** 3 high-resolution technical diagrams (Figs 1–3)
- **References:** 51 peer-reviewed citations in standard IEEE citation format

---

## Compilation

The Word manuscript is generated programmatically from verified project artifacts using:
```bash
uv run python scripts/build_final_word_paper.py
```

