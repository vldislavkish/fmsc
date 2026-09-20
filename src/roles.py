"""
Классы для расчёта ролей игроков в Football Manager
"""


class Goalkeeper:
    """
    Класс для расчёта ролей вратарей.
    Все методы возвращают рейтинг от 0 до 100.
    """

    @staticmethod
    def _calculate_role(player_data: dict,
                        goalkeeper_weights: dict,
                        technical_weights: dict,
                        mental_weights: dict,
                        physical_weights: dict) -> float:
        """
        Универсальный метод расчёта роли вратаря.
        """
        weighted_sum = 0.0
        max_possible = 0.0

        # Вратарские атрибуты
        for attr, weight in goalkeeper_weights.items():
            value = player_data.get(attr, 0)
            weighted_sum += value * weight
            max_possible += 20 * weight

        # Технические атрибуты
        for attr, weight in technical_weights.items():
            value = player_data.get(attr, 0)
            weighted_sum += value * weight
            max_possible += 20 * weight

        # Психологические атрибуты
        for attr, weight in mental_weights.items():
            value = player_data.get(attr, 0)
            weighted_sum += value * weight
            max_possible += 20 * weight

        # Физические атрибуты
        for attr, weight in physical_weights.items():
            value = player_data.get(attr, 0)
            weighted_sum += value * weight
            max_possible += 20 * weight

        if max_possible == 0:
            return 0.0

        role_score = (weighted_sum / max_possible) * 100
        return round(role_score, 2)

    @staticmethod
    def standard(player_data: dict) -> float:
        """
        Вратарь (Зщ) - базовая/защитная обязанность.
        Зелёные (1.0): Вза, Выб, Иштр, Рук, Ркц, Взд
        Синие (0.75): Ввод, 1на1
        Психологические зелёные (1.0): Поз, Кнц
        Психологические синие (0.75): Инт, ПРш
        Физические зелёные (1.0): Лвк
        """
        goalkeeper_weights = {
            'Вза': 1.0, 'Выб': 1.0, 'Иштр': 1.0,
            'Рук': 1.0, 'Ркц': 1.0, 'Взд': 1.0,
            'Ввод': 0.75, '1на1': 0.75,
        }
        technical_weights = {}
        mental_weights = {
            'Поз': 1.0, 'Кнц': 1.0,
            'Инт': 0.75, 'ПРш': 0.75,
        }
        physical_weights = {'Лвк': 1.0}

        return Goalkeeper._calculate_role(
            player_data, goalkeeper_weights, technical_weights,
            mental_weights, physical_weights
        )

    # Алиас для обратной совместимости с parser.py
    defender = standard

    @staticmethod
    def sweeper_keeper_defend(player_data: dict) -> float:
        """Вратарь-чистильщик (Зщ)"""
        goalkeeper_weights = {
            'Выб': 1.0, 'Иштр': 1.0, '1на1': 1.0, 'Ркц': 1.0,
            'Ввод': 0.75, 'Вза': 0.75, 'Свв': 0.75,
            'Рук': 0.75, 'Взд': 0.75,
        }
        technical_weights = {'Пас': 0.75, 'ПКас': 0.75}
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Кнц': 1.0,
            'Вид': 0.75, 'ПРш': 0.75, 'Смб': 0.75,
        }
        physical_weights = {'Лвк': 1.0, 'Уск': 0.75}

        return Goalkeeper._calculate_role(
            player_data, goalkeeper_weights, technical_weights,
            mental_weights, physical_weights
        )

    @staticmethod
    def sweeper_keeper_support(player_data: dict) -> float:
        """Вратарь-чистильщик (По)"""
        goalkeeper_weights = {
            'Выб': 1.0, 'Иштр': 1.0, '1на1': 1.0, 'Ркц': 1.0, 'Свв': 1.0,
            'Ввод': 0.75, 'Вза': 0.75, 'Рук': 0.75, 'Взд': 0.75,
        }
        technical_weights = {'Пас': 0.75, 'ПКас': 0.75}
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Кнц': 1.0, 'Смб': 1.0,
            'Вид': 0.75, 'ПРш': 0.75,
        }
        physical_weights = {'Лвк': 1.0, 'Уск': 0.75}

        return Goalkeeper._calculate_role(
            player_data, goalkeeper_weights, technical_weights,
            mental_weights, physical_weights
        )

    @staticmethod
    def sweeper_keeper_attack(player_data: dict) -> float:
        """Вратарь-чистильщик (Ат)"""
        goalkeeper_weights = {
            'Выб': 1.0, 'Иштр': 1.0, '1на1': 1.0, 'Ркц': 1.0, 'Свв': 1.0,
            'Ввод': 0.75, 'Вза': 0.75, 'Рук': 0.75, 'Взд': 0.75, 'Экц': 0.75,
        }
        technical_weights = {'Пас': 0.75, 'ПКас': 0.75}
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Кнц': 1.0, 'Смб': 1.0,
            'Вид': 0.75, 'ПРш': 0.75,
        }
        physical_weights = {'Лвк': 1.0, 'Уск': 0.75}

        return Goalkeeper._calculate_role(
            player_data, goalkeeper_weights, technical_weights,
            mental_weights, physical_weights
        )


class CenterBack:
    """
    Класс для расчёта ролей центрального защитника.
    """

    @staticmethod
    def _calculate_role(player_data: dict,
                        technical_weights: dict,
                        mental_weights: dict,
                        physical_weights: dict) -> float:
        """Универсальный метод расчёта роли."""
        weighted_sum = 0.0
        max_possible = 0.0

        for attr, weight in technical_weights.items():
            value = player_data.get(attr, 0)
            weighted_sum += value * weight
            max_possible += 20 * weight

        for attr, weight in mental_weights.items():
            value = player_data.get(attr, 0)
            weighted_sum += value * weight
            max_possible += 20 * weight

        for attr, weight in physical_weights.items():
            value = player_data.get(attr, 0)
            weighted_sum += value * weight
            max_possible += 20 * weight

        if max_possible == 0:
            return 0.0

        return round((weighted_sum / max_possible) * 100, 2)

    @staticmethod
    def ball_playing_defend(player_data: dict) -> float:
        """Созидательный защитник (Зщ)"""
        technical_weights = {
            'Глв': 1.0, 'Опк': 1.0, 'Отб': 1.0, 'Пас': 1.0,
            'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Смб': 1.0,
            'Агр': 0.75, 'Вид': 0.75, 'Инт': 0.75,
            'Кнц': 0.75, 'ПРш': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'ПРГ': 1.0, 'СИЛ': 1.0,
            'Скр': 0.75,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def ball_playing_stop(player_data: dict) -> float:
        """Созидательный защитник (Бл) — блокирующий"""
        technical_weights = {
            'Глв': 1.0, 'Отб': 1.0, 'Пас': 1.0,
            'Опк': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Хрб': 1.0, 'Агр': 1.0, 'Поз': 1.0, 'Смб': 1.0, 'ПРш': 1.0,
            'Вид': 0.75, 'Инт': 0.75, 'Кнц': 0.75,
        }
        physical_weights = {
            'ПРГ': 1.0, 'СИЛ': 1.0,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def ball_playing_cover(player_data: dict) -> float:
        """Созидательный защитник (Пс) — страховка"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0, 'Пас': 1.0,
            'Глв': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Смб': 1.0, 'Инт': 1.0, 'Кнц': 1.0, 'ПРш': 1.0,
            'Вид': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'Скр': 1.0, 'ПРГ': 1.0,
            'СИЛ': 0.75,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def ball_playing_overall(player_data: dict) -> float:
        """Созидательный защитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            CenterBack.ball_playing_defend(player_data),
            CenterBack.ball_playing_stop(player_data),
            CenterBack.ball_playing_cover(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === ЗАГЛУШКИ для остальных ролей (вернут 0.0 пока не добавим веса) ===

    @staticmethod
    def libero_overall(player_data: dict) -> float:
        """Либеро (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def libero_support(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def libero_attack(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def wide_center_back_overall(player_data: dict) -> float:
        """Крайний центральный защитник (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def wide_center_back_defend(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def wide_center_back_support(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def wide_center_back_attack(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def central_defender_overall(player_data: dict) -> float:
        """Центральный защитник (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def central_defender_defend(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def central_defender_stop(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def central_defender_cover(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def no_nonsense_overall(player_data: dict) -> float:
        """Чистый центральный защитник (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def no_nonsense_defend(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def no_nonsense_stop(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def no_nonsense_cover(player_data: dict) -> float:
        return 0.0

    @staticmethod
    def overall(player_data: dict) -> float:
        """ЦЗ (ОВР) — среднее по всем реализованным ролям"""
        # Пока считаем только по Созидательному защитнику
        # Когда добавим остальные — расширим
        bp = CenterBack.ball_playing_overall(player_data)
        return bp  # Заглушка, пока нет других ролей
