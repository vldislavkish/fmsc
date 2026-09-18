"""
Парсер HTML файлов из Football Manager
"""
import os
import glob
import pandas as pd
from bs4 import BeautifulSoup
from src import config, models


def get_latest_html(directory: str = None) -> str:
    """Находит самый новый HTML файл в указанной папке по дате модификации."""
    if directory is None:
        directory = config.DATA_DIR

    list_of_files = glob.glob(os.path.join(directory, '*.html'))
    if not list_of_files:
        raise FileNotFoundError(f"В папке '{directory}' не найдено ни одного HTML файла.")

    return max(list_of_files, key=os.path.getmtime)


def calculate_technical(positions: str, cols: list, col_indices: dict) -> float:
    """
    Рассчитывает технические атрибуты (0-100) в зависимости от позиции игрока.
    """
    # Определяем, вратарь ли это (в русском FM вратарь обозначается как "ВР" или "В")
    is_goalkeeper = 'В' in str(positions)

    attrs = models.GK_TECHNICAL_ATTRS if is_goalkeeper else models.OUTFIELD_TECHNICAL_ATTRS

    values = []
    for attr in attrs:
        if attr in col_indices:
            val_str = cols[col_indices[attr]].get_text(strip=True)
            try:
                values.append(int(val_str))
            except ValueError:
                pass  # Пропускаем, если значение не числовое (например, "-")

    if not values:
        return 0.0

    # Среднее арифметическое (диапазон 1-20) переводим в диапазон 0-100
    avg_20 = sum(values) / len(values)
    return round(avg_20 * 5, 2)


def parse_squad(html_path: str) -> pd.DataFrame:
    """Парсит HTML таблицу из Football Manager и извлекает данные игроков."""
    print(f"📖 Чтение файла: {html_path}")
    print(f"📦 Размер файла: {os.path.getsize(html_path) / 1024:.2f} КБ")

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, config.HTML_PARSER)

    table = soup.find('table')
    if not table:
        raise ValueError("В HTML файле не найдена таблица <table>.")

    rows = table.find_all('tr')
    if not rows:
        raise ValueError("В таблице не найдены строки <tr>.")

    print(f"📊 Найдено строк в таблице: {len(rows) - 1}")

    # Получаем заголовки и индексы колонок
    headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]

    # Собираем индексы для базовых колонок и всех атрибутов
    all_needed_attrs = (models.GK_TECHNICAL_ATTRS +
                        models.OUTFIELD_TECHNICAL_ATTRS +
                        models.ALL_MENTAL_ATTRS)
    all_cols_to_find = models.BASE_COLUMNS + all_needed_attrs

    col_indices = {}
    for col in all_cols_to_find:
        for i, h in enumerate(headers):
            if h == col or col.lower() in h.lower():
                col_indices[col] = i
                break

    data = []
    for idx, row in enumerate(rows[1:], 1):
        cols = row.find_all(['td', 'th'])

        if len(cols) > max(col_indices.values(), default=-1):
            row_data = {}

            # 1. Извлекаем базовые данные
            for col_name in models.BASE_COLUMNS:
                if col_name in col_indices:
                    row_data[col_name] = cols[col_indices[col_name]].get_text(strip=True)
                else:
                    row_data[col_name] = ''

            # 2. Рассчитываем "Технические"
            positions_val = row_data.get('Позиции', '')
            row_data['Технические'] = calculate_technical(positions_val, cols, col_indices)

            # 3. Рассчитываем "Психологические"
            row_data['Психологические'] = calculate_mental(cols, col_indices)

            # 4. Заглушка для "Физические"
            row_data['Физические'] = ''

            # 5. Заглушка для "Ликвидность"
            row_data['Ликвидность'] = ''

            data.append(row_data)

            if idx % 1000 == 0:
                print(f"   ⏳ Обработано: {idx} строк")

    print(f"✅ Парсинг завершен. Обработано строк: {len(data)}")

    return pd.DataFrame(data, columns=models.ALL_COLUMNS)

def calculate_mental(cols: list, col_indices: dict) -> float:
    """
    Рассчитывает психологические атрибуты по взвешенной формуле.
    Результат в диапазоне 0-100.
    """
    total_score = 0.0

    for group_name, group_data in models.MENTAL_GROUPS.items():
        weight = group_data['weight']
        attrs = group_data['attrs']

        # Собираем значения атрибутов группы
        values = []
        for attr in attrs:
            if attr in col_indices:
                val_str = cols[col_indices[attr]].get_text(strip=True)
                try:
                    values.append(int(val_str))
                except ValueError:
                    pass  # Пропускаем нечисловые значения

        if values:
            # Среднее по группе (в диапазоне 1-20)
            group_avg = sum(values) / len(values)
            # Умножаем на вес группы
            total_score += weight * group_avg

    # Переводим из диапазона 1-20 в 0-100
    return round(total_score * 5, 2)
