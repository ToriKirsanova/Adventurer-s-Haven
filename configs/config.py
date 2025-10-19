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
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.scale_factor = SCALE

    def update(self, current_width, current_height):
        self.current_width = current_width
        self.current_height = current_height
        self.scale_x = current_width / self.reference_width
        self.scale_y = current_height / self.reference_height
        self.scale_factor = min(self.scale_x, self.scale_y)  # Сохраняем пропорции

    def scale_x(self, value):
        return int(value * self.scale_x)

    def scale_y(self, value):
        return int(value * self.scale_y)

    def scale(self, value):
        return int(value * self.scale_factor)

    def scale_rect(self, x, y, width, height):
        return (
            int(x * self.scale_x),
            int(y * self.scale_y),
            int(width * self.scale_x),
            int(height * self.scale_y)
        )


scaling_system = ScalingSystem()
