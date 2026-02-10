import pandas as pd
import json
from django.core.files.base import ContentFile
from pathlib import Path

def process_file(dataset):
    file_path = dataset.raw_file.path
    ext = Path(file_path).suffix.lower()

    # -------- LOAD FILE --------
    if ext == '.csv':
        df = pd.read_csv(file_path)

    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)

    elif ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.json_normalize(data)

    elif ext == '.tsv':
        df = pd.read_csv(file_path, sep='\t')

    elif ext == '.txt':
        df = pd.read_csv(file_path, delimiter=None, engine='python')

    else:
        dataset.ai_summary = f"Unsupported file type: {ext}"
        dataset.save()
        return

    # -------- BEFORE STATS --------
    dataset.rows_before = len(df)

    # -------- CLEANING --------
    df.columns = df.columns.str.strip().str.lower()
    df = df.drop_duplicates()
    df = df.dropna(how='all')

    # Convert datatypes
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    dataset.rows_after = len(df)
    dataset.cleaned_rows = dataset.rows_before - dataset.rows_after

    # -------- SAVE OUTPUT --------
    csv_data = df.to_csv(index=False)
    output_name = Path(dataset.name).stem + "_processed.csv"

    dataset.processed_file.save(
        output_name,
        ContentFile(csv_data)
    )

    dataset.processed = True
    dataset.ai_summary = (
        f"File type: {ext}\n"
        f"Rows before: {dataset.rows_before}\n"
        f"Rows after: {dataset.rows_after}\n"
        f"Duplicates removed: {dataset.cleaned_rows}"
    )

    dataset.save()
