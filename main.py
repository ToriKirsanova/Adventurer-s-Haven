import pygame
import ctypes
from ctypes import wintypes
import sys

from configs.config import FPS
from core.baseimage import BaseImage
from core.clickableimage import ClickableImage
from core.window import Window


def get_taskbar_size_windows():
    """Получить размер панели задач в Windows"""
    # Получаем handle панели задач
    taskbar_hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)

    # Получаем прямоугольник панели задач
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(taskbar_hwnd, ctypes.byref(rect))
    # Определяем положение панели задач
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    if rect.top != 0:  # снизу
        return screen_height - rect.top


# Инициализация Pygame
pygame.init()

# Получаем размеры экрана
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Устанавливаем размер окна на 1/3 экрана по высоте
window_width = screen_width
window_height = screen_height // 3

# Создаем окно без рамок
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
pygame.display.set_caption("Color Changer")

hwnd = pygame.display.get_wm_info()["window"]
ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, screen_height - window_height - get_taskbar_size_windows(), 0, 0, 0x0001)

# Размеры кнопок
button_width = 100
button_height = 50
button_margin = 10
DARK_GRAY = pygame.color.THECOLORS.get("darkgray")
GRAY = pygame.color.THECOLORS.get("gray")
BLACK = pygame.color.THECOLORS.get("black")
# Позиции кнопок (справа)
button_x = window_width - button_width - 20
button_start_y = 20

# Создаем список кнопок
buttons = []
for i in range(5):
    button_rect = pygame.Rect(
        button_x,
        button_start_y + i * (button_height + button_margin),
        button_width,
        button_height
    )
    buttons.append(button_rect)

font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()  # Clock для ограничения FPS

town = BaseImage("Images/Town.png", 0, 0)
tavern = ClickableImage("Images/tavern.png", 803, 0)
town.scale(window_width, window_height)

town_win = Window()
town_win.append_image(town)
town_win.append_image(tavern)
windows = list()
windows.append(town_win)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Выход по ESC
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяем клик по кнопкам
            mouse_pos = pygame.mouse.get_pos()
            clicked_image = None
            for win in windows:
                clicked_image = win.handle_click(mouse_pos)
                if clicked_image:
                    clicked_image

    for win in windows:
        win.draw(screen)

    # Рисуем кнопки
    for i, button in enumerate(buttons):
        # Проверяем, наведена ли мышь на кнопку
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, DARK_GRAY, button)
        else:
            pygame.draw.rect(screen, GRAY, button)

        # Рисуем рамку кнопки
        pygame.draw.rect(screen, BLACK, button, 2)

        # Текст кнопки
        color_text = f"Color {i + 1}"
        text_surface = font.render(color_text, True, BLACK)
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)

    # Обновляем экран
    pygame.display.flip()

# Выход из Pygame
pygame.quit()
sys.exit()
