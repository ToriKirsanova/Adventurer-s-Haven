import pygame.draw
from pygame import Rect, Surface, font, draw
from configs.config import *


class Button(Rect):
    """
    Класс кнопки с поддержкой относительных размеров
    """

    def __init__(self, left: float, top: float, width: float, height: float,
                 enabled: bool = True, relative: bool = True):
        """
        Конструктор

        :param left: левая граница (в пикселях или долях)
        :param top: верхняя граница (в пикселях или долях)
        :param width: ширина (в пикселях или долях)
        :param height: высота (в пикселях или долях)
        :param enabled: обрабатываются ли клики
        :param relative: если True, то координаты и размеры считаются в долях от экрана
        """
        self.__relative = relative
        self.__relative_left = left
        self.__relative_top = top
        self.__relative_width = width
        self.__relative_height = height

        if relative:
            abs_left = int(left * scaling_system.current_width)
            abs_top = int(top * scaling_system.current_height)
            abs_width = int(width * scaling_system.current_width)
            abs_height = int(height * scaling_system.current_height)
        else:
            abs_left = left
            abs_top = top
            abs_width = width
            abs_height = height

        super().__init__(abs_left, abs_top, abs_width, abs_height)
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
        """Обновляет размеры и позицию при изменении масштаба"""
        if self.__relative:
            abs_left = int(self.__relative_left * scaling_system.current_width)
            abs_top = int(self.__relative_top * scaling_system.current_height)
            abs_width = int(self.__relative_width * scaling_system.current_width)
            abs_height = int(self.__relative_height * scaling_system.current_height)

            self.x = abs_left
            self.y = abs_top
            self.width = abs_width
            self.height = abs_height

        self.__font_size = scaling_system.scale(20)
        self.__font = font.SysFont('Arial', self.__font_size)

        if self.__image is not None:
            self.__image = pygame.transform.scale(self.__image, (self.width, self.height))

    def draw(self, surface: Surface):
        """
        Метод для отрисовки кнопки

        :param surface: полотно для отрисовки
        """
        if self.color:
            draw.rect(surface, self.color, self)
        if self.image:
            surface.blit(self.image, self)
        if self.text:
            text_surface = self.font.render(self.text, True, self.color_text)
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
    def font_size(self):
        return self.__font_size

    @font_size.setter
    def font_size(self, size: int):
        self.__font_size = scaling_system.scale(size)
        self.__font = font.SysFont('Arial', self.__font_size)

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

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        self.__action = action