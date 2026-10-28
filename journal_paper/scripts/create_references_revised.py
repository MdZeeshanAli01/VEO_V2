# -*- coding: utf-8 -*-
"""
Creates journal_paper/references_revised.bib with all 59 verified citations.
Fixes Swedish umlaut in Schon and adds 5 previously missing entries.
"""

from pathlib import Path

bib_path = Path("journal_paper/references.bib")
out_path = Path("journal_paper/references_revised.bib")

with open(bib_path, "r", encoding="utf-8") as f:
    bib = f.read()

# Fix Schon
bib_fixed = bib.replace('Sch{"o}n, Thomas B.', r'Sch{\"o}n, Thomas B.')

missing_entries = """
@inproceedings{laina2016deeper,
  author    = {Laina, Iro and Rupprecht, Christian and Belagiannis, Vasileios and Tombari, Federico and Navab, Nassir},
  title     = {Deeper Depth Prediction with Fully Convolutional Residual Networks},
  booktitle = {Proceedings of the International Conference on 3D Vision (3DV)},
  pages     = {239--248},
  year      = {2016}
}

@inproceedings{adebayo2018sanity,
  author    = {Adebayo, Julius and Gilmer, Justin and Muelly, Michael and Goodfellow, Ian and Hardt, Moritz and Kim, Been},
  title     = {Sanity Checks for Saliency Maps},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {31},
  pages     = {9505--9515},
  year      = {2018}
}

@inproceedings{godard2017unsupervised,
  author    = {Godard, Cl{\\'e}ment and Mac Aodha, Oisin and Brostow, Gabriel J.},
  title     = {Unsupervised Monocular Depth Estimation with Left-Right Consistency},
  booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {270--279},
  year      = {2017}
}

@inproceedings{bolya2020tide,
  author    = {Bolya, Daniel and Foley, Sean and Hays, James and Hoffman, Judy},
  title     = {{TIDE}: A General Toolbox for Identifying Object Detection Errors},
  booktitle = {Proceedings of the European Conference on Computer Vision (ECCV)},
  pages     = {558--573},
  year      = {2020}
}

@inproceedings{eyuboglu2022domino,
  author    = {Eyuboglu, Sabri and Varma, Maya and Saab, Khaled and Delbrouck, Jean-Benoit and Lee-Messer, Christopher and R{\\'e}, Christopher},
  title     = {Domino: Discovering Systematic Errors with Cross-Modal Embeddings},
  booktitle = {Proceedings of the International Conference on Machine Learning (ICML)},
  pages     = {5971--5988},
  year      = {2022}
}
"""

revised_bib = bib_fixed.strip() + "\n" + missing_entries.strip() + "\n"

with open(out_path, "w", encoding="utf-8") as f:
    f.write(revised_bib)

print(f"Successfully generated {out_path}")

