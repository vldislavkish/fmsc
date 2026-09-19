# test_attrs.py — запусти один раз
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).parent.parent
df = pd.read_excel(base_dir / 'resources' / 'attrexc.xlsx')

# Колонки AJ-AQ (индексы 35-42, т.к. A=0, B=1, ..., AJ=35)
print("Физические атрибуты (колонки AJ-AQ):")
for i in range(35, 43):
    col_letter = chr(65 + (i // 26)) + chr(65 + (i % 26)) if i >= 26 else chr(65 + i)
    print(f"  {col_letter} (индекс {i}) → {df.columns[i]} = {df.iloc[0, i]}")
