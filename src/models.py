"""
Модели данных проекта FMSC
"""

# Базовые колонки из HTML
BASE_COLUMNS = [
    'Позиции',
    'Возраст',
    'Имя',
    'Зарплата',
    'Сумма транфера',
    'Характер'
]

# Дополнительные колонки
EXTRA_COLUMNS = [
    'Ликвидность',
    'Технические',
    'Психологические',
    'Физические'
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

# Группы атрибутов и их веса
MENTAL_GROUPS = {
    'group_1': {
        'weight': 0.25,
        'attrs': ['Инт', 'Кнц', 'Вид']  # AA, AC, W
    },
    'group_2': {
        'weight': 0.25,
        'attrs': ['Раб', 'Реш', 'Ком', 'Лид']  # AF, AG, AB, AD
    },
    'group_3': {
        'weight': 0.20,
        'attrs': ['ПРш', 'Смб', 'Имп']  # AE, AH, Z
    },
    'group_4': {
        'weight': 0.15,
        'attrs': ['Хрб', 'Агр']  # AI, V
    },
    'group_5': {
        'weight': 0.15,
        'attrs': ['Ибм', 'Поз']  # Y, X
    }
}

# Все психологические атрибуты (для поиска индексов)
ALL_MENTAL_ATTRS = []
for group in MENTAL_GROUPS.values():
    ALL_MENTAL_ATTRS.extend(group['attrs'])
