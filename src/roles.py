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
                        mental_weights: dict,
                        physical_weights: dict) -> float:
        """
        Универсальный метод расчёта роли вратаря.

        Args:
            player_data: Словарь {название_атрибута: значение}
            goalkeeper_weights: Веса вратарских атрибутов
            mental_weights: Веса психологических атрибутов
            physical_weights: Веса физических атрибутов

        Returns:
            Рейтинг роли (0-100)
        """
        weighted_sum = 0.0
        max_possible = 0.0

        # Вратарские атрибуты
        for attr, weight in goalkeeper_weights.items():
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

        # Расчёт процента
        if max_possible == 0:
            return 0.0

        role_score = (weighted_sum / max_possible) * 100
        return round(role_score, 2)

    @staticmethod
    def defender(player_data: dict) -> float:
        """
        Вратарь (Зщ) - защитная обязанность.

        Зелёные (1.0): Вза, Выб, Иштр, Рук, Ркц, Взд
        Синие (0.75): Ввод, 1на1
        Психологические зелёные (1.0): Поз, Кнц
        Психологические синие (0.75): Инт, ПРш
        Физические зелёные (1.0): Лвк
        """
        goalkeeper_weights = {
            'Вза': 1.0,
            'Выб': 1.0,
            'Иштр': 1.0,
            'Рук': 1.0,
            'Ркц': 1.0,
            'Взд': 1.0,
            'Ввод': 0.75,
            '1на1': 0.75,
        }

        mental_weights = {
            'Поз': 1.0,
            'Кнц': 1.0,
            'Инт': 0.75,
            'ПРш': 0.75,
        }

        physical_weights = {
            'Лвк': 1.0,
        }

        return Goalkeeper._calculate_role(
            player_data,
            goalkeeper_weights,
            mental_weights,
            physical_weights
        )

    @staticmethod
    def sweeper_keeper_defend(player_data: dict) -> float:
        """Вратарь-чистильщик (Зщ) - защитная обязанность."""
        # TODO: Добавить веса когда будут известны
        # Пока используем веса от Вратарь (Зщ)
        return Goalkeeper.defender(player_data)

    @staticmethod
    def sweeper_keeper_support(player_data: dict) -> float:
        """Вратарь-чистильщик (По) - поддерживающая обязанность."""
        # TODO: Добавить веса когда будут известны
        return Goalkeeper.defender(player_data)

    @staticmethod
    def sweeper_keeper_attack(player_data: dict) -> float:
        """Вратарь-чистильщик (Ат) - атакующая обязанность."""
        # TODO: Добавить веса когда будут известны
        return Goalkeeper.defender(player_data)
