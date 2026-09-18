"""
Конфигурация проекта FMSC
"""
import os

# Пути к директориям
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')

# Имена файлов
DEFAULT_OUTPUT_NAME = 'parsed_squad'

# Форматы вывода
OUTPUT_FORMATS = ['csv', 'xlsx']

# Настройки CSV
CSV_ENCODING = 'utf-8-sig'
CSV_SEPARATOR = ';'

# Настройки Excel
EXCEL_ENGINE = 'openpyxl'

# Настройки парсинга
HTML_PARSER = 'lxml'
