"""
Парсер HTML файлов из Football Manager
"""
import os
import glob
import math
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


def parse_money_value(value_str: str) -> float:
    """
    Преобразует строку с денежной суммой в числовое значение (в евро).
    Для диапазона берёт медиану (среднее арифметическое двух значений).

    Примеры:
        "€550тыс." → 550000
        "€8млн." → 8000000
        "€100млн. - €128млн." → 114000000
        "Не продаётся" → None
    """
    if not value_str or value_str.strip() == '-' or 'Не продаётся' in value_str:
        return None

    # Если диапазон - берём медиану (среднее двух значений)
    if ' - ' in value_str:
        parts = value_str.split(' - ')
        if len(parts) == 2:
            val1 = parse_single_money(parts[0].strip())
            val2 = parse_single_money(parts[1].strip())
            if val1 is not None and val2 is not None:
                return (val1 + val2) / 2
        return None

    return parse_single_money(value_str.strip())


def parse_single_money(value_str: str) -> float:
    """Парсит одиночное денежное значение."""
    if not value_str:
        return None

    # Убираем текст "в год", "в неделю" и т.д.
    value_str = value_str.split('в')[0].strip() if 'в' in value_str else value_str

    # Убираем символы валюты, пробелы и запятые (разделители тысяч)
    value_str = value_str.replace('€', '').replace(' ', '').replace(',', '').strip()

    # Определяем множитель
    multiplier = 1
    if 'млн' in value_str.lower():
        multiplier = 1_000_000
        value_str = value_str.lower().replace('млн', '').replace('.', '')
    elif 'тыс' in value_str.lower():
        multiplier = 1_000
        value_str = value_str.lower().replace('тыс', '').replace('.', '')

    try:
        return float(value_str) * multiplier
    except ValueError:
        return None


def calculate_age_coefficient(age: int) -> float:
    """
    Рассчитывает коэффициент возраста для формулы Цена/Качество.

    Логика:
    - 14-23 года: быстрый рост (0.7 → 1.0)
    - 23-27 лет: плато (1.0) — пик карьеры
    - После 27: медленное падение
    - После 28: резкий штраф (экспоненциальное падение)

    Примеры:
        14 лет → 0.70
        18 лет → 0.83
        21 год (Беллингем) → 0.93
        25 лет → 1.00 (максимум)
        28 лет → 0.91
        30 лет → 0.27
        33 года → 0.05
    """
    if age <= 23:
        # Быстрый рост от 0.7 (в 14 лет) до 1.0 (в 23 года)
        base = 0.7 + (age - 14) * (0.3 / 9)
    elif age <= 27:
        # Плато — пик карьеры
        base = 1.0
    else:
        # Медленное падение после 27
        base = math.exp(-(age - 27) / 10)

    # Штраф после 28 лет (резкое падение)
    if age > 28:
        penalty = math.exp(-(age - 28) / 2)
        base = base * penalty

    return round(base, 4)


def calculate_price_quality(ovr: float, transfer_value: float,
                            salary: float, age: int) -> float:
    """
    Рассчитывает показатель "Цена / Качество" (0-100).
    Чем ВЫШЕ показатель, тем ЛУЧШЕ трансфер.
    """
    import math

    # Коэффициент возраста
    age_coeff = calculate_age_coefficient(age)

    # Базовый рейтинг (0-100)
    base_score = ovr * age_coeff

    # Если игрок не продаётся
    if transfer_value is None:
        return 0.0

    # Если зарплата не указана - считаем как 0
    if salary is None:
        salary = 0.0

    # Общая стоимость (трансфер + 2 года зарплаты)
    total_cost = transfer_value + (salary * 2)

    # Защита от деления на ноль и слишком маленьких значений
    # Минимальная стоимость для расчёта - €100,000
    MIN_COST = 100_000

    if total_cost < MIN_COST:
        # Если игрок почти бесплатный, используем упрощённую формулу
        # Максимум 80 для бесплатных игроков с высоким ОВР
        free_player_score = base_score * 0.8
        return round(min(80.0, free_player_score), 2)

    # Логарифмическое масштабирование
    cost_in_millions = total_cost / 1_000_000

    # ИСПРАВЛЕНИЕ: используем max(1, cost_in_millions) чтобы log10 никогда не был отрицательным
    cost_factor = 1 + math.log10(max(1, cost_in_millions))

    # Дополнительная защита от деления на ноль
    if cost_factor <= 0:
        cost_factor = 1.0

    # Финальный рейтинг
    final_score = base_score / cost_factor

    # Ограничение 0-100
    final_score = min(100.0, max(0.0, final_score))

    return round(final_score, 2)


def calculate_technical(positions: str, cols: list, col_indices: dict) -> float:
    """Рассчитывает технические атрибуты (0-100) в зависимости от позиции игрока."""
    is_goalkeeper = 'В' in str(positions)

    attrs = models.GK_TECHNICAL_ATTRS if is_goalkeeper else models.OUTFIELD_TECHNICAL_ATTRS

    values = []
    for attr in attrs:
        if attr in col_indices:
            val_str = cols[col_indices[attr]].get_text(strip=True)
            try:
                values.append(int(val_str))
            except ValueError:
                pass

    if not values:
        return 0.0

    avg_20 = sum(values) / len(values)
    return round(avg_20 * 5, 2)


def calculate_mental(cols: list, col_indices: dict) -> float:
    """Рассчитывает психологические атрибуты по взвешенной формуле (0-100)."""
    total_score = 0.0

    for group_name, group_data in models.MENTAL_GROUPS.items():
        weight = group_data['weight']
        attrs = group_data['attrs']

        values = []
        for attr in attrs:
            if attr in col_indices:
                val_str = cols[col_indices[attr]].get_text(strip=True)
                try:
                    values.append(int(val_str))
                except ValueError:
                    pass

        if values:
            group_avg = sum(values) / len(values)
            total_score += weight * group_avg

    return round(total_score * 5, 2)


def calculate_physical(cols: list, col_indices: dict) -> float:
    """Рассчитывает физические атрибуты по взвешенной формуле (0-100)."""
    total_score = 0.0

    for group_name, group_data in models.PHYSICAL_GROUPS.items():
        weight = group_data['weight']
        attrs = group_data['attrs']

        values = []
        for attr in attrs:
            if attr in col_indices:
                val_str = cols[col_indices[attr]].get_text(strip=True)
                try:
                    values.append(int(val_str))
                except ValueError:
                    pass

        if values:
            group_avg = sum(values) / len(values)
            total_score += weight * group_avg

    return round(total_score * 5, 2)


def calculate_ovr(physical: float, mental: float, technical: float) -> float:
    """Рассчитывает Общий Рейтинг Игрока (ОВР). Физ: 45%, Псих: 25%, Тех: 30%."""
    ovr = 0.45 * physical + 0.25 * mental + 0.30 * technical
    return round(ovr, 2)


def parse_squad(html_path: str) -> pd.DataFrame:
    """Парсит HTML таблицу из Football Manager и извлекает данные игроков."""
    print(f"📖 Чтение файла: {html_path}")
    print(f" Размер файла: {os.path.getsize(html_path) / 1024:.2f} КБ")

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

    # Собираем индексы для всех нужных атрибутов
    all_needed_attrs = (models.GK_TECHNICAL_ATTRS +
                        models.OUTFIELD_TECHNICAL_ATTRS +
                        models.ALL_MENTAL_ATTRS +
                        models.ALL_PHYSICAL_ATTRS)
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
                    val = cols[col_indices[col_name]].get_text(strip=True)

                    # Конвертируем возраст в число
                    if col_name == 'Возраст':
                        try:
                            val = int(val)
                        except ValueError:
                            val = 0

                    row_data[col_name] = val
                else:
                    row_data[col_name] = '' if col_name != 'Возраст' else 0

            # 2. Рассчитываем "Технические"
            positions_val = row_data.get('Позиции', '')
            technical = calculate_technical(positions_val, cols, col_indices)
            row_data['Технические'] = technical

            # 3. Рассчитываем "Психологические"
            mental = calculate_mental(cols, col_indices)
            row_data['Психологические'] = mental

            # 4. Рассчитываем "Физические"
            physical = calculate_physical(cols, col_indices)
            row_data['Физические'] = physical

            # 5. Рассчитываем "ОВР"
            ovr = calculate_ovr(physical, mental, technical)
            row_data['ОВР'] = ovr

            # 6. Рассчитываем "Цена / Качество"
            transfer_str = row_data.get('Сумма транфера', '')
            transfer_value = parse_money_value(transfer_str)

            salary_str = row_data.get('Зарплата', '')
            salary_value = parse_money_value(salary_str)

            age_str = row_data.get('Возраст', '0')
            try:
                age = int(age_str)
            except ValueError:
                age = 20

            price_quality = calculate_price_quality(ovr, transfer_value, salary_value, age)
            row_data['Цена / Качество'] = price_quality

            data.append(row_data)

            if idx % 1000 == 0:
                print(f"   ⏳ Обработано: {idx} строк")

    print(f"✅ Парсинг завершен. Обработано строк: {len(data)}")

    return pd.DataFrame(data, columns=models.ALL_COLUMNS)
