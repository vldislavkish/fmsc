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

    @staticmethod
    def ball_winning_midfielder_overall(player_data: dict) -> float:
        """Полузащитник-разрушитель (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def anchor_man_overall(player_data: dict) -> float:
        """Чистый опорный полузащитник (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def half_back_overall(player_data: dict) -> float:
        """Хавбек (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def regista_overall(player_data: dict) -> float:
        """Реджиста (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def roamer_overall(player_data: dict) -> float:
        """Блуждающий плеймейкер (ОВР) — заглушка"""
        return 0.0

    @staticmethod
    def segundo_volante_overall(player_data: dict) -> float:
        """Сегундо-воланте (ОВР) — заглушка"""
        return 0.0

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
