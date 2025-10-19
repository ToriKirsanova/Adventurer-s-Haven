FPS = 60
SCALE = 1.0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)

COLORS = [
    (255, 0, 0),  # Красный
    (0, 255, 0),  # Зеленый
    (0, 0, 255),  # Синий
    (255, 255, 0),  # Желтый
    (255, 0, 255)  # Пурпурный
]


class ScalingSystem:
    def __init__(self, reference_width=1920, reference_height=1080):
        self.reference_width = reference_width
        self.reference_height = reference_height
        self.current_width = reference_width
        self.current_height = reference_height
        self.scale_factor = SCALE

    def update(self, current_width, current_height):
        """Обновляет масштабные коэффициенты"""
        self.current_width = current_width
        self.current_height = current_height
        self.scale_factor = min(
            current_width / self.reference_width,
            current_height / self.reference_height
        )

    def scale(self, value):
        """Масштабирует значение пропорционально"""
        return int(value * self.scale_factor)

    def scale_absolute(self, relative_value, is_width=True):
        """Конвертирует относительное значение в абсолютное"""
        if is_width:
            return int(relative_value * self.current_width)
        return int(relative_value * self.current_height)


# Глобальный объект масштабирования
scaling_system = ScalingSystem()
