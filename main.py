"""make.fun news-image entry: copies the committed entry.png (drawn by tools/draw.py) to the output folder.

Locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
shutil.copyfile(os.path.join(here, "entry.png"), os.path.join(out_dir, "entry.png"))
