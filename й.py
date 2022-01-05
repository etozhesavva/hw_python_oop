from dataclasses import dataclass, fields
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(
            self.training_type, self.duration,
            self.distance, self.speed,
            self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER: ClassVar[float] = 18
    SPEED_SHIFT: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        return (
            ((self.SPEED_MULTIPLIER * self.get_mean_speed())
             - self.SPEED_SHIFT) * self.weight / self.M_IN_KM
             * self.duration * self.MIN_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WIGHT_MULTIPLIER_1: ClassVar[float] = 0.035
    WIGHT_MULTIPLIER_2: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self) -> float:
        return (
                ((self.WIGHT_MULTIPLIER_1 * self.weight)
                 + ((self.get_mean_speed() ** 2 // self.height)
                 * self.WIGHT_MULTIPLIER_2 * self.weight))
                 * self.duration * self.MIN_IN_HOUR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    SPEED_MULTIPLIER: ClassVar[float] = 1.1
    SPEED_SHIFT: ClassVar[float] = 2
    LEN_STEP: ClassVar[float] = 1.38
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Средняя скорость."""
        return (
                self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Спаленные калории"""
        return (
                (self.get_mean_speed() + self.SPEED_MULTIPLIER)
                * self.SPEED_SHIFT * self.weight
        )


TRAINING_TYPES = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
TRAINING_ERROR = 'Нет такой тренировки {}'
PARAMETER_ERROR = 'Для тренировки {} ожадалось {} показателей, а не {}'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAINING_TYPES:
        raise ValueError(TRAINING_ERROR.format(workout_type))
    training_type = TRAINING_TYPES[workout_type]
    if len(data) != len(fields(training_type)):
        raise ValueError(PARAMETER_ERROR.format(workout_type,
                                                len(fields(training_type)), len(data)))
    return training_type(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
