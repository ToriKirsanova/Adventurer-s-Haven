import pygame

from core.clickableimage import BaseImage, ClickableImage


class Window:
    """
    Класс, содержащий в себе набор изображений для управления и взаимодействия с ними
    """
    def __init__(self, image_list: list["BaseImage"] = None):
        self.image_list = list()
        if image_list is not None:
            self.image_list = image_list

    def append_image(self, img: "BaseImage"):
        """
        Добавление новго изображения в окно

        :param img: новое изображение
        """
        self.image_list.append(img)

    def draw(self, surface: pygame.Surface):
        """
        Метод для отрисовки изображения

        :param surface: полотно для отрисовки
        """
        for image in self.image_list:
            image.draw(surface)

    def handle_click(self, pos):
        """
        Обрабатывает клик по всем изображениям в окне
        """
        for image in self.image_list:
            if isinstance(image, ClickableImage) and image.check_click(pos):
                return image
        return None
