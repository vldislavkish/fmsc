"""
Главный модуль проекта FMSC
Точка входа в программу
"""
import sys
from src import parser, utils


def main():
    """
    Основная функция программы.
    Парсит последний HTML файл из папки data и сохраняет результаты.
    """
    print("=" * 60)
    print("🎮 FMSC - Football Manager Squad Converter")
    print("=" * 60)
    print()

    try:
        # 1. Находим последний HTML файл
        html_file = parser.get_latest_html()
        print(f"📁 Найден файл: {html_file}")
        print()

        # 2. Парсим данные
        df = parser.parse_squad(html_file)
        print()

        # 3. Сохраняем результаты
        utils.save_results(df)
        print()

        print("🎉 Программа завершена успешно!")

    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}")
        print("💡 Убедитесь, что в папке 'data' есть хотя бы один HTML файл.")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
