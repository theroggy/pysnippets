import json
import os
from pathlib import Path

import pandas as pd
import pdfplumber
import pdfplumber.cli

script_dir = Path(__file__).parent

pdf_path = script_dir / "background-checks.pdf"
with pdfplumber.open(pdf_path) as pdf:
    data = pd.DataFrame(pdf.pages[0].extract_words())
    data.to_csv(script_dir / "background-checks.csv", index=False)
