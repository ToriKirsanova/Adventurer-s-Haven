import pygame
import ctypes
from ctypes import wintypes
import sys

from configs.config import FPS

# Импортируем классы персонажей
from core.character import Adventurer, CharacterClass


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
pygame.display.set_caption("Adventure Town Manager")

hwnd = pygame.display.get_wm_info()["window"]
ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, screen_height - window_height - get_taskbar_size_windows(), 0, 0, 0x0001)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)

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
button_width = 120
button_height = 40
button_margin = 10

# Позиции кнопок (справа)
button_x = window_width - button_width - 20
button_start_y = 20

# Создаем список основных кнопок
buttons = []
for i in range(5):
    button_rect = pygame.Rect(
        button_x,
        button_start_y + i * (button_height + button_margin),
        button_width,
        button_height
    )
    buttons.append(button_rect)

# Кнопка создания авантюриста
create_adventurer_button = pygame.Rect(
    button_x,
    button_start_y + 5 * (button_height + button_margin),
    button_width,
    button_height
)

# Шрифты
font = pygame.font.SysFont('Arial', 20)
small_font = pygame.font.SysFont('Arial', 16)
title_font = pygame.font.SysFont('Arial', 24, bold=True)

# Состояния игры
creating_adventurer = False
adventurers = []  # Список созданных авантюристов
adventurer_counter = 1  # Счетчик для имен

# Классы авантюристов
class_types = [
    ("Воин", CharacterClass.WARRIOR, RED),
    ("Маг", CharacterClass.MAGE, BLUE),
    ("Рейнджер", CharacterClass.RANGER, GREEN)
]

clock = pygame.time.Clock()


def draw_button(screen, rect, text, color=GRAY, text_color=BLACK, border_color=BLACK):
    """Рисует кнопку с текстом"""
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, DARK_GRAY, rect)
    else:
        pygame.draw.rect(screen, color, rect)

    pygame.draw.rect(screen, border_color, rect, 2)

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_adventurer_info(screen, adventurer, x, y):
    """Отображает информацию об авантюристе"""
    # Фон информации
    info_rect = pygame.Rect(x, y, 250, 80)
    pygame.draw.rect(screen, LIGHT_BLUE, info_rect)
    pygame.draw.rect(screen, BLACK, info_rect, 2)

    # Имя и класс
    name_text = f"{adventurer.name} - {adventurer.character_class.value}"
    name_surface = small_font.render(name_text, True, BLACK)
    screen.blit(name_surface, (x + 10, y + 10))

    # Уровень
    level_text = f"Ур. {adventurer.level}"
    level_surface = small_font.render(level_text, True, BLACK)
    screen.blit(level_surface, (x + 10, y + 30))

    # Здоровье
    health_text = f"HP: {adventurer.health:.0f}/{adventurer.max_health:.0f}"
    health_surface = small_font.render(health_text, True, BLACK)
    screen.blit(health_surface, (x + 10, y + 50))

    # Золото
    gold_text = f"Золото: {adventurer.gold}"
    gold_surface = small_font.render(gold_text, True, BLACK)
    screen.blit(gold_surface, (x + 120, y + 30))


# Основной цикл игры
town = pygame.image.load("Images/Town.png")
town = pygame.transform.scale(town, (window_width, window_height))
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
            mouse_pos = pygame.mouse.get_pos()

            # Проверяем клик по основным кнопкам
            for i, button in enumerate(buttons):
                if button.collidepoint(mouse_pos):
                    current_color = COLORS[i]

            # Кнопка создания авантюриста
            if create_adventurer_button.collidepoint(mouse_pos):
                creating_adventurer = True
                print("Открыто меню выбора класса")

            # Кнопки выбора класса (только когда меню открыто)
            if creating_adventurer:
                # Создаем кнопки классов в центре экрана
                class_button_width = 200
                class_button_height = 50
                class_window_center_x = window_width // 2
                class_window_center_y = window_height // 2

                for i, (class_name, class_type, color) in enumerate(class_types):
                    button_rect = pygame.Rect(
                        class_window_center_x - class_button_width // 2,
                        class_window_center_y - 80 + i * (class_button_height + 15),
                        class_button_width,
                        class_button_height
                    )

                    if button_rect.collidepoint(mouse_pos):
                        # Создаем авантюриста
                        adventurer_name = f"Авантюрист {adventurer_counter}"
                        new_adventurer = Adventurer(adventurer_name, class_type)
                        adventurers.append(new_adventurer)
                        adventurer_counter += 1
                        creating_adventurer = False
                        print(f"Создан новый авантюрист: {adventurer_name} ({class_name})")

    # Отрисовка фона
    screen.blit(town, town.get_rect())

    # Рисуем основные кнопки
    for i, button in enumerate(buttons):
        draw_button(screen, button, f"Color {i + 1}")

    # Кнопка создания авантюриста
    draw_button(screen, create_adventurer_button, "Создать авантюриста", GREEN, WHITE)

    # Окно выбора класса (если активно создание)
    if creating_adventurer:
        # Затемнение фона
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # Окно выбора класса
        class_window_width = 400
        class_window_height = 300
        class_window = pygame.Rect(
            window_width // 2 - class_window_width // 2,
            window_height // 2 - class_window_height // 2,
            class_window_width,
            class_window_height
        )
        pygame.draw.rect(screen, WHITE, class_window)
        pygame.draw.rect(screen, BLACK, class_window, 3)

        # Заголовок
        title_text = title_font.render("Выберите класс авантюриста", True, BLACK)
        title_rect = title_text.get_rect(center=(window_width // 2, window_height // 2 - 100))
        screen.blit(title_text, title_rect)

        # Кнопки классов
        class_button_width = 200
        class_button_height = 50

        for i, (class_name, class_type, color) in enumerate(class_types):
            button_rect = pygame.Rect(
                window_width // 2 - class_button_width // 2,
                window_height // 2 - 50 + i * (class_button_height + 20),
                class_button_width,
                class_button_height
            )

            # Рисуем кнопку класса
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, DARK_GRAY, button_rect)
            else:
                pygame.draw.rect(screen, color, button_rect)

            pygame.draw.rect(screen, BLACK, button_rect, 2)

            # Текст кнопки
            text_surface = font.render(class_name, True, WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

            # Описание класса (дополнительная информация)
            desc_y = button_rect.bottom + 5
            if class_type == CharacterClass.WARRIOR:
                desc_text = "Сильный боец ближнего боя"
            elif class_type == CharacterClass.MAGE:
                desc_text = "Мощный заклинатель"
            else:  # RANGER
                desc_text = "Меткий стрелок и следопыт"

            desc_surface = small_font.render(desc_text, True, BLACK)
            desc_rect = desc_surface.get_rect(center=(window_width // 2, desc_y))
            screen.blit(desc_surface, desc_rect)

    # Отображаем созданных авантюристов
    for i, adventurer in enumerate(adventurers):
        row = i // 4  # 4 авантюриста в строке
        col = i % 4
        x = 20 + col * 270
        y = 20 + row * 100
        draw_adventurer_info(screen, adventurer, x, y)

    # Статистика в левом верхнем углу
    stats_bg = pygame.Rect(10, 10, 200, 60)
    pygame.draw.rect(screen, (255, 255, 255, 180), stats_bg)
    pygame.draw.rect(screen, BLACK, stats_bg, 1)

    total_adventurers = len(adventurers)
    stats_text = f"Всего авантюристов: {total_adventurers}"
    stats_surface = small_font.render(stats_text, True, BLACK)
    screen.blit(stats_surface, (20, 20))

    # Подсказка
    if total_adventurers == 0 and not creating_adventurer:
        hint_text = "Нажмите 'Создать авантюриста' чтобы начать!"
        hint_surface = font.render(hint_text, True, YELLOW)
        hint_rect = hint_surface.get_rect(center=(window_width // 2, window_height - 30))
        screen.blit(hint_surface, hint_rect)

    # Обновляем экран
    pygame.display.flip()

# Выход из Pygame
pygame.quit()
sys.exit()