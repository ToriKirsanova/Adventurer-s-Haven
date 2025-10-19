import pygame.draw
from pygame import Rect, Surface, font, draw
from configs.config import *


class Button(Rect):
    """
    Простой класс кнопки для отображения текста/изображений
    """

    def __init__(self, left: float, top: float, width: float, height: float, enabled: bool = True, relative: bool = True):
        """
        Конструктор

        :param left: левая граница
        :param top: верхняя граница
        :param width: ширина
        :param height: высота
        :param enabled: обрабатываются ли клики
        :param relative: если True, то координаты и размеры считаются в долях от экрана
        """
        if relative:
            left = int(left * scaling_system.current_width)
            top = int(top * scaling_system.current_height)
            width = int(width * scaling_system.current_width)
            height = int(height * scaling_system.current_height)

        super().__init__(left, top, width, height)
        self.__text = ""
        self.__color_text = BLACK
        self.__font_size = scaling_system.scale(20)
        self.__font = font.SysFont('Arial', self.__font_size)
        self.__image = None
        self.__color = None
        self.__enabled = enabled
        self.__action = None
        self.__action_args = ()
        self.__action_kwargs = {}
        self.__relative = relative

    @property
    def action_args(self):
        return self.__action_args

    def set_action(self, action, *args, **kwargs):
        """Установка действия с аргументами"""
        self.__action = action
        self.__action_args = args
        self.__action_kwargs = kwargs

    def execute_action(self):
        """Выполнение действия с аргументами"""
        if self.__action and self.__enabled:
            self.__action(*self.__action_args, **self.__action_kwargs)

    def update_scale(self):
        if self.__relative:
            self.x = int(self.x * scaling_system.scale_x)
            self.y = int(self.y * scaling_system.scale_y)
            self.width = int(self.width * scaling_system.scale_x)
            self.height = int(self.height * scaling_system.scale_y)

        self.__font_size = scaling_system.scale(20)
        self.__font = font.SysFont('Arial', self.__font_size)
        if self.image is not None:
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, surface: Surface):
        """
        Метод для отрисовки изображения

        :param surface: полотно для отрисовки
        """
        if self.color:
            draw.rect(surface, self.color, self)
        if self.image:
            surface.blit(self.image, self)
        if self.text:
            text_surface = self.font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.center)
            surface.blit(text_surface, text_rect)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, new_text: str):
        self.__text = new_text

    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, new_font: font):
        self.__font = new_font

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, new_image):
        self.__image = new_image

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, new_color):
        self.__color = new_color

    @property
    def color_text(self):
        return self.__color_text

    @color_text.setter
    def color_text(self, new_color_text):
        self.__color_text = new_color_text

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, is_enabled: bool):
        self.__enabled = is_enabled


