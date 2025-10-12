import pygame
from pathlib import Path


class BaseImage:
    """
    Базовый класс для отрисовки
    """

    def __init__(self, image_path: str, x: float, y: float):
        if Path(image_path).exists():
            self.image = pygame.image.load(image_path).convert_alpha()
            self.rect = self.image.get_rect(topleft=(x, y))
            self.mask = pygame.mask.from_surface(self.image)
        else:
            print(f"Попытка загрузить несуществующую картинку {image_path}")

    def scale(self, width, height):
        """

        :param width:
        :param height:
        :return:
        """
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

    def draw(self, surface: pygame.Surface):
        """
        Метод для отрисовки изображения

        :param surface: полотно для отрисовки
        """
        surface.blit(self.image, self.rect)
