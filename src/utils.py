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
    os.makedirs(directory, exist_ok=True)


def format_sheet(ws, columns: list, freeze_col: str = 'L2') -> None:
    ws.freeze_panes = freeze_col
    ws.auto_filter.ref = ws.dimensions

    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
    ws.row_dimensions[1].height = 30

    column_widths = {'A': 12, 'B': 8, 'C': 25, 'D': 18, 'E': 20, 'F': 20, 'G': 12, 'H': 12}
    money_cols = ['Зарплата (€)', 'Сумма трансфера (€)']
    rating_cols = [
        'Цена / Качество', 'Технические', 'Психологические', 'Физические', 'ОВР',
        'Универсальность',
        'Вратарь (Зщ)', 'Вратарь-чистильщик (Зщ)', 'Вратарь-чистильщик (По)', 'Вратарь-чистильщик (Ат)',
        'Созидательный защитник', 'Либеро', 'Крайний центральный защитник',
        'Центральный защитник', 'Чистый центральный защитник',
        'Фланговый защитник', 'Крайний защитник', 'Атакующий крайний защитник',
        'Полуфланговый крайний защитник', 'Чистый крайний защитник',
        'Опорный полузащитник', 'Оттянутый плеймейкер', 'Полузащитник-разрушитель',
        'Чистый опорный полузащитник', 'Хавбек', 'Реджиста',
        'Блуждающий плеймейкер', 'Сегундо-воланте',
        'Центральный полузащитник', 'Полузащитник бокс-ту-бокс',
        'Выдвинутый плеймейкер', 'Меццала', 'Каррилеро',
        'Фланговый полузащитник', 'Крайний полузащитник',
        'Крайний полузащитник оборон. плана', 'Фланговый плеймейкер',
        'Полуфланговый крайний полузащитник',
        'Атакующий полузащитник', 'Треквартиста', 'Энганче', 'Теневой нападающий',
        'Инсайд', 'Фланговый таргетмен', 'Раумдойтер',
    ]
    for col_idx in range(1, len(columns) + 1):
        col_letter = get_column_letter(col_idx)
        col_name = columns[col_idx - 1]

        ws.column_dimensions[col_letter].width = column_widths.get(col_letter, 8)

        if col_letter == 'B':
            for row in range(2, ws.max_row + 1):
                ws[f'{col_letter}{row}'].alignment = Alignment(horizontal='center', vertical='center')

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
        # === Лист "Основное" ===
        df_main = df[models.MAIN_COLUMNS].copy()
        df_main.to_excel(writer, sheet_name='Основное', index=False)
        format_sheet(writer.sheets['Основное'], models.MAIN_COLUMNS, freeze_col='L2')

        # === Лист "Вратарь" ===
        df_gk = df[df['Позиции'].str.contains('В', na=False)][models.GOALKEEPER_COLUMNS].copy()
        df_gk.to_excel(writer, sheet_name='Вратарь', index=False)
        ws_gk = writer.sheets['Вратарь']
        format_sheet(ws_gk, models.GOALKEEPER_COLUMNS, freeze_col='M2')

        for row in range(2, ws_gk.max_row + 1):
            ws_gk.cell(row=row, column=12).value = f'=AVERAGE(M{row}:P{row})'

        # === Лист "Центральный защитник" ===
        # Позиции: "З", "КЗ", "ОП"
        from src.parser import has_position_prefix
        cb_prefixes = ["З", "КЗ", "ОП"]
        mask_cb = df['Позиции'].apply(lambda x: has_position_prefix(x, cb_prefixes))
        df_cb = df[mask_cb][models.CENTER_BACK_COLUMNS].copy()
        df_cb.to_excel(writer, sheet_name='Центральный защитник', index=False)
        ws_cb = writer.sheets['Центральный защитник']
        format_sheet(ws_cb, models.CENTER_BACK_COLUMNS, freeze_col='M2')

        for row in range(2, ws_cb.max_row + 1):
            ws_cb.cell(row=row, column=12).value = f'=AVERAGE(M{row}:Q{row})'

        # === Лист "Крайний защитник" ===
        # Позиции: "З", "КЗ", "ОП", "П"
        fb_prefixes = ["З", "КЗ", "ОП", "П"]
        mask_fb = df['Позиции'].apply(lambda x: has_position_prefix(x, fb_prefixes))
        df_fb = df[mask_fb][models.FULLBACK_COLUMNS].copy()
        df_fb.to_excel(writer, sheet_name='Крайний защитник', index=False)
        ws_fb = writer.sheets['Крайний защитник']
        format_sheet(ws_fb, models.FULLBACK_COLUMNS, freeze_col='M2')

        for row in range(2, ws_fb.max_row + 1):
            ws_fb.cell(row=row, column=12).value = f'=AVERAGE(M{row}:Q{row})'

        # === Лист "Опорный полузащитник" ===
        # Позиции: "З", "КЗ", "ОП", "П"
        dm_prefixes = ["З", "КЗ", "ОП", "П"]
        mask_dm = df['Позиции'].apply(lambda x: has_position_prefix(x, dm_prefixes))
        df_dm = df[mask_dm][models.DEFENSIVE_MIDFIELDER_COLUMNS].copy()
        df_dm.to_excel(writer, sheet_name='Опорный полузащитник', index=False)
        ws_dm = writer.sheets['Опорный полузащитник']
        format_sheet(ws_dm, models.DEFENSIVE_MIDFIELDER_COLUMNS, freeze_col='M2')

        for row in range(2, ws_dm.max_row + 1):
            ws_dm.cell(row=row, column=12).value = f'=AVERAGE(M{row}:T{row})'

        # === Лист "Центральный полузащитник" ===
        # Позиции: "КЗ", "ОП", "П", "АП"
        cm_prefixes = ["КЗ", "ОП", "П", "АП"]
        mask_cm = df['Позиции'].apply(lambda x: has_position_prefix(x, cm_prefixes))
        df_cm = df[mask_cm][models.CENTER_MIDFIELDER_COLUMNS].copy()
        df_cm.to_excel(writer, sheet_name='Центральный полузащитник', index=False)
        ws_cm = writer.sheets['Центральный полузащитник']
        format_sheet(ws_cm, models.CENTER_MIDFIELDER_COLUMNS, freeze_col='M2')

        for row in range(2, ws_cm.max_row + 1):
            ws_cm.cell(row=row, column=12).value = f'=AVERAGE(M{row}:T{row})'

        # === Лист "Крайний полузащитник" ===
        # Позиции: "КЗ", "ОП", "П", "АП"
        wm_prefixes = ["КЗ", "ОП", "П", "АП"]
        mask_wm = df['Позиции'].apply(lambda x: has_position_prefix(x, wm_prefixes))
        df_wm = df[mask_wm][models.WIDE_MIDFIELDER_COLUMNS].copy()
        df_wm.to_excel(writer, sheet_name='Крайний полузащитник', index=False)
        ws_wm = writer.sheets['Крайний полузащитник']
        format_sheet(ws_wm, models.WIDE_MIDFIELDER_COLUMNS, freeze_col='M2')

        for row in range(2, ws_wm.max_row + 1):
            ws_wm.cell(row=row, column=12).value = f'=AVERAGE(M{row}:Q{row})'

        # === Лист "Атакующий полузащитник" ===
        # Позиции: "П", "АП", "НП"
        am_prefixes = ["П", "АП", "НП"]
        mask_am = df['Позиции'].apply(lambda x: has_position_prefix(x, am_prefixes))
        df_am = df[mask_am][models.ATTACKING_MIDFIELDER_COLUMNS].copy()
        df_am.to_excel(writer, sheet_name='Атакующий полузащитник', index=False)
        ws_am = writer.sheets['Атакующий полузащитник']
        format_sheet(ws_am, models.ATTACKING_MIDFIELDER_COLUMNS, freeze_col='M2')

        for row in range(2, ws_am.max_row + 1):
            ws_am.cell(row=row, column=12).value = f'=AVERAGE(M{row}:Q{row})'

        # === Лист "Атакующий крайний полузащитник" ===
        # Позиции: "П", "АП", "НП"
        awm_prefixes = ["П", "АП", "НП"]
        mask_awm = df['Позиции'].apply(lambda x: has_position_prefix(x, awm_prefixes))
        df_awm = df[mask_awm][models.ATTACKING_WIDE_MIDFIELDER_COLUMNS].copy()
        df_awm.to_excel(writer, sheet_name='Атакующий крайний полузащитник', index=False)
        ws_awm = writer.sheets['Атакующий крайний полузащитник']
        format_sheet(ws_awm, models.ATTACKING_WIDE_MIDFIELDER_COLUMNS, freeze_col='M2')

        for row in range(2, ws_awm.max_row + 1):
            ws_awm.cell(row=row, column=12).value = f'=AVERAGE(M{row}:S{row})'

    print(f"💾 Excel с форматированием сохранен: {output_path}")


def save_results(df: pd.DataFrame, base_name: str = None) -> None:
    if base_name is None:
        base_name = config.DEFAULT_OUTPUT_NAME
    ensure_directory(config.OUTPUT_DIR)

    xlsx_path = os.path.join(config.OUTPUT_DIR, f'{base_name}.xlsx')
    save_to_excel_formatted(df, xlsx_path)

    print(f"\n📊 Итого строк: {len(df)}")
    print(f"📊 Итого столбцов: {len(df.columns)}")
    print(f"📋 Колонки: {list(df.columns)}")
