import pandas as pd
from pathlib import Path


def show_technical_attrs():
    """Показывает все колонки от AR до BE"""
    base_dir = Path(__file__).parent.parent
    attr_file = base_dir / 'resources' / 'attrexc.xlsx'

    df_attr = pd.read_excel(attr_file)

    print("=" * 80)
    print("📊 КОЛОНКИ ОТ AR ДО BE (Технические атрибуты полевых игроков)")
    print("=" * 80)

    # Получаем все колонки
    columns = df_attr.columns.tolist()

    # Находим индекс AR
    ar_index = columns.index('AR') if 'AR' in columns else None

    if ar_index is None:
        print("❌ Колонка AR не найдена!")
        return

    # Показываем колонки от AR до BE
    print(f"\n Колонки от AR (индекс {ar_index}) до конца:")
    print()

    for i in range(ar_index, len(columns)):
        col_name = columns[i]
        attr_name = df_attr[col_name].iloc[0]
        print(f"  {col_name:3} (индекс {i:2}) → {attr_name}")

    print()
    print("=" * 80)
    print(" Исключения для полевых игроков: AR, AW, BB, BE")
    print("=" * 80)


if __name__ == '__main__':
    show_technical_attrs()
