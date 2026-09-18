"""
Вспомогательные утилиты проекта FMSC
"""
import os
import pandas as pd
from src import config


def ensure_directory(directory: str) -> None:
    """
    Создает директорию, если она не существует.

    Args:
        directory: Путь к директории
    """
    os.makedirs(directory, exist_ok=True)


def save_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    Сохраняет DataFrame в CSV файл.

    Args:
        df: DataFrame для сохранения
        output_path: Путь к выходному файлу
    """
    df.to_csv(
        output_path,
        index=False,
        encoding=config.CSV_ENCODING,
        sep=config.CSV_SEPARATOR
    )
    print(f"💾 CSV сохранен: {output_path}")


def save_to_excel(df: pd.DataFrame, output_path: str) -> None:
    """
    Сохраняет DataFrame в Excel файл.

    Args:
        df: DataFrame для сохранения
        output_path: Путь к выходному файлу
    """
    df.to_excel(
        output_path,
        index=False,
        engine=config.EXCEL_ENGINE
    )
    print(f"💾 Excel сохранен: {output_path}")


def save_results(df: pd.DataFrame, base_name: str = None) -> None:
    """
    Сохраняет результаты во всех форматах.

    Args:
        df: DataFrame для сохранения
        base_name: Базовое имя файла (без расширения)
    """
    if base_name is None:
        base_name = config.DEFAULT_OUTPUT_NAME

    ensure_directory(config.OUTPUT_DIR)

    # Сохраняем в CSV
    csv_path = os.path.join(config.OUTPUT_DIR, f'{base_name}.csv')
    save_to_csv(df, csv_path)

    # Сохраняем в Excel
    xlsx_path = os.path.join(config.OUTPUT_DIR, f'{base_name}.xlsx')
    save_to_excel(df, xlsx_path)

    print(f"\n📊 Итого строк: {len(df)}")
    print(f"📊 Итого столбцов: {len(df.columns)}")
    print(f"📋 Колонки: {list(df.columns)}")
