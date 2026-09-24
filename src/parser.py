"""
Парсер HTML файлов из Football Manager
"""
import os
import re
import glob
import math
import pandas as pd
from bs4 import BeautifulSoup
from src import config, models


def get_latest_html(directory: str = None) -> str:
    if directory is None:
        directory = config.DATA_DIR
    list_of_files = glob.glob(os.path.join(directory, '*.html'))
    if not list_of_files:
        raise FileNotFoundError(f"В папке '{directory}' не найдено ни одного HTML файла.")
    return max(list_of_files, key=os.path.getmtime)


def has_position_prefix(positions_str, prefixes: list) -> bool:
    """
    Проверяет, есть ли в строке позиций хотя бы одна позиция,
    начинающаяся с одного из указанных префиксов.
    """
    if not positions_str or str(positions_str).strip() == '':
        return False

    # Заменяем '/' на ',' чтобы корректно парсить позиции вида "П/АП (ПЦ)"
    normalized_str = str(positions_str).replace('/', ',')
    elements = (item.strip() for item in normalized_str.split(','))

    return any(
        any(pos.startswith(prefix) for prefix in prefixes)
        for pos in elements if pos
    )


def parse_single_money(value_str: str) -> float:
    if not value_str:
        return None

    # Убираем "в год" и символы валюты
    value_str = value_str.split('в')[0].strip() if 'в' in value_str else value_str
    value_str = value_str.replace('€', '').replace(' ', '').strip()

    # Проверяем суффиксы млн/тыс ДО удаления запятых
    multiplier = 1
    if 'млн' in value_str.lower():
        multiplier = 1_000_000
        value_str = value_str.lower().replace('млн', '')
    elif 'тыс' in value_str.lower():
        multiplier = 1_000
        value_str = value_str.lower().replace('тыс', '')

    # Убираем лишние точки в конце (например, "9.2млн." -> "9.2")
    value_str = value_str.strip('.')

    # сначала удаляем все запятые (разделители тысяч)
    value_str = value_str.replace(',', '')

    # Теперь извлекаем число
    match = re.search(r'[\d]+\.?[\d]*', value_str)
    if match:
        try:
            return float(match.group(0)) * multiplier
        except ValueError:
            return None
    return None


def parse_money_value(value_str: str) -> float:
    if not value_str or value_str.strip() == '-' or 'Не продаётся' in value_str or 'Не продается' in value_str:
        return None
    if ' - ' in value_str:
        parts = value_str.split(' - ')
        if len(parts) == 2:
            val1 = parse_single_money(parts[0].strip())
            val2 = parse_single_money(parts[1].strip())
            if val1 is not None and val2 is not None:
                return (val1 + val2) / 2
        return None
    return parse_single_money(value_str.strip())


def calculate_age_coefficient(age: int) -> float:
    if age <= 23:
        base = 0.7 + (age - 14) * (0.3 / 9)
    elif age <= 27:
        base = 1.0
    else:
        base = math.exp(-(age - 27) / 10)
    if age > 28:
        base = base * math.exp(-(age - 28) / 2)
    return round(base, 4)


def calculate_price_quality(ovr: float, transfer_value: float, salary: float, age: int) -> float:
    if transfer_value is None or (isinstance(transfer_value, float) and math.isnan(transfer_value)):
        return float('nan')
    if salary is None:
        salary = 0.0
    total_cost = transfer_value + (salary * 2)
    if total_cost <= 0:
        return round(ovr * calculate_age_coefficient(age), 2)

    base_score = ovr * calculate_age_coefficient(age)
    cost_factor = 1 + math.log10(max(1, total_cost / 1_000_000))
    final_score = min(100.0, max(0.0, base_score / cost_factor))
    return round(final_score, 2)


def calculate_technical(positions: str, cols: list, col_indices: dict) -> float:
    is_goalkeeper = 'В' in str(positions)
    attrs = models.GK_TECHNICAL_ATTRS if is_goalkeeper else models.OUTFIELD_TECHNICAL_ATTRS
    values = [int(cols[col_indices[attr]].get_text(strip=True)) for attr in attrs if attr in col_indices and cols[col_indices[attr]].get_text(strip=True).isdigit()]
    return round((sum(values) / len(values)) * 5, 2) if values else 0.0


def calculate_mental(cols: list, col_indices: dict) -> float:
    total_score = 0.0
    for group_data in models.MENTAL_GROUPS.values():
        values = [int(cols[col_indices[attr]].get_text(strip=True)) for attr in group_data['attrs'] if attr in col_indices and cols[col_indices[attr]].get_text(strip=True).isdigit()]
        if values:
            total_score += group_data['weight'] * (sum(values) / len(values))
    return round(total_score * 5, 2)


def calculate_physical(cols: list, col_indices: dict) -> float:
    total_score = 0.0
    for group_data in models.PHYSICAL_GROUPS.values():
        values = [int(cols[col_indices[attr]].get_text(strip=True)) for attr in group_data['attrs'] if attr in col_indices and cols[col_indices[attr]].get_text(strip=True).isdigit()]
        if values:
            total_score += group_data['weight'] * (sum(values) / len(values))
    return round(total_score * 5, 2)


def calculate_ovr(physical: float, mental: float, technical: float) -> float:
    return round(0.45 * physical + 0.25 * mental + 0.30 * technical, 2)


def parse_squad(html_path: str) -> pd.DataFrame:
    print(f"📖 Чтение файла: {html_path}")
    print(f"📦 Размер файла: {os.path.getsize(html_path) / 1024:.2f} КБ")

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, config.HTML_PARSER)

    table = soup.find('table')
    if not table:
        raise ValueError("В HTML файле не найдена таблица <table>.")

    rows = table.find_all('tr')
    headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]

    col_indices = {}
    for col in models.BASE_COLUMNS + models.GK_TECHNICAL_ATTRS + models.OUTFIELD_TECHNICAL_ATTRS + models.ALL_MENTAL_ATTRS + models.ALL_PHYSICAL_ATTRS:
        for i, h in enumerate(headers):
            if h == col or col.lower() in h.lower():
                col_indices[col] = i
                break

    data = []
    for idx, row in enumerate(rows[1:], 1):
        cols = row.find_all(['td', 'th'])
        if len(cols) <= max(col_indices.values(), default=-1):
            continue

        row_data = {}
        for col_name in models.BASE_COLUMNS:
            val = cols[col_indices[col_name]].get_text(strip=True) if col_name in col_indices else ''
            if col_name == 'Возраст':
                try:
                    val = int(val)
                except ValueError:
                    val = 0
            row_data[col_name] = val

        # Сохраняем все атрибуты для расчёта ролей
        for attr in models.GK_TECHNICAL_ATTRS + models.OUTFIELD_TECHNICAL_ATTRS + models.ALL_MENTAL_ATTRS + models.ALL_PHYSICAL_ATTRS:
            val_str = cols[col_indices[attr]].get_text(strip=True) if attr in col_indices else '0'
            row_data[attr] = int(val_str) if val_str.isdigit() else 0

        positions_val = row_data.get('Позиции', '')
        row_data['Технические'] = calculate_technical(positions_val, cols, col_indices)
        row_data['Психологические'] = calculate_mental(cols, col_indices)
        row_data['Физические'] = calculate_physical(cols, col_indices)
        row_data['ОВР'] = calculate_ovr(row_data['Физические'], row_data['Психологические'], row_data['Технические'])

        # Парсинг денег и возраста
        salary_value = parse_money_value(row_data.get('Зарплата', '')) or 0.0
        row_data['Зарплата (€)'] = salary_value

        transfer_value = parse_money_value(row_data.get('Сумма транфера', ''))
        if transfer_value is None:
            row_data['Сумма трансфера (€)'] = float('nan')
            row_data['Продаётся'] = False
        else:
            row_data['Сумма трансфера (€)'] = transfer_value
            row_data['Продаётся'] = True

        age = row_data.get('Возраст', 20)
        if not isinstance(age, int):
            try:
                age = int(age)
            except (ValueError, TypeError):
                age = 20

        row_data['Цена / Качество'] = calculate_price_quality(row_data['ОВР'], transfer_value, salary_value, age)

        # Роли вратарей
        if 'В' in str(positions_val):
            from src.roles import Goalkeeper
            row_data['Вратарь (Зщ)'] = Goalkeeper.defender(row_data)
            row_data['Вратарь-чистильщик (Зщ)'] = Goalkeeper.sweeper_keeper_defend(row_data)
            row_data['Вратарь-чистильщик (По)'] = Goalkeeper.sweeper_keeper_support(row_data)
            row_data['Вратарь-чистильщик (Ат)'] = Goalkeeper.sweeper_keeper_attack(row_data)
            row_data['Универсальность'] = round((row_data['Вратарь (Зщ)'] + row_data['Вратарь-чистильщик (Зщ)'] + row_data['Вратарь-чистильщик (По)'] + row_data['Вратарь-чистильщик (Ат)']) / 4, 2)
        else:
            for col in ['Универсальность', 'Вратарь (Зщ)', 'Вратарь-чистильщик (Зщ)', 'Вратарь-чистильщик (По)', 'Вратарь-чистильщик (Ат)']:
                row_data[col] = 0.0

        # Роли центральных защитников
        cb_prefixes = ["З", "КЗ", "ОП"]
        is_center_back = has_position_prefix(positions_val, cb_prefixes)
        if is_center_back:
            from src.roles import CenterBack
            row_data['Универсальность'] = CenterBack.overall(row_data)
            row_data['Созидательный защитник'] = CenterBack.ball_playing_overall(row_data)
            row_data['Либеро'] = CenterBack.libero_overall(row_data)
            row_data['Крайний центральный защитник'] = CenterBack.wide_center_back_overall(row_data)
            row_data['Центральный защитник'] = CenterBack.central_defender_overall(row_data)
            row_data['Чистый центральный защитник'] = CenterBack.no_nonsense_overall(row_data)
        else:
            for col in ['Универсальность', 'Созидательный защитник', 'Либеро', 'Крайний центральный защитник', 'Центральный защитник', 'Чистый центральный защитник']:
                row_data[col] = 0.0

        # Роли крайнего защитника
        fb_prefixes = ["З", "КЗ", "ОП", "П"]
        is_fullback = has_position_prefix(positions_val, fb_prefixes)
        from src.roles import FullBack
        if is_fullback:
            row_data['Универсальность'] = FullBack.overall(row_data)
            row_data['Фланговый защитник'] = FullBack.wing_back_overall(row_data)
            row_data['Крайний защитник'] = FullBack.full_back_overall(row_data)
            row_data['Атакующий крайний защитник'] = FullBack.attacking_wing_back_overall(row_data)
            row_data['Полуфланговый крайний защитник'] = FullBack.half_wing_back_overall(row_data)
            row_data['Чистый крайний защитник'] = FullBack.no_nonsense_full_back_overall(row_data)

        # Роли опорного полузащитника
        dm_prefixes = ["З", "КЗ", "ОП", "П"]
        is_defensive_midfielder = has_position_prefix(positions_val, dm_prefixes)
        from src.roles import DefensiveMidfielder

        if is_defensive_midfielder:
            row_data['Универсальность'] = DefensiveMidfielder.overall(row_data)
            row_data['Опорный полузащитник'] = DefensiveMidfielder.defensive_midfielder_overall(row_data)
            row_data['Оттянутый плеймейкер'] = DefensiveMidfielder.deep_lying_playmaker_overall(row_data)
            row_data['Полузащитник-разрушитель'] = DefensiveMidfielder.ball_winning_midfielder_overall(row_data)
            row_data['Чистый опорный полузащитник'] = DefensiveMidfielder.anchor_man_overall(row_data)
            row_data['Хавбек'] = DefensiveMidfielder.half_back_overall(row_data)
            row_data['Реджиста'] = DefensiveMidfielder.regista_overall(row_data)
            row_data['Блуждающий плеймейкер'] = DefensiveMidfielder.roamer_overall(row_data)
            row_data['Сегундо-воланте'] = DefensiveMidfielder.segundo_volante_overall(row_data)

        # Роли центрального полузащитника
        cm_prefixes = ["КЗ", "ОП", "П", "АП"]
        is_center_midfielder = has_position_prefix(positions_val, cm_prefixes)
        from src.roles import CentralMidfielder

        if is_center_midfielder:
            row_data['Универсальность'] = CentralMidfielder.overall(row_data)
            row_data['Центральный полузащитник'] = CentralMidfielder.central_midfielder_overall(row_data)
            row_data['Оттянутый плеймейкер'] = CentralMidfielder.deep_lying_playmaker_overall(row_data)
            row_data['Полузащитник бокс-ту-бокс'] = CentralMidfielder.box_to_box_midfielder_overall(row_data)
            row_data['Выдвинутый плеймейкер'] = CentralMidfielder.advanced_playmaker_overall(row_data)
            row_data['Полузащитник-разрушитель'] = CentralMidfielder.ball_winning_midfielder_overall(row_data)
            row_data['Блуждающий плеймейкер'] = CentralMidfielder.roamer_overall(row_data)
            row_data['Меццала'] = CentralMidfielder.mezzala_overall(row_data)
            row_data['Каррилеро'] = CentralMidfielder.carrilero_overall(row_data)

        # Роли крайнего полузащитника
        wm_prefixes = ["КЗ", "ОП", "П", "АП"]
        is_wide_midfielder = has_position_prefix(positions_val, wm_prefixes)
        from src.roles import WideMidfielder

        if is_wide_midfielder:
            row_data['Универсальность'] = WideMidfielder.overall(row_data)
            row_data['Фланговый полузащитник'] = WideMidfielder.winger_overall(row_data)
            row_data['Крайний полузащитник'] = WideMidfielder.wide_midfielder_overall(row_data)
            row_data['Крайний полузащитник оборон. плана'] = WideMidfielder.defensive_winger_overall(row_data)
            row_data['Фланговый плеймейкер'] = WideMidfielder.wide_playmaker_overall(row_data)
            row_data['Полуфланговый крайний полузащитник'] = WideMidfielder.inverted_winger_overall(row_data)

        # Роли атакующего полузащитника
        am_prefixes = ["П", "АП", "НП"]
        is_attacking_midfielder = has_position_prefix(positions_val, am_prefixes)
        from src.roles import AttackingMidfielder

        if is_attacking_midfielder:
            row_data['Универсальность'] = AttackingMidfielder.overall(row_data)
            row_data['Атакующий полузащитник'] = AttackingMidfielder.attacking_midfielder_overall(row_data)
            row_data['Выдвинутый плеймейкер'] = AttackingMidfielder.advanced_playmaker_overall(row_data)
            row_data['Треквартиста'] = AttackingMidfielder.trequartista_overall(row_data)
            row_data['Энганче'] = AttackingMidfielder.enganche_overall(row_data)
            row_data['Теневой нападающий'] = AttackingMidfielder.shadow_striker_overall(row_data)

        # Роли атакующего крайнего полузащитника
        awm_prefixes = ["П", "АП", "НП"]
        is_attacking_wide_midfielder = has_position_prefix(positions_val, awm_prefixes)
        from src.roles import AttackingWideMidfielder

        if is_attacking_wide_midfielder:
            row_data['Универсальность'] = AttackingWideMidfielder.overall(row_data)
            row_data['Крайний полузащитник'] = AttackingWideMidfielder.wide_midfielder_overall(row_data)
            row_data['Выдвинутый плеймейкер'] = AttackingWideMidfielder.advanced_playmaker_overall(row_data)
            row_data['Инсайд'] = AttackingWideMidfielder.inside_forward_overall(row_data)
            row_data['Треквартиста'] = AttackingWideMidfielder.trequartista_overall(row_data)
            row_data['Фланговый таргетмен'] = AttackingWideMidfielder.target_man_winger_overall(row_data)
            row_data['Раумдойтер'] = AttackingWideMidfielder.raumdeuter_overall(row_data)
            row_data['Полуфланговый крайний полузащитник'] = AttackingWideMidfielder.inverted_winger_overall(row_data)

        # Роли нападающего
        st_prefixes = ["П", "АП", "НП"]
        is_striker = has_position_prefix(positions_val, st_prefixes)
        from src.roles import Striker

        if is_striker:
            row_data['Универсальность'] = Striker.overall(row_data)
            row_data['Оттянутый форвард'] = Striker.deep_lying_forward_overall(row_data)
            row_data['Выдвинутый форвард'] = Striker.advanced_forward_overall(row_data)
            row_data['Таргетмен'] = Striker.target_man_overall(row_data)
            row_data['Чистый форвард'] = Striker.poacher_overall(row_data)
            row_data['Универсальный форвард'] = Striker.complete_forward_overall(row_data)
            row_data['Прессингующий форвард'] = Striker.pressing_forward_overall(row_data)
            row_data['Треквартиста'] = Striker.trequartista_overall(row_data)
            row_data['Ложная девятка'] = Striker.false_nine_overall(row_data)

        # ==========================================
        # РАСЧЕТ ПС и ЦЕНЫ / КАЧЕСТВА
        # ==========================================
        import math
        from src.models import get_har_coefficient

        age = row_data.get('Возраст', 20)
        ovr = row_data['ОВР']
        transfer_value = row_data.get('Сумма трансфера (€)', 0)

        # Проверяем, продается ли игрок и есть ли цена
        is_for_sale = (
                transfer_value is not None and
                not (isinstance(transfer_value, float) and math.isnan(transfer_value)) and
                isinstance(transfer_value, (int, float)) and
                transfer_value > 0
        )

        if not is_for_sale:
            # Игрок не продается или цена неизвестна — пропускаем расчет
            row_data['Цена / Качество'] = float('nan')
        else:
            # 1. ВЗР (Возраст)
            if age <= 16:
                vzr = 1.45
            elif age <= 18:
                vzr = 1.35
            elif age <= 21:
                vzr = 1.25
            elif age <= 23:
                vzr = 1.15
            elif age <= 26:
                vzr = 1.10
            else:
                vzr = max(0.3, 1.0 - (age - 27) * 0.1)

            # 2. СТРМЛ (Природные данные + Работоспособность)
            nat_fit = row_data.get('Природные данные', 10)
            work_rate = row_data.get('Работоспособность', 10)
            strml_avg = (nat_fit + work_rate) / 2
            if strml_avg <= 7:
                strml = 0.7
            elif strml_avg <= 12:
                strml = 0.9
            elif strml_avg <= 16:
                strml = 1.1
            else:
                strml = 1.3

            # 3. ХАР (Характер + Пресса из словаря)
            character = row_data.get('Характер', '')
            press = row_data.get('Общение с прессой', '')
            har = get_har_coefficient(character, press)

            # 4. СБР (Сборная)
            team = str(row_data.get('Команда', '')).strip()
            games = row_data.get('Игр', 0)
            youth_games = row_data.get('Млд Игр', 0)

            sbr = 1.0
            if team == 'Главная':
                sbr = 1.3
            elif team and team != 'Главная':
                sbr = 1.15  # U21, U23 и т.д.

            if isinstance(games, (int, float)) and games > 0:
                sbr += min(0.3, math.log10(games + 1) * 0.1)
            if isinstance(youth_games, (int, float)) and youth_games > 0:
                sbr += min(0.15, math.log10(youth_games + 1) * 0.05)
            sbr = min(2.0, sbr)

            # 5. СУМТР (Логарифмический коэффициент цены)
            log_sumtr = 1.0 + math.log10(max(1, transfer_value / 100_000)) * 0.1
            sumtr_coeff = min(2.0, log_sumtr * 1.3) if age <= 21 else min(1.5, log_sumtr)

            # 6. Итоговый расчет ПС
            normalizer = 1.5
            ps = (ovr * vzr * strml * har * sbr * sumtr_coeff) / normalizer

            # 7. Цена / Качество
            price_in_millions = transfer_value / 1_000_000
            price_quality = (ps * 0.7 + ovr * 0.3) / price_in_millions
            row_data['Цена / Качество'] = round(price_quality, 6)
        # ==========================================

        data.append(row_data)
        if idx % 1000 == 0:
            print(f"   ⏳ Обработано: {idx} строк")

    print(f"✅ Парсинг завершен. Обработано строк: {len(data)}")
    return pd.DataFrame(data, columns=models.ALL_COLUMNS)
