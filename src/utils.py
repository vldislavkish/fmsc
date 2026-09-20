"""
Вспомогательные утилиты проекта FMSC
"""
import os
import math
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from src import config, models


def ensure_directory(directory: str) -> None:
    """Создает директорию, если она не существует."""
    os.makedirs(directory, exist_ok=True)


def format_sheet(ws, columns: list) -> None:
    """
    Форматирует лист Excel:
    - Закрепление столбцов A-K
    - Автофильтр
    - Стилизация заголовков
    - Фиксированная ширина столбцов
    """
    # Закрепление столбцов A-K включительно
    ws.freeze_panes = 'L2'

    # Автофильтр
    ws.auto_filter.ref = ws.dimensions

    # Стилизация заголовков
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment

    ws.row_dimensions[1].height = 30

    # Ширина столбцов
    column_widths = {
        'A': 12,  # Позиции
        'B': 8,   # Возраст
        'C': 25,  # Имя
        'D': 18,  # Зарплата (€)
        'E': 20,  # Сумма трансфера (€)
        'F': 20,  # Характер
        'G': 12,  # Цена / Качество
        'H': 12,  # Технические
    }

    # Списки колонок для форматирования
    money_cols = ['Зарплата (€)', 'Сумма трансфера (€)']
    rating_cols = [
        'Цена / Качество', 'Технические', 'Психологические', 'Физические', 'ОВР',
        'Вратарь', 'Вратарь (Зщ)', 'Вратарь-чистильщик (Зщ)',
        'Вратарь-чистильщик (По)', 'Вратарь-чистильщик (Ат)'
    ]

    center_alignment = Alignment(horizontal='center', vertical='center')

    for col_idx in range(1, len(columns) + 1):
        col_letter = get_column_letter(col_idx)
        col_name = columns[col_idx - 1]

        # Устанавливаем ширину
        if col_letter in column_widths:
            ws.column_dimensions[col_letter].width = column_widths[col_letter]
        else:
            ws.column_dimensions[col_letter].width = 8

        # Центрирование столбца B (Возраст)
        if col_letter == 'B':
            for row in range(2, ws.max_row + 1):
                ws[f'{col_letter}{row}'].alignment = center_alignment

        # Форматирование числовых столбцов
        if col_name in money_cols:
            for row in range(2, ws.max_row + 1):
                cell = ws[f'{col_letter}{row}']
                cell.number_format = '€#,##0'
                cell.alignment = Alignment(horizontal='right', vertical='center')
        elif col_name in rating_cols:
            for row in range(2, ws.max_row + 1):
                cell = ws[f'{col_letter}{row}']
                if cell.value is not None and not (isinstance(cell.value, float) and math.isnan(cell.value)):
                    cell.number_format = '0.00'
                cell.alignment = Alignment(horizontal='center', vertical='center')


def save_to_excel_formatted(df: pd.DataFrame, output_path: str) -> None:
    """
    Сохраняет DataFrame в Excel файл с несколькими листами:
    - Основное (все игроки)
    - Вратарь (только вратари)
    - Центральный защитник (только центральные защитники)
    """
    print(f"🎨 Применяется форматирование Excel...")

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Лист "Основное" - все игроки
        df_main = df[models.MAIN_COLUMNS].copy()
        df_main.to_excel(writer, sheet_name='Основное', index=False)
        format_sheet(writer.sheets['Основное'], models.MAIN_COLUMNS)

        # Лист "Вратарь" - только вратари
        df_gk = df[df['Позиции'].str.contains('В', na=False)][models.GOALKEEPER_COLUMNS].copy()
        df_gk.to_excel(writer, sheet_name='Вратарь', index=False)
        format_sheet(writer.sheets['Вратарь'], models.GOALKEEPER_COLUMNS)

        # Лист "Центральный защитник" - только центральные защитники
        df_cb = df[df['Позиции'].str.contains('ЦЗ|Ц', na=False)][models.CENTER_BACK_COLUMNS].copy()
        df_cb.to_excel(writer, sheet_name='Центральный защитник', index=False)
        format_sheet(writer.sheets['Центральный защитник'], models.CENTER_BACK_COLUMNS)

    print(f"💾 Excel с форматированием сохранен: {output_path}")


def save_results(df: pd.DataFrame, base_name: str = None) -> None:
    """Сохраняет результаты только в Excel формате."""
    if base_name is None:
        base_name = config.DEFAULT_OUTPUT_NAME

    ensure_directory(config.OUTPUT_DIR)

    xlsx_path = os.path.join(config.OUTPUT_DIR, f'{base_name}.xlsx')
    save_to_excel_formatted(df, xlsx_path)

    print(f"\n📊 Итого строк: {len(df)}")
    print(f"📊 Итого столбцов: {len(df.columns)}")
    print(f"📋 Колонки: {list(df.columns)}")
