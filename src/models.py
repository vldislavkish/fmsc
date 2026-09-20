"""
Модели данных проекта FMSC
"""

# Базовые колонки из HTML
BASE_COLUMNS = [
    'Позиции',
    'Возраст',  # int
    'Имя',
    'Зарплата',  # float (евро)
    'Сумма транфера',  # float (евро) или None
    'Характер'
]

# Дополнительные колонки
EXTRA_COLUMNS = [
    'Цена / Качество',
    'Технические',
    'Психологические',
    'Физические',
    'ОВР',
    'Вратарь',
    'Вратарь (Зщ)',
    'Вратарь-чистильщик (Зщ)',
    'Вратарь-чистильщик (По)',
    'Вратарь-чистильщик (Ат)',
]

# Все колонки итогового DataFrame
ALL_COLUMNS = BASE_COLUMNS + EXTRA_COLUMNS

# --- АТРИБУТЫ ДЛЯ РАСЧЁТОВ (на основе attrexc.xlsx) ---

# Вратарские технические (K-U, кроме O=СВВ, R=Клк, U=Экц)
GK_TECHNICAL_ATTRS = [
    'Ввод',   # K
    'Вза',    # L
    'Выб',    # M
    'ИШтр',   # N
    'Рук',    # P
    '1на1',   # Q
    'Ркц',    # S
    'Взд'     # T
]

# Технические полевых игроков (AR-BE, кроме AR=Вбр, AW=Штр, BB=Пен, BE=Угл)
OUTFIELD_TECHNICAL_ATTRS = [
    'Длн',    # AS
    'Дрб',    # AT
    'Зав',    # AU
    'Глв',    # AV
    'Нав',    # AX
    'Опк',    # AY
    'Отб',    # AZ
    'Пас',    # BA
    'ПКас',   # BC
    'Тех'     # BD
]

# --- ПСИХОЛОГИЧЕСКИЕ АТРИБУТЫ (с весами) ---
MENTAL_GROUPS = {
    'group_1': {
        'weight': 0.25,
        'attrs': ['Инт', 'Кнц', 'Вид']
    },
    'group_2': {
        'weight': 0.25,
        'attrs': ['Раб', 'Реш', 'Ком', 'Лид']
    },
    'group_3': {
        'weight': 0.20,
        'attrs': ['ПРш', 'Смб', 'Имп']
    },
    'group_4': {
        'weight': 0.15,
        'attrs': ['Хрб', 'Агр']
    },
    'group_5': {
        'weight': 0.15,
        'attrs': ['Ибм', 'Поз']
    }
}

ALL_MENTAL_ATTRS = []
for group in MENTAL_GROUPS.values():
    ALL_MENTAL_ATTRS.extend(group['attrs'])

# --- ФИЗИЧЕСКИЕ АТРИБУТЫ (с весами) ---
PHYSICAL_GROUPS = {
    'group_1': {
        'weight': 0.30,
        'attrs': ['Скр', 'Уск']
    },
    'group_2': {
        'weight': 0.20,
        'attrs': ['Лвк', 'ПРГ']
    },
    'group_3': {
        'weight': 0.15,
        'attrs': ['ВЫН']
    },
    'group_4': {
        'weight': 0.20,
        'attrs': ['СИЛ', 'КРД']
    },
    'group_5': {
        'weight': 0.15,
        'attrs': ['ПРД']
    }
}

ALL_PHYSICAL_ATTRS = []
for group in PHYSICAL_GROUPS.values():
    ALL_PHYSICAL_ATTRS.extend(group['attrs'])
