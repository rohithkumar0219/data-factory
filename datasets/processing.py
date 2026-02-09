import pandas as pd
from django.core.files.base import ContentFile
from .ai_engine import generate_ai_summary

def process_csv(dataset):
    df = pd.read_csv(dataset.raw_file.path)

    dataset.rows_before = len(df)
    dataset.ai_summary = generate_ai_summary(df)

    df = df.dropna().drop_duplicates()
    df.columns = df.columns.str.lower()

    dataset.rows_after = len(df)
    dataset.cleaned_rows = dataset.rows_before - dataset.rows_after

    csv_data = df.to_csv(index=False)
    dataset.processed_file.save(
        dataset.name.replace('.csv', '_clean.csv'),
        ContentFile(csv_data)
    )

    dataset.processed = True
    dataset.save()
