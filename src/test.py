import pandas as pd
from pathlib import Path


def inspect_attr_file(attr_file='resources/attrexc.xlsx'):
    """
    Выводит структуру файла attrexc.xlsx для понимания формата данных.
    """
    if not Path(attr_file).exists():
        print(f"❌ Файл {attr_file} не найден!")
        return None

    # Загружаем файл без заголовков, чтобы увидеть сырую структуру
    df = pd.read_excel(attr_file, header=None)

    print("=" * 80)
    print(f"📊 Структура файла: {attr_file}")
    print("=" * 80)
    print(f"Размер: {df.shape[0]} строк × {df.shape[1]} колонок")
    print()

    # Выводим первые 5 строк
    print(" Первые 5 строк:")
    print(df.head())
    print()

    # Выводим названия колонок (если есть)
    print("🏷️  Названия колонок (первые 60):")
    print(df.columns[:60].tolist())
    print()

    # Проверяем, есть ли коды атрибутов (AR, AW, BB, BE и т.д.)
    print("🔍 Поиск кодов атрибутов в первой строке:")
    first_row = df.iloc[0].tolist()
    attr_codes = [x for x in first_row if isinstance(x, str) and len(x) <= 3]
    print(f"Найдено кодов: {len(attr_codes)}")
    print(f"Примеры: {attr_codes[:20]}")
    print()

    # Проверяем, есть ли названия атрибутов (Вбр, Выб и т.д.)
    print("🔍 Поиск названий атрибутов во второй строке:")
    second_row = df.iloc[1].tolist()
    attr_names = [x for x in second_row if isinstance(x, str) and len(x) >= 2]
    print(f"Найдено названий: {len(attr_names)}")
    print(f"Примеры: {attr_names[:20]}")
    print()

    return df


# Запускаем инспекцию
if __name__ == '__main__':
    inspect_attr_file()
