import pygame
import ctypes
from ctypes import wintypes
import sys

from configs.config import FPS


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

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Цвета для кнопок и окон
COLORS = [
    (255, 0, 0),  # Красный
    (0, 255, 0),  # Зеленый
    (0, 0, 255),  # Синий
    (255, 255, 0),  # Желтый
    (255, 0, 255)  # Пурпурный
]

# Текущий цвет окна
current_color = WHITE

# Размеры кнопок
button_width = 100
button_height = 50
button_margin = 10

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

# Шрифт для текста кнопок
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()  # Clock для ограничения FPS
# Основной цикл игры
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
            for i, button in enumerate(buttons):
                if button.collidepoint(mouse_pos):
                    current_color = COLORS[i]

    # Заливаем экран текущим цветом
    screen.fill(current_color)

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
