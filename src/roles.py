"""
Классы для расчёта ролей игроков в Football Manager
"""

class Goalkeeper:
    """Класс для расчёта ролей вратарей."""

    @staticmethod
    def _calculate_role(player_data: dict, goalkeeper_weights: dict, technical_weights: dict, mental_weights: dict, physical_weights: dict) -> float:
        weighted_sum = sum(player_data.get(attr, 0) * weight for attr, weight in {**goalkeeper_weights, **technical_weights, **mental_weights, **physical_weights}.items())
        max_possible = sum(20 * weight for weight in {**goalkeeper_weights, **technical_weights, **mental_weights, **physical_weights}.values())
        return round((weighted_sum / max_possible) * 100, 2) if max_possible > 0 else 0.0

    @staticmethod
    def defender(player_data: dict) -> float:
        return Goalkeeper._calculate_role(player_data,
            {'Вза': 1.0, 'Выб': 1.0, 'Иштр': 1.0, 'Рук': 1.0, 'Ркц': 1.0, 'Взд': 1.0, 'Ввод': 0.75, '1на1': 0.75},
            {},
            {'Поз': 1.0, 'Кнц': 1.0, 'Инт': 0.75, 'ПРш': 0.75},
            {'Лвк': 1.0}
        )

    @staticmethod
    def sweeper_keeper_defend(player_data: dict) -> float:
        return Goalkeeper._calculate_role(player_data,
            {'Выб': 1.0, 'Иштр': 1.0, '1на1': 1.0, 'Ркц': 1.0, 'Ввод': 0.75, 'Вза': 0.75, 'Свв': 0.75, 'Рук': 0.75, 'Взд': 0.75},
            {'Пас': 0.75, 'ПКас': 0.75},
            {'Поз': 1.0, 'Инт': 1.0, 'Кнц': 1.0, 'Вид': 0.75, 'ПРш': 0.75, 'Смб': 0.75},
            {'Лвк': 1.0, 'Уск': 0.75}
        )

    @staticmethod
    def sweeper_keeper_support(player_data: dict) -> float:
        return Goalkeeper._calculate_role(player_data,
            {'Выб': 1.0, 'Иштр': 1.0, '1на1': 1.0, 'Ркц': 1.0, 'Свв': 1.0, 'Ввод': 0.75, 'Вза': 0.75, 'Рук': 0.75, 'Взд': 0.75},
            {'Пас': 0.75, 'ПКас': 0.75},
            {'Поз': 1.0, 'Инт': 1.0, 'Кнц': 1.0, 'Смб': 1.0, 'Вид': 0.75, 'ПРш': 0.75},
            {'Лвк': 1.0, 'Уск': 0.75}
        )

    @staticmethod
    def sweeper_keeper_attack(player_data: dict) -> float:
        return Goalkeeper._calculate_role(player_data,
            {'Выб': 1.0, 'Иштр': 1.0, '1на1': 1.0, 'Ркц': 1.0, 'Свв': 1.0, 'Ввод': 0.75, 'Вза': 0.75, 'Рук': 0.75, 'Взд': 0.75, 'Экц': 0.75},
            {'Пас': 0.75, 'ПКас': 0.75},
            {'Поз': 1.0, 'Инт': 1.0, 'Кнц': 1.0, 'Смб': 1.0, 'Вид': 0.75, 'ПРш': 0.75},
            {'Лвк': 1.0, 'Уск': 0.75}
        )

    @staticmethod
    def overall(player_data: dict) -> float:
        roles = [Goalkeeper.defender(player_data), Goalkeeper.sweeper_keeper_defend(player_data), Goalkeeper.sweeper_keeper_support(player_data), Goalkeeper.sweeper_keeper_attack(player_data)]
        return round(sum(roles) / len(roles), 2)


class CenterBack:
    """Класс для расчёта ролей центрального защитника."""

    @staticmethod
    def _calculate_role(player_data: dict, technical_weights: dict, mental_weights: dict, physical_weights: dict) -> float:
        weighted_sum = sum(player_data.get(attr, 0) * weight for attr, weight in {**technical_weights, **mental_weights, **physical_weights}.items())
        max_possible = sum(20 * weight for weight in {**technical_weights, **mental_weights, **physical_weights}.values())
        return round((weighted_sum / max_possible) * 100, 2) if max_possible > 0 else 0.0

    @staticmethod
    def ball_playing_defend(player_data: dict) -> float:
        return CenterBack._calculate_role(player_data,
            {'Глв': 1.0, 'Опк': 1.0, 'Отб': 1.0, 'Пас': 1.0, 'ПКас': 0.75, 'Тех': 0.75},
            {'Поз': 1.0, 'Смб': 1.0, 'Агр': 0.75, 'Вид': 0.75, 'Инт': 0.75, 'Кнц': 0.75, 'ПРш': 0.75, 'Хрб': 0.75},
            {'ПРГ': 1.0, 'СИЛ': 1.0, 'Скр': 0.75}
        )

    @staticmethod
    def ball_playing_stop(player_data: dict) -> float:
        return CenterBack._calculate_role(player_data,
            {'Глв': 1.0, 'Отб': 1.0, 'Пас': 1.0, 'Опк': 0.75, 'ПКас': 0.75, 'Тех': 0.75},
            {'Хрб': 1.0, 'Агр': 1.0, 'Поз': 1.0, 'Смб': 1.0, 'ПРш': 1.0, 'Вид': 0.75, 'Инт': 0.75, 'Кнц': 0.75},
            {'ПРГ': 1.0, 'СИЛ': 1.0}
        )

    @staticmethod
    def ball_playing_cover(player_data: dict) -> float:
        return CenterBack._calculate_role(player_data,
            {'Опк': 1.0, 'Отб': 1.0, 'Пас': 1.0, 'Глв': 0.75, 'ПКас': 0.75, 'Тех': 0.75},
            {'Поз': 1.0, 'Смб': 1.0, 'Инт': 1.0, 'Кнц': 1.0, 'ПРш': 1.0, 'Вид': 0.75, 'Хрб': 0.75},
            {'Скр': 1.0, 'ПРГ': 1.0, 'СИЛ': 0.75}
        )

    @staticmethod
    def ball_playing_overall(player_data: dict) -> float:
        roles = [CenterBack.ball_playing_defend(player_data), CenterBack.ball_playing_stop(player_data), CenterBack.ball_playing_cover(player_data)]
        return round(sum(roles) / len(roles), 2)

    @staticmethod
    def libero_support(player_data: dict) -> float:
        """Либеро (По) - поддерживающая обязанность"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0, 'Пас': 1.0, 'ПКас': 1.0,
            'Дрб': 0.75, 'Глв': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Вид': 1.0, 'Поз': 1.0, 'Инт': 1.0, 'Ком': 1.0,
            'Кнц': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Имп': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'Скр': 1.0,
            'ВЫН': 0.75, 'ПРГ': 0.75, 'КРД': 0.75, 'Лвк': 0.75, 'СИЛ': 0.75,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def libero_attack(player_data: dict) -> float:
        """Либеро (Ат) - атакующая обязанность"""
        technical_weights = {
            'Дрб': 1.0, 'Опк': 1.0, 'Отб': 1.0, 'Пас': 1.0, 'ПКас': 1.0,
            'Длн': 0.75, 'Глв': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Вид': 1.0, 'Поз': 1.0, 'Имп': 1.0, 'Инт': 1.0,
            'Ком': 1.0, 'Кнц': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Хрб': 0.75,
        }
        physical_weights = {
            'Скр': 1.0,
            'ВЫН': 0.75, 'ПРГ': 0.75, 'КРД': 0.75,
            'Лвк': 0.75, 'СИЛ': 0.75, 'Уск': 0.75,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def libero_overall(player_data: dict) -> float:
        """Либеро (ОВР) — среднее арифметическое ролей"""
        roles = [
            CenterBack.libero_support(player_data),
            CenterBack.libero_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    @staticmethod
    def wide_center_back_defend(player_data: dict) -> float:
        """Крайний центральный защитник (Зщ)"""
        technical_weights = {
            'Глв': 1.0, 'Опк': 1.0, 'Отб': 1.0, 'Нав': 1.0,
            'Дрб': 0.75,
        }
        mental_weights = {
            'Поз': 1.0,
            'Раб': 0.75, 'Смб': 0.75, 'Хрб': 0.75,
            'Инт': 0.75, 'Кнц': 0.75, 'ПРш': 0.75, 'Агр': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'ПРГ': 1.0, 'СИЛ': 1.0,
            'Скр': 0.75,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def wide_center_back_support(player_data: dict) -> float:
        """Крайний центральный защитник (По)"""
        technical_weights = {
            'Дрб': 1.0, 'Глв': 1.0, 'Нав': 1.0, 'Опк': 1.0, 'Отб': 1.0,
        }
        mental_weights = {
            'Поз': 1.0,
            'Агр': 0.75, 'Ибм': 0.75, 'Инт': 0.75, 'Кнц': 0.75,
            'ПРш': 0.75, 'Раб': 0.75, 'Смб': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'ПРГ': 1.0, 'СИЛ': 1.0, 'Скр': 1.0,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def wide_center_back_attack(player_data: dict) -> float:
        """Крайний центральный защитник (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Глв': 1.0, 'Нав': 1.0, 'Опк': 1.0, 'Отб': 1.0,
        }
        mental_weights = {
            'Ибм': 1.0,
            'Агр': 0.75, 'Поз': 0.75, 'Инт': 0.75, 'Кнц': 0.75,
            'ПРш': 0.75, 'Раб': 0.75, 'Смб': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'ПРГ': 1.0, 'СИЛ': 1.0, 'Скр': 1.0,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def wide_center_back_overall(player_data: dict) -> float:
        """Крайний центральный защитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            CenterBack.wide_center_back_defend(player_data),
            CenterBack.wide_center_back_support(player_data),
            CenterBack.wide_center_back_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    @staticmethod
    def central_defender_defend(player_data: dict) -> float:
        """Центральный защитник (Зщ)"""
        technical_weights = {
            'Глв': 1.0, 'Опк': 1.0, 'Отб': 1.0,
        }
        mental_weights = {
            'Поз': 1.0,
            'Агр': 0.75, 'Инт': 0.75, 'Кнц': 0.75,
            'ПРш': 0.75, 'Смб': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'ПРГ': 1.0, 'СИЛ': 1.0,
            'Скр': 0.75,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def central_defender_stop(player_data: dict) -> float:
        """Центральный защитник (Бл)"""
        technical_weights = {
            'Глв': 1.0, 'Отб': 1.0,
            'Опк': 0.75,
        }
        mental_weights = {
            'Агр': 1.0, 'Поз': 1.0, 'ПРш': 1.0, 'Хрб': 1.0,
            'Инт': 0.75, 'Кнц': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ПРГ': 1.0, 'СИЛ': 1.0,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def central_defender_cover(player_data: dict) -> float:
        """Центральный защитник (Пс)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0,
            'Глв': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Кнц': 1.0, 'ПРш': 1.0,
            'Смб': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'Скр': 1.0,
            'ПРГ': 0.75, 'СИЛ': 0.75,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def central_defender_overall(player_data: dict) -> float:
        """Центральный защитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            CenterBack.central_defender_defend(player_data),
            CenterBack.central_defender_stop(player_data),
            CenterBack.central_defender_cover(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    @staticmethod
    def no_nonsense_defend(player_data: dict) -> float:
        """Чистый центральный защитник (Зщ)"""
        technical_weights = {
            'Глв': 1.0, 'Опк': 1.0, 'Отб': 1.0,
        }
        mental_weights = {
            'Поз': 1.0,
            'Агр': 0.75, 'Инт': 0.75, 'Кнц': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'ПРГ': 1.0, 'СИЛ': 1.0,
            'Скр': 0.75,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def no_nonsense_stop(player_data: dict) -> float:
        """Чистый центральный защитник (Бл)"""
        technical_weights = {
            'Глв': 1.0, 'Отб': 1.0,
            'Опк': 0.75,
        }
        mental_weights = {
            'Агр': 1.0, 'Поз': 1.0, 'Хрб': 1.0,
            'Инт': 0.75, 'Кнц': 0.75,
        }
        physical_weights = {
            'ПРГ': 1.0, 'СИЛ': 1.0,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def no_nonsense_cover(player_data: dict) -> float:
        """Чистый центральный защитник (Пс)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0,
            'Глв': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Кнц': 1.0,
            'Хрб': 0.75,
        }
        physical_weights = {
            'Скр': 1.0,
            'ПРГ': 0.75, 'СИЛ': 0.75,
        }
        return CenterBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def no_nonsense_overall(player_data: dict) -> float:
        """Чистый центральный защитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            CenterBack.no_nonsense_defend(player_data),
            CenterBack.no_nonsense_stop(player_data),
            CenterBack.no_nonsense_cover(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    @staticmethod
    def overall(player_data: dict) -> float:
        """Универсальность ЦЗ — среднее всех 5 ролей"""
        roles = [
            CenterBack.ball_playing_overall(player_data),
            CenterBack.libero_overall(player_data),
            CenterBack.wide_center_back_overall(player_data),
            CenterBack.central_defender_overall(player_data),
            CenterBack.no_nonsense_overall(player_data),
        ]
        return round(sum(roles) / len(roles), 2)


class FullBack:
    """Класс для расчёта ролей крайнего защитника."""

    @staticmethod
    def _calculate_role(player_data: dict,
                        technical_weights: dict,
                        mental_weights: dict,
                        physical_weights: dict) -> float:
        """Универсальный метод расчёта роли."""
        weighted_sum = sum(player_data.get(attr, 0) * weight
                           for attr, weight in {**technical_weights, **mental_weights, **physical_weights}.items())
        max_possible = sum(20 * weight
                           for weight in {**technical_weights, **mental_weights, **physical_weights}.values())
        return round((weighted_sum / max_possible) * 100, 2) if max_possible > 0 else 0.0

    # === Фланговый защитник ===
    @staticmethod
    def wing_back_defend(player_data: dict) -> float:
        """Фланговый защитник (Зщ)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0,
            'Нав': 0.75, 'Пас': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Кнц': 1.0,
            'Ком': 0.75, 'ПРш': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 0.75, 'Скр': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def wing_back_support(player_data: dict) -> float:
        """Фланговый защитник (По)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0,
            'Нав': 0.75, 'Дрб': 0.75, 'Пас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Ком': 1.0, 'Кнц': 1.0, 'Раб': 1.0,
            'ПРш': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 0.75, 'Скр': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def wing_back_attack(player_data: dict) -> float:
        """Фланговый защитник (Ат)"""
        technical_weights = {
            'Нав': 1.0, 'Отб': 1.0,
            'Дрб': 0.75, 'Опк': 0.75, 'Пас': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Ком': 1.0, 'Раб': 1.0,
            'Ибм': 0.75, 'Кнц': 0.75, 'ПРш': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'Скр': 1.0,
            'Лвк': 0.75, 'Уск': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def wing_back_overall(player_data: dict) -> float:
        """Фланговый защитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            FullBack.wing_back_defend(player_data),
            FullBack.wing_back_support(player_data),
            FullBack.wing_back_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Крайний защитник (Full-back) ===

    @staticmethod
    def full_back_defend(player_data: dict) -> float:
        """Крайний защитник (Зщ)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0,
            'Дрб': 0.75, 'Нав': 0.75, 'Пас': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Ком': 1.0, 'Раб': 1.0,
            'Ибм': 0.75, 'Кнц': 0.75, 'ПРш': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'Уск': 1.0,
            'Лвк': 0.75, 'Скр': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def full_back_support(player_data: dict) -> float:
        """Крайний защитник (По)"""
        technical_weights = {
            'Дрб': 1.0, 'Нав': 1.0, 'Опк': 1.0, 'Отб': 1.0,
            'Пас': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Ком': 1.0, 'Раб': 1.0,
            'Поз': 0.75, 'Инт': 0.75, 'Кнц': 0.75, 'ПРш': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'Уск': 1.0,
            'Лвк': 0.75, 'Скр': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def full_back_attack(player_data: dict) -> float:
        """Крайний защитник (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Нав': 1.0, 'Отб': 1.0, 'Тех': 1.0,
            'Опк': 0.75, 'Пас': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Ком': 1.0, 'Раб': 1.0,
            'Поз': 0.75, 'Имп': 0.75, 'Инт': 0.75, 'Кнц': 0.75, 'ПРш': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'Скр': 1.0, 'Уск': 1.0,
            'Лвк': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def full_back_overall(player_data: dict) -> float:
        """Крайний защитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            FullBack.full_back_defend(player_data),
            FullBack.full_back_support(player_data),
            FullBack.full_back_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Атакующий крайний защитник ===

    @staticmethod
    def attacking_wing_back_support(player_data: dict) -> float:
        """Атакующий крайний защитник (По)"""
        technical_weights = {
            'Дрб': 1.0, 'Нав': 1.0, 'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Отб': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Раб': 1.0,
            'Имп': 0.75, 'Инт': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'Скр': 1.0, 'Уск': 1.0,
            'КРД': 0.75, 'Лвк': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def attacking_wing_back_attack(player_data: dict) -> float:
        """Атакующий крайний защитник (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Нав': 1.0, 'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Отб': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Имп': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Раб': 1.0,
            'Инт': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'Скр': 1.0, 'Уск': 1.0,
            'КРД': 0.75, 'Лвк': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def attacking_wing_back_overall(player_data: dict) -> float:
        """Атакующий крайний защитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            FullBack.attacking_wing_back_support(player_data),
            FullBack.attacking_wing_back_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Полуфланговый крайний защитник ===

    @staticmethod
    def half_wing_back_defend(player_data: dict) -> float:
        """Полуфланговый крайний защитник (Зщ)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0, 'Пас': 1.0,
            'Дрб': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Раб': 1.0,
            'Ибм': 0.75, 'Кнц': 0.75,
        }
        physical_weights = {
            'ВЫН': 0.75, 'Лвк': 0.75, 'Уск': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def half_wing_back_support(player_data: dict) -> float:
        """Полуфланговый крайний защитник (По)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0, 'Пас': 1.0,
            'Дрб': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Раб': 1.0,
            'Поз': 0.75, 'Инт': 0.75, 'Кнц': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0,
            'Лвк': 0.75, 'Уск': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def half_wing_back_attack(player_data: dict) -> float:
        """Полуфланговый крайний защитник (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Опк': 1.0, 'Отб': 1.0, 'Пас': 1.0, 'Тех': 1.0,
            'Длн': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Раб': 1.0,
            'Поз': 0.75, 'Имп': 0.75, 'Инт': 0.75, 'Кнц': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'Уск': 1.0,
            'Лвк': 0.75, 'Скр': 0.75,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def half_wing_back_overall(player_data: dict) -> float:
        """Полуфланговый крайний защитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            FullBack.half_wing_back_defend(player_data),
            FullBack.half_wing_back_support(player_data),
            FullBack.half_wing_back_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Чистый крайний защитник ===

    @staticmethod
    def no_nonsense_full_back_defend(player_data: dict) -> float:
        """Чистый крайний защитник (Зщ)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0,
            'Глв': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0,
            'Агр': 0.75, 'Ком': 0.75, 'Кнц': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'СИЛ': 1.0,
        }
        return FullBack._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def no_nonsense_full_back_overall(player_data: dict) -> float:
        """Чистый крайний защитник (ОВР) — пока только одна роль"""
        return FullBack.no_nonsense_full_back_defend(player_data)

    @staticmethod
    def overall(player_data: dict) -> float:
        """Универсальность КЗ — среднее всех 5 ролей"""
        roles = [
            FullBack.wing_back_overall(player_data),
            FullBack.full_back_overall(player_data),
            FullBack.attacking_wing_back_overall(player_data),
            FullBack.half_wing_back_overall(player_data),
            FullBack.no_nonsense_full_back_overall(player_data),
        ]
        return round(sum(roles) / len(roles), 2)


class DefensiveMidfielder:
    """Класс для расчёта ролей опорного полузащитника."""

    @staticmethod
    def _calculate_role(player_data: dict,
                        technical_weights: dict,
                        mental_weights: dict,
                        physical_weights: dict) -> float:
        """Универсальный метод расчёта роли."""
        weighted_sum = sum(player_data.get(attr, 0) * weight
                           for attr, weight in {**technical_weights, **mental_weights, **physical_weights}.items())
        max_possible = sum(20 * weight
                           for weight in {**technical_weights, **mental_weights, **physical_weights}.values())
        return round((weighted_sum / max_possible) * 100, 2) if max_possible > 0 else 0.0

    # === Опорный полузащитник ===
    @staticmethod
    def defensive_midfielder_defend(player_data: dict) -> float:
        """Опорный полузащитник (Зщ)"""
        technical_weights = {
            'Отб': 1.0,
            'Опк': 0.75, 'Пас': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Ком': 1.0, 'Кнц': 1.0,
            'Агр': 0.75, 'ПРш': 0.75, 'Раб': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 0.75, 'СИЛ': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def defensive_midfielder_support(player_data: dict) -> float:
        """Опорный полузащитник (По)"""
        technical_weights = {
            'Отб': 1.0,
            'Опк': 0.75, 'Пас': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Ком': 1.0, 'Кнц': 1.0,
            'Агр': 0.75, 'ПРш': 0.75, 'Раб': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 0.75, 'СИЛ': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def defensive_midfielder_overall(player_data: dict) -> float:
        """Опорный полузащитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            DefensiveMidfielder.defensive_midfielder_defend(player_data),
            DefensiveMidfielder.defensive_midfielder_support(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Оттянутый плеймейкер ===
    @staticmethod
    def deep_lying_playmaker_defend(player_data: dict) -> float:
        """Оттянутый плеймейкер (Зщ)"""
        technical_weights = {
            'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Отб': 0.75,
        }
        mental_weights = {
            'ВПл': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Поз': 0.75, 'Инт': 0.75,
        }
        physical_weights = {
            'КРД': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def deep_lying_playmaker_support(player_data: dict) -> float:
        """Оттянутый плеймейкер (По)"""
        technical_weights = {
            'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
        }
        mental_weights = {
            'ВПл': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Поз': 0.75, 'Ибм': 0.75, 'Инт': 0.75,
        }
        physical_weights = {
            'КРД': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def deep_lying_playmaker_overall(player_data: dict) -> float:
        """Оттянутый плеймейкер (ОВР) — среднее арифметическое ролей"""
        roles = [
            DefensiveMidfielder.deep_lying_playmaker_defend(player_data),
            DefensiveMidfielder.deep_lying_playmaker_support(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Полузащитник-разрушитель ===
    @staticmethod
    def ball_winning_midfielder_defend(player_data: dict) -> float:
        """Полузащитник-разрушитель (Зщ)"""
        technical_weights = {
            'Отб': 1.0,
            'Опк': 0.75,
        }
        mental_weights = {
            'Агр': 1.0, 'Инт': 1.0, 'Ком': 1.0, 'Раб': 1.0,
            'Поз': 0.75, 'Кнц': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0,
            'Лвк': 0.75, 'СИЛ': 0.75, 'Скр': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def ball_winning_midfielder_support(player_data: dict) -> float:
        """Полузащитник-разрушитель (По)"""
        technical_weights = {
            'Отб': 1.0,
            'Опк': 0.75, 'Пас': 0.75,
        }
        mental_weights = {
            'Агр': 1.0, 'Инт': 1.0, 'Ком': 1.0, 'Раб': 1.0,
            'Кнц': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0,
            'Лвк': 0.75, 'СИЛ': 0.75, 'Скр': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def ball_winning_midfielder_overall(player_data: dict) -> float:
        """Полузащитник-разрушитель (ОВР) — среднее арифметическое ролей"""
        roles = [
            DefensiveMidfielder.ball_winning_midfielder_defend(player_data),
            DefensiveMidfielder.ball_winning_midfielder_support(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Чистый опорный полузащитник ===

    @staticmethod
    def anchor_man_defend(player_data: dict) -> float:
        """Чистый опорный полузащитник (Зщ)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Кнц': 1.0, 'ПРш': 1.0,
            'Ком': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'СИЛ': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def anchor_man_overall(player_data: dict) -> float:
        """Чистый опорный полузащитник (ОВР)"""
        # Пока реализована только защитная обязанность
        return DefensiveMidfielder.anchor_man_defend(player_data)

    # === Хавбек ===

    @staticmethod
    def half_back_defend(player_data: dict) -> float:
        """Хавбек (Зщ)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0,
            'Пас': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Инт': 1.0, 'Ком': 1.0, 'Кнц': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Агр': 0.75, 'Раб': 0.75, 'Хрб': 0.75,
        }
        physical_weights = {
            'ВЫН': 0.75, 'ПРГ': 0.75, 'СИЛ': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def half_back_overall(player_data: dict) -> float:
        """Хавбек (ОВР)"""
        # Пока реализована только защитная обязанность
        return DefensiveMidfielder.half_back_defend(player_data)

    # === Реджиста ===

    @staticmethod
    def regista_support(player_data: dict) -> float:
        """Реджиста (По)"""
        technical_weights = {
            'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Длн': 0.75, 'Дрб': 0.75,
        }
        mental_weights = {
            'Вид': 1.0, 'Ибм': 1.0, 'Имп': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Инт': 0.75,
        }
        physical_weights = {
            'КРД': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def regista_overall(player_data: dict) -> float:
        """Реджиста (ОВР) — у роли только одна обязанность (По)"""
        return DefensiveMidfielder.regista_support(player_data)

    # === Блуждающий плеймейкер ===

    @staticmethod
    def roamer_support(player_data: dict) -> float:
        """Блуждающий плеймейкер (По)"""
        technical_weights = {
            'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Длн': 0.75, 'Дрб': 0.75,
        }
        mental_weights = {
            'Вид': 1.0, 'Ибм': 1.0, 'Инт': 1.0, 'Ком': 1.0,
            'ПРш': 1.0, 'Раб': 1.0, 'Смб': 1.0,
            'Поз': 0.75, 'Кнц': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'Уск': 1.0,
            'КРД': 0.75, 'Лвк': 0.75, 'Скр': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def roamer_overall(player_data: dict) -> float:
        """Блуждающий плеймейкер (ОВР) — у роли только одна обязанность (По)"""
        return DefensiveMidfielder.roamer_support(player_data)

    # === Сегундо-воланте ===

    @staticmethod
    def segundo_volante_support(player_data: dict) -> float:
        """Сегундо-воланте (По)"""
        technical_weights = {
            'Опк': 1.0, 'Отб': 1.0, 'Пас': 1.0,
            'Длн': 0.75, 'Зав': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Ибм': 1.0, 'Раб': 1.0,
            'Инт': 0.75, 'Кнц': 0.75, 'ПРш': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'Скр': 1.0,
            'КРД': 0.75, 'СИЛ': 0.75, 'Уск': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def segundo_volante_attack(player_data: dict) -> float:
        """Сегундо-воланте (Ат)"""
        technical_weights = {
            'Длн': 1.0, 'Зав': 1.0, 'Отб': 1.0, 'Пас': 1.0,
            'Опк': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Ибм': 1.0, 'Инт': 1.0, 'Раб': 1.0,
            'Кнц': 0.75, 'ПРш': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0, 'Скр': 1.0,
            'КРД': 0.75, 'СИЛ': 0.75, 'Уск': 0.75,
        }
        return DefensiveMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def segundo_volante_overall(player_data: dict) -> float:
        """Сегундо-воланте (ОВР) — среднее арифметическое ролей"""
        roles = [
            DefensiveMidfielder.segundo_volante_support(player_data),
            DefensiveMidfielder.segundo_volante_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    @staticmethod
    def overall(player_data: dict) -> float:
        """Универсальность ОП — среднее всех 8 ролей"""
        roles = [
            DefensiveMidfielder.defensive_midfielder_overall(player_data),
            DefensiveMidfielder.deep_lying_playmaker_overall(player_data),
            DefensiveMidfielder.ball_winning_midfielder_overall(player_data),
            DefensiveMidfielder.anchor_man_overall(player_data),
            DefensiveMidfielder.half_back_overall(player_data),
            DefensiveMidfielder.regista_overall(player_data),
            DefensiveMidfielder.roamer_overall(player_data),
            DefensiveMidfielder.segundo_volante_overall(player_data),
        ]
        active_roles = [r for r in roles if r > 0]
        if not active_roles:
            return 0.0
        return round(sum(active_roles) / len(active_roles), 2)


class CentralMidfielder:
    """Класс для расчёта ролей центрального полузащитника."""

    @staticmethod
    def _calculate_role(player_data: dict,
                        technical_weights: dict,
                        mental_weights: dict,
                        physical_weights: dict) -> float:
        """Универсальный метод расчёта роли."""
        weighted_sum = sum(player_data.get(attr, 0) * weight
                           for attr, weight in {**technical_weights, **mental_weights, **physical_weights}.items())
        max_possible = sum(20 * weight
                           for weight in {**technical_weights, **mental_weights, **physical_weights}.values())
        return round((weighted_sum / max_possible) * 100, 2) if max_possible > 0 else 0.0

    @staticmethod
    def deep_lying_playmaker_overall(player_data: dict) -> float:
        """Оттянутый плеймейкер — используем реализацию из DefensiveMidfielder"""
        return DefensiveMidfielder.deep_lying_playmaker_overall(player_data)

    @staticmethod
    def ball_winning_midfielder_overall(player_data: dict) -> float:
        """Полузащитник-разрушитель — используем реализацию из DefensiveMidfielder"""
        return DefensiveMidfielder.ball_winning_midfielder_overall(player_data)

    @staticmethod
    def roamer_overall(player_data: dict) -> float:
        """Блуждающий плеймейкер — используем реализацию из DefensiveMidfielder"""
        return DefensiveMidfielder.roamer_overall(player_data)

    # === Центральный полузащитник ===
    @staticmethod
    def central_midfielder_defend(player_data: dict) -> float:
        """Центральный полузащитник (Зщ)"""
        technical_weights = {
            'Отб': 1.0,
            'Опк': 0.75, 'Пас': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Ком': 1.0, 'Кнц': 1.0, 'ПРш': 1.0,
            'Агр': 0.75, 'Инт': 0.75, 'Раб': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 0.75,
        }
        return CentralMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def central_midfielder_support(player_data: dict) -> float:
        """Центральный полузащитник (По)"""
        technical_weights = {
            'Отб': 1.0, 'Пас': 1.0, 'ПКас': 1.0,
            'Тех': 0.75,
        }
        mental_weights = {
            'Ком': 1.0, 'ПРш': 1.0,
            'Вид': 0.75, 'Ибм': 0.75, 'Инт': 0.75, 'Кнц': 0.75, 'Раб': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 0.75,
        }
        return CentralMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def central_midfielder_attack(player_data: dict) -> float:
        """Центральный полузащитник (Ат)"""
        technical_weights = {
            'Пас': 1.0, 'ПКас': 1.0,
            'Длн': 0.75, 'Отб': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'ПРш': 1.0,
            'Вид': 0.75, 'Инт': 0.75, 'Ком': 0.75, 'Раб': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 0.75, 'Уск': 0.75,
        }
        return CentralMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def central_midfielder_overall(player_data: dict) -> float:
        """Центральный полузащитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            CentralMidfielder.central_midfielder_defend(player_data),
            CentralMidfielder.central_midfielder_support(player_data),
            CentralMidfielder.central_midfielder_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Полузащитник бокс-ту-бокс ===
    @staticmethod
    def box_to_box_midfielder_support(player_data: dict) -> float:
        """Полузащитник бокс-ту-бокс (По)"""
        technical_weights = {
            'Отб': 1.0, 'Пас': 1.0,
            'Длн': 0.75, 'Дрб': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Ком': 1.0, 'Раб': 1.0,
            'Агр': 0.75, 'Поз': 0.75, 'Инт': 0.75, 'ПРш': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0,
            'КРД': 0.75, 'СИЛ': 0.75, 'Скр': 0.75, 'Уск': 0.75,
        }
        return CentralMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def box_to_box_midfielder_overall(player_data: dict) -> float:
        """Полузащитник бокс-ту-бокс (ОВР) — пока только одна обязанность (По)"""
        return CentralMidfielder.box_to_box_midfielder_support(player_data)

    # === Выдвинутый плеймейкер ===
    @staticmethod
    def advanced_playmaker_support(player_data: dict) -> float:
        """Выдвинутый плеймейкер (По)"""
        technical_weights = {
            'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Дрб': 0.75,
        }
        mental_weights = {
            'Вид': 1.0, 'Ибм': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Имп': 0.75, 'Инт': 0.75,
        }
        physical_weights = {
            'Лвк': 0.75,
        }
        return CentralMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def advanced_playmaker_attack(player_data: dict) -> float:
        """Выдвинутый плеймейкер (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
        }
        mental_weights = {
            'Вид': 1.0, 'Ибм': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Имп': 0.75, 'Инт': 0.75,
        }
        physical_weights = {
            'Лвк': 0.75, 'Уск': 0.75,
        }
        return CentralMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def advanced_playmaker_overall(player_data: dict) -> float:
        """Выдвинутый плеймейкер (ОВР) — среднее арифметическое ролей"""
        roles = [
            CentralMidfielder.advanced_playmaker_support(player_data),
            CentralMidfielder.advanced_playmaker_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Меццала ===
    @staticmethod
    def mezzala_support(player_data: dict) -> float:
        """Меццала (По)"""
        technical_weights = {
            'Пас': 1.0, 'Тех': 1.0,
            'Длн': 0.75, 'Дрб': 0.75, 'Отб': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'ПРш': 1.0, 'Раб': 1.0,
            'Вид': 0.75, 'Инт': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'Уск': 1.0,
            'ВЫН': 0.75, 'КРД': 0.75,
        }
        return CentralMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def mezzala_attack(player_data: dict) -> float:
        """Меццала (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Пас': 1.0, 'Тех': 1.0,
            'Длн': 0.75, 'Зав': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Вид': 1.0, 'Ибм': 1.0, 'ПРш': 1.0, 'Раб': 1.0,
            'Имп': 0.75, 'Инт': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'Уск': 1.0,
            'ВЫН': 0.75, 'КРД': 0.75,
        }
        return CentralMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def mezzala_overall(player_data: dict) -> float:
        """Меццала (ОВР) — среднее арифметическое ролей"""
        roles = [
            CentralMidfielder.mezzala_support(player_data),
            CentralMidfielder.mezzala_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Каррилеро ===
    @staticmethod
    def carrilero_support(player_data: dict) -> float:
        """Каррилеро (По)"""
        technical_weights = {
            'Отб': 1.0, 'Пас': 1.0, 'ПКас': 1.0,
            'Тех': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Ком': 1.0, 'ПРш': 1.0,
            'Вид': 0.75, 'Ибм': 0.75, 'Инт': 0.75,
            'Кнц': 0.75, 'Раб': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0,
        }
        return CentralMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def carrilero_overall(player_data: dict) -> float:
        """Каррилеро (ОВР) — у роли только одна обязанность (По)"""
        return CentralMidfielder.carrilero_support(player_data)

    @staticmethod
    def overall(player_data: dict) -> float:
        """Универсальность ЦП — среднее всех 8 ролей"""
        roles = [
            CentralMidfielder.central_midfielder_overall(player_data),
            CentralMidfielder.deep_lying_playmaker_overall(player_data),
            CentralMidfielder.box_to_box_midfielder_overall(player_data),
            CentralMidfielder.advanced_playmaker_overall(player_data),
            CentralMidfielder.ball_winning_midfielder_overall(player_data),
            CentralMidfielder.roamer_overall(player_data),
            CentralMidfielder.mezzala_overall(player_data),
            CentralMidfielder.carrilero_overall(player_data),
        ]
        active_roles = [r for r in roles if r > 0]
        if not active_roles:
            return 0.0
        return round(sum(active_roles) / len(active_roles), 2)


class WideMidfielder:
    """Класс для расчёта ролей крайнего полузащитника."""

    @staticmethod
    def _calculate_role(player_data: dict,
                        technical_weights: dict,
                        mental_weights: dict,
                        physical_weights: dict) -> float:
        """Универсальный метод расчёта роли."""
        weighted_sum = sum(player_data.get(attr, 0) * weight
                           for attr, weight in {**technical_weights, **mental_weights, **physical_weights}.items())
        max_possible = sum(20 * weight
                           for weight in {**technical_weights, **mental_weights, **physical_weights}.values())
        return round((weighted_sum / max_possible) * 100, 2) if max_possible > 0 else 0.0

    # === Фланговый полузащитник ===
    @staticmethod
    def winger_defend(player_data: dict) -> float:
        """Фланговый полузащитник (Зщ)"""
        technical_weights = {
            'Отб': 1.0, 'Пас': 1.0,
            'Нав': 0.75, 'Опк': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Ком': 1.0, 'Кнц': 1.0, 'ПРш': 1.0, 'Раб': 1.0,
            'Инт': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 0.75,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def winger_support(player_data: dict) -> float:
        """Фланговый полузащитник (По)"""
        technical_weights = {
            'Отб': 1.0, 'Пас': 1.0,
            'Нав': 0.75, 'ПКас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Ком': 1.0, 'ПРш': 1.0, 'Раб': 1.0,
            'Вид': 0.75, 'Поз': 0.75, 'Ибм': 0.75,
            'Инт': 0.75, 'Кнц': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def winger_attack(player_data: dict) -> float:
        """Фланговый полузащитник (Ат)"""
        technical_weights = {
            'Нав': 1.0, 'Пас': 1.0, 'ПКас': 1.0,
            'Отб': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Ком': 1.0, 'ПРш': 1.0, 'Раб': 1.0,
            'Вид': 0.75, 'Ибм': 0.75, 'Инт': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def winger_overall(player_data: dict) -> float:
        """Фланговый полузащитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            WideMidfielder.winger_defend(player_data),
            WideMidfielder.winger_support(player_data),
            WideMidfielder.winger_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Крайний полузащитник ===
    @staticmethod
    def wide_midfielder_support(player_data: dict) -> float:
        """Крайний полузащитник (По)"""
        technical_weights = {
            'Дрб': 1.0, 'Нав': 1.0, 'Тех': 1.0,
            'Пас': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0,
            'Раб': 0.75,
        }
        physical_weights = {
            'Скр': 1.0, 'Уск': 1.0,
            'ВЫН': 0.75, 'Лвк': 0.75,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def wide_midfielder_attack(player_data: dict) -> float:
        """Крайний полузащитник (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Нав': 1.0, 'Тех': 1.0,
            'Пас': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0,
            'Имп': 0.75, 'Инт': 0.75,
        }
        physical_weights = {
            'Скр': 1.0, 'Уск': 1.0,
            'Лвк': 0.75,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def wide_midfielder_overall(player_data: dict) -> float:
        """Крайний полузащитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            WideMidfielder.wide_midfielder_support(player_data),
            WideMidfielder.wide_midfielder_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Крайний полузащитник оборон. плана ===
    @staticmethod
    def defensive_winger_defend(player_data: dict) -> float:
        """Крайний полузащитник оборон. плана (Зщ)"""
        technical_weights = {
            'Тех': 1.0,
            'Дрб': 0.75, 'Нав': 0.75, 'Опк': 0.75, 'Отб': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Поз': 1.0, 'Ибм': 1.0, 'Инт': 1.0, 'Ком': 1.0, 'Раб': 1.0,
            'Агр': 0.75, 'Кнц': 0.75, 'ПРш': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0,
            'Уск': 0.75,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def defensive_winger_support(player_data: dict) -> float:
        """Крайний полузащитник оборон. плана (По)"""
        technical_weights = {
            'Нав': 1.0, 'Тех': 1.0,
            'Дрб': 0.75, 'Опк': 0.75, 'Отб': 0.75, 'Пас': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Ком': 1.0, 'Раб': 1.0,
            'Агр': 0.75, 'Поз': 0.75, 'Инт': 0.75, 'Кнц': 0.75, 'ПРш': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'ВЫН': 1.0,
            'Уск': 0.75,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def defensive_winger_overall(player_data: dict) -> float:
        """Крайний полузащитник оборон. плана (ОВР) — среднее арифметическое ролей"""
        roles = [
            WideMidfielder.defensive_winger_defend(player_data),
            WideMidfielder.defensive_winger_support(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Фланговый плеймейкер ===
    @staticmethod
    def wide_playmaker_support(player_data: dict) -> float:
        """Фланговый плеймейкер (По)"""
        technical_weights = {
            'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Дрб': 0.75,
        }
        mental_weights = {
            'Вид': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Ибм': 0.75,
        }
        physical_weights = {
            'Лвк': 0.75,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def wide_playmaker_attack(player_data: dict) -> float:
        """Фланговый плеймейкер (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
        }
        mental_weights = {
            'Вид': 1.0, 'Ибм': 1.0, 'Ком': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Имп': 0.75, 'Инт': 0.75,
        }
        physical_weights = {
            'Лвк': 0.75, 'Уск': 0.75,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def wide_playmaker_overall(player_data: dict) -> float:
        """Фланговый плеймейкер (ОВР) — среднее арифметическое ролей"""
        roles = [
            WideMidfielder.wide_playmaker_support(player_data),
            WideMidfielder.wide_playmaker_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Полуфланговый крайний полузащитник ===
    @staticmethod
    def inverted_winger_support(player_data: dict) -> float:
        """Полуфланговый крайний полузащитник (По)"""
        technical_weights = {
            'Дрб': 1.0, 'Пас': 1.0, 'Тех': 1.0,
            'Длн': 0.75, 'Нав': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0,
            'Вид': 0.75, 'ПРш': 0.75, 'Раб': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'Уск': 1.0,
            'ВЫН': 0.75, 'Лвк': 0.75, 'Скр': 0.75,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def inverted_winger_attack(player_data: dict) -> float:
        """Полуфланговый крайний полузащитник (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Пас': 1.0, 'Тех': 1.0,
            'Длн': 0.75, 'Нав': 0.75, 'ПКас': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0,
            'Вид': 0.75, 'Имп': 0.75, 'Инт': 0.75, 'ПРш': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'Лвк': 1.0, 'Уск': 1.0,
            'Скр': 0.75,
        }
        return WideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def inverted_winger_overall(player_data: dict) -> float:
        """Полуфланговый крайний полузащитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            WideMidfielder.inverted_winger_support(player_data),
            WideMidfielder.inverted_winger_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    @staticmethod
    def overall(player_data: dict) -> float:
        """Универсальность КП — среднее всех 5 ролей"""
        roles = [
            WideMidfielder.winger_overall(player_data),
            WideMidfielder.wide_midfielder_overall(player_data),
            WideMidfielder.defensive_winger_overall(player_data),
            WideMidfielder.wide_playmaker_overall(player_data),
            WideMidfielder.inverted_winger_overall(player_data),
        ]
        active_roles = [r for r in roles if r > 0]
        if not active_roles:
            return 0.0
        return round(sum(active_roles) / len(active_roles), 2)


class AttackingMidfielder:
    """Класс для расчёта ролей атакующего полузащитника."""

    @staticmethod
    def _calculate_role(player_data: dict,
                        technical_weights: dict,
                        mental_weights: dict,
                        physical_weights: dict) -> float:
        """Универсальный метод расчёта роли."""
        weighted_sum = sum(player_data.get(attr, 0) * weight
                           for attr, weight in {**technical_weights, **mental_weights, **physical_weights}.items())
        max_possible = sum(20 * weight
                           for weight in {**technical_weights, **mental_weights, **physical_weights}.values())
        return round((weighted_sum / max_possible) * 100, 2) if max_possible > 0 else 0.0

    @staticmethod
    def advanced_playmaker_overall(player_data: dict) -> float:
        """Выдвинутый плеймейкер — используем реализацию из CentralMidfielder"""
        return CentralMidfielder.advanced_playmaker_overall(player_data)

    # === Атакующий полузащитник ===
    @staticmethod
    def attacking_midfielder_support(player_data: dict) -> float:
        """Атакующий полузащитник (По)"""
        technical_weights = {
            'Длн': 1.0, 'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Дрб': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Имп': 1.0, 'Инт': 1.0, 'ПРш': 1.0,
            'Вид': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'Лвк': 0.75,
        }
        return AttackingMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def attacking_midfielder_attack(player_data: dict) -> float:
        """Атакующий полузащитник (Ат)"""
        technical_weights = {
            'Длн': 1.0, 'Дрб': 1.0, 'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Зав': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Имп': 1.0, 'Инт': 1.0, 'ПРш': 1.0,
            'Вид': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'Лвк': 0.75,
        }
        return AttackingMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def attacking_midfielder_overall(player_data: dict) -> float:
        """Атакующий полузащитник (ОВР) — среднее арифметическое ролей"""
        roles = [
            AttackingMidfielder.attacking_midfielder_support(player_data),
            AttackingMidfielder.attacking_midfielder_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    # === Треквартиста ===
    @staticmethod
    def trequartista_attack(player_data: dict) -> float:
        """Треквартиста (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Зав': 0.75,
        }
        mental_weights = {
            'Вид': 1.0, 'Ибм': 1.0, 'Имп': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Инт': 0.75,
        }
        physical_weights = {
            'Уск': 1.0,
            'КРД': 0.75, 'Лвк': 0.75,
        }
        return AttackingMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def trequartista_overall(player_data: dict) -> float:
        """Треквартиста (ОВР) — у роли только одна обязанность (Ат)"""
        return AttackingMidfielder.trequartista_attack(player_data)

    # === Энганче ===
    @staticmethod
    def enganche_support(player_data: dict) -> float:
        """Энганче (По)"""
        technical_weights = {
            'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Дрб': 0.75,
        }
        mental_weights = {
            'Вид': 1.0, 'ПРш': 1.0, 'Смб': 1.0,
            'Ибм': 0.75, 'Имп': 0.75, 'Инт': 0.75, 'Ком': 0.75,
        }
        physical_weights = {
            'Лвк': 0.75,
        }
        return AttackingMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def enganche_overall(player_data: dict) -> float:
        """Энганче (ОВР) — у роли только одна обязанность (По)"""
        return AttackingMidfielder.enganche_support(player_data)

    # === Теневой нападающий ===
    @staticmethod
    def shadow_striker_attack(player_data: dict) -> float:
        """Теневой нападающий (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Зав': 1.0, 'ПКас': 1.0,
            'Пас': 0.75, 'Тех': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0, 'Инт': 1.0, 'Смб': 1.0,
            'Кнц': 0.75, 'ПРш': 0.75, 'Раб': 0.75,
        }
        physical_weights = {
            'Уск': 1.0,
            'ВЫН': 0.75, 'КРД': 0.75, 'Лвк': 0.75, 'Скр': 0.75,
        }
        return AttackingMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def shadow_striker_overall(player_data: dict) -> float:
        """Теневой нападающий (ОВР) — у роли только одна обязанность (Ат)"""
        return AttackingMidfielder.shadow_striker_attack(player_data)

    @staticmethod
    def overall(player_data: dict) -> float:
        """Универсальность АП — среднее всех 5 ролей"""
        roles = [
            AttackingMidfielder.attacking_midfielder_overall(player_data),
            AttackingMidfielder.advanced_playmaker_overall(player_data),
            AttackingMidfielder.trequartista_overall(player_data),
            AttackingMidfielder.enganche_overall(player_data),
            AttackingMidfielder.shadow_striker_overall(player_data),
        ]
        active_roles = [r for r in roles if r > 0]
        if not active_roles:
            return 0.0
        return round(sum(active_roles) / len(active_roles), 2)


class AttackingWideMidfielder:
    """Класс для расчёта ролей атакующего крайнего полузащитника."""

    @staticmethod
    def _calculate_role(player_data: dict,
                        technical_weights: dict,
                        mental_weights: dict,
                        physical_weights: dict) -> float:
        """Универсальный метод расчёта роли."""
        weighted_sum = sum(player_data.get(attr, 0) * weight
                           for attr, weight in {**technical_weights, **mental_weights, **physical_weights}.items())
        max_possible = sum(20 * weight
                           for weight in {**technical_weights, **mental_weights, **physical_weights}.values())
        return round((weighted_sum / max_possible) * 100, 2) if max_possible > 0 else 0.0

    @staticmethod
    def wide_midfielder_overall(player_data: dict) -> float:
        """Крайний полузащитник — делегируем к WideMidfielder"""
        return WideMidfielder.wide_midfielder_overall(player_data)

    @staticmethod
    def advanced_playmaker_overall(player_data: dict) -> float:
        """Выдвинутый плеймейкер — делегируем к CentralMidfielder"""
        return CentralMidfielder.advanced_playmaker_overall(player_data)

    @staticmethod
    def trequartista_overall(player_data: dict) -> float:
        """Треквартиста — делегируем к AttackingMidfielder"""
        return AttackingMidfielder.trequartista_overall(player_data)

    @staticmethod
    def inverted_winger_overall(player_data: dict) -> float:
        """Полуфланговый крайний полузащитник — делегируем к WideMidfielder"""
        return WideMidfielder.inverted_winger_overall(player_data)

    # === Инсайд ===
    @staticmethod
    def inside_forward_support(player_data: dict) -> float:
        """Инсайд (По)"""
        technical_weights = {
            'Дрб': 1.0, 'Пас': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Длн': 0.75, 'Зав': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0,
            'Вид': 0.75, 'Имп': 0.75, 'Инт': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'КРД': 1.0, 'Лвк': 1.0, 'Уск': 1.0,
            'Скр': 0.75,
        }
        return AttackingWideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def inside_forward_attack(player_data: dict) -> float:
        """Инсайд (Ат)"""
        technical_weights = {
            'Дрб': 1.0, 'Зав': 1.0, 'ПКас': 1.0, 'Тех': 1.0,
            'Длн': 0.75, 'Пас': 0.75,
        }
        mental_weights = {
            'Ибм': 1.0,
            'Имп': 0.75, 'Инт': 0.75, 'Смб': 0.75,
        }
        physical_weights = {
            'КРД': 1.0, 'Лвк': 1.0, 'Уск': 1.0,
            'Скр': 0.75,
        }
        return AttackingWideMidfielder._calculate_role(
            player_data, technical_weights, mental_weights, physical_weights
        )

    @staticmethod
    def inside_forward_overall(player_data: dict) -> float:
        """Инсайд (ОВР) — среднее арифметическое ролей"""
        roles = [
            AttackingWideMidfielder.inside_forward_support(player_data),
            AttackingWideMidfielder.inside_forward_attack(player_data),
        ]
        return round(sum(roles) / len(roles), 2)

    @staticmethod
    def target_man_winger_overall(player_data: dict) -> float:
        """Фланговый таргетмен (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def Raumdeuter_overall(player_data: dict) -> float:
        """Раумдойтер (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def overall(player_data: dict) -> float:
        """Универсальность АКП — среднее всех 7 ролей"""
        roles = [
            AttackingWideMidfielder.wide_midfielder_overall(player_data),
            AttackingWideMidfielder.advanced_playmaker_overall(player_data),
            AttackingWideMidfielder.inside_forward_overall(player_data),
            AttackingWideMidfielder.trequartista_overall(player_data),
            AttackingWideMidfielder.target_man_winger_overall(player_data),
            AttackingWideMidfielder.Raumdeuter_overall(player_data),
            AttackingWideMidfielder.inverted_winger_overall(player_data),
        ]
        active_roles = [r for r in roles if r > 0]
        if not active_roles:
            return 0.0
        return round(sum(active_roles) / len(active_roles), 2)
