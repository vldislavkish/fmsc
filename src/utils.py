"""
Вспомогательные утилиты проекта FMSC
"""
import os
import math
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import Outline
from src import config


def ensure_directory(directory: str) -> None:
    """Создает директорию, если она не существует."""
    os.makedirs(directory, exist_ok=True)


def save_to_excel_formatted(df: pd.DataFrame, output_path: str) -> None:
    """
    Сохраняет DataFrame в Excel файл с автоматическим форматированием:
    - Закрепление столбцов A-K
    - Группировка столбцов M-P (вратарские роли)
    - Автофильтр
    - Стилизация заголовков
    - Фиксированная ширина столбцов
    """
    print(f"🎨 Применяется форматирование Excel...")

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Игроки', index=False)
        ws = writer.sheets['Игроки']

        # 1. Закрепление столбцов A-K включительно
        ws.freeze_panes = 'L2'

        # 2. Группировка столбцов M-P включительно (вратарские роли)
        for col in ['M', 'N', 'O', 'P']:
            ws.column_dimensions[col].outline_level = 1
            ws.column_dimensions[col].hidden = False

        # 3. Включение автофильтра на всю таблицу
        ws.auto_filter.ref = ws.dimensions

        # 4. Стилизация заголовков (первая строка)
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF', size=11)
        header_alignment = Alignment(
            horizontal='center',
            vertical='center',
            wrap_text=True
        )

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment

        # Высота первой строки для корректного отображения переноса
        ws.row_dimensions[1].height = 30

        # 5. Фиксированная ширина столбцов
        column_widths = {
            'A': 12,  # Позиции
            'B': 8,   # Возраст
            'C': 25,  # Имя
            'D': 18,  # Зарплата
            'E': 20,  # Сумма транфера
            'F': 20,  # Характер
        }

        # Списки колонок для форматирования
        money_cols = ['Зарплата (€)', 'Сумма трансфера (€)']
        rating_cols = [
            'Цена / Качество', 'Технические', 'Психологические', 'Физические', 'ОВР',
            'Вратарь', 'Вратарь (Зщ)', 'Вратарь-чистильщик (Зщ)',
            'Вратарь-чистильщик (По)', 'Вратарь-чистильщик (Ат)'
        ]

        # Центрирование для столбца B
        center_alignment = Alignment(horizontal='center', vertical='center')

        for col_idx in range(1, len(df.columns) + 1):
            col_letter = get_column_letter(col_idx)
            col_name = df.columns[col_idx - 1]

            # Устанавливаем ширину
            if col_letter in column_widths:
                ws.column_dimensions[col_letter].width = column_widths[col_letter]
            else:
                # G и далее = 8
                ws.column_dimensions[col_letter].width = 8

            # Центрирование столбца B (Возраст)
            if col_letter == 'B':
                for row in range(2, ws.max_row + 1):
                    ws[f'{col_letter}{row}'].alignment = center_alignment

            # Форматирование числовых столбцов
            if col_name in money_cols:
                # Формат валюты для зарплат и трансферов
                for row in range(2, ws.max_row + 1):
                    cell = ws[f'{col_letter}{row}']
                    cell.number_format = '€#,##0'
                    cell.alignment = Alignment(horizontal='right', vertical='center')

            elif col_name in rating_cols:
                # Формат 0.00 для рейтингов
                for row in range(2, ws.max_row + 1):
                    cell = ws[f'{col_letter}{row}']
                    # NaN оставляем пустыми (не трогаем формат)
                    if cell.value is not None and not (isinstance(cell.value, float) and math.isnan(cell.value)):
                        cell.number_format = '0.00'
                    cell.alignment = Alignment(horizontal='center', vertical='center')

    print(f"💾 Excel с форматированием сохранен: {output_path}")


def save_results(df: pd.DataFrame, base_name: str = None) -> None:
    """Сохраняет результаты только в Excel формате."""
    if base_name is None:
        base_name = config.DEFAULT_OUTPUT_NAME

    ensure_directory(config.OUTPUT_DIR)

    # Сохраняем только в форматированный Excel
    xlsx_path = os.path.join(config.OUTPUT_DIR, f'{base_name}.xlsx')
    save_to_excel_formatted(df, xlsx_path)

    print(f"\n📊 Итого строк: {len(df)}")
    print(f" Итого столбцов: {len(df.columns)}")
    print(f"📋 Колонки: {list(df.columns)}")
