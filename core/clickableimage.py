import pygame
from pathlib import Path

class ClickableImage:
    """
    Класс, позволяющий сделать из изображения кнопку
    """
    def __init__(self, image_path: str, x: float, y: float):
        if Path(image_path).exists():
            self.image = pygame.image.load(image_path).convert_alpha()
            self.rect = self.image.get_rect(topleft=(x, y))
            self.mask = pygame.mask.from_surface(self.image)
        else:
            print(f"Попытка загрузить несуществующую картинку {image_path}")

    def draw(self, surface: pygame.Surface):
        """
        Метод для отрисовки изображения

        :param surface: полотно для отрисовки
        """
        surface.blit(self.image, self.rect)

    def check_click(self, pos) -> bool:
        """
        Функция возвращает ответ, попал ли клик по иконке
        Проверка идет по маске

        :param pos: позиция клика
        :return: True, если попал
        """
        local_x = pos[0] - self.rect.x
        local_y = pos[1] - self.rect.y
        try:
            mask_value = self.mask.get_at((local_x, local_y))
            if mask_value:
                return True
            return False

        except IndexError as e:
            print(f"❌ Ошибка координат маски: {e}")
        except AttributeError as e:
            print(f"❌ Попытка обратиться к непроиницилизированному изображению: {e}")
        finally:
            return False