"""
Парсер HTML файлов из Football Manager
"""
import os
import glob
import pandas as pd
from bs4 import BeautifulSoup
from src import config, models


def get_latest_html(directory: str = None) -> str:
    """
    Находит самый новый HTML файл в указанной папке по дате модификации.

    Args:
        directory: Путь к папке с HTML файлами (по умолчанию DATA_DIR из config)

    Returns:
        Путь к последнему HTML файлу

    Raises:
        FileNotFoundError: Если в папке не найдено ни одного HTML файла
    """
    if directory is None:
        directory = config.DATA_DIR

    list_of_files = glob.glob(os.path.join(directory, '*.html'))

    if not list_of_files:
        raise FileNotFoundError(f"В папке '{directory}' не найдено ни одного HTML файла.")

    latest_file = max(list_of_files, key=os.path.getmtime)
    return latest_file


def parse_squad(html_path: str) -> pd.DataFrame:
    """
    Парсит HTML таблицу из Football Manager и извлекает данные игроков.

    Args:
        html_path: Путь к HTML файлу

    Returns:
        DataFrame с данными игроков

    Raises:
        ValueError: Если в файле не найдена таблица или строки
    """
    print(f" Чтение файла: {html_path}")
    print(f"📦 Размер файла: {os.path.getsize(html_path) / 1024:.2f} КБ")

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, config.HTML_PARSER)

    # Находим первую таблицу в документе
    table = soup.find('table')
    if not table:
        raise ValueError("В HTML файле не найдена таблица <table>.")

    rows = table.find_all('tr')
    if not rows:
        raise ValueError("В таблице не найдены строки <tr>.")

    print(f"📊 Найдено строк в таблице: {len(rows) - 1}")

    # Получаем заголовки из первой строки
    headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]

    # Ищем индексы базовых колонок
    col_indices = {}
    for col in models.BASE_COLUMNS:
        for i, h in enumerate(headers):
            if h == col or col.lower() in h.lower():
                col_indices[col] = i
                break

    # Проверяем, что все базовые колонки найдены
    missing_cols = [col for col in models.BASE_COLUMNS if col not in col_indices]
    if missing_cols:
        print(f"⚠️  Не найдены колонки: {missing_cols}")
        print(f"📋 Доступные заголовки: {headers}")

    # Собираем данные
    data = []
    for idx, row in enumerate(rows[1:], 1):
        cols = row.find_all(['td', 'th'])

        if len(cols) > max(col_indices.values(), default=-1):
            row_data = {}

            # Извлекаем базовые данные
            for col_name in models.BASE_COLUMNS:
                if col_name in col_indices:
                    val = cols[col_indices[col_name]].get_text(strip=True)
                    row_data[col_name] = val
                else:
                    row_data[col_name] = ''

            # Добавляем дополнительные колонки (пока пустые)
            for col_name in models.EXTRA_COLUMNS:
                row_data[col_name] = ''

            data.append(row_data)

            # Прогресс для больших файлов
            if idx % 1000 == 0:
                print(f"   Обработано: {idx} строк")

    print(f"✅ Парсинг завершен. Обработано строк: {len(data)}")

    # Создаем DataFrame с нужным порядком колонок
    df = pd.DataFrame(data, columns=models.ALL_COLUMNS)

    return df
