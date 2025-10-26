import time
from pathlib import Path

import pygame
import ctypes
from ctypes import wintypes
import sys
import os

from configs.config import *
from core.baseimage import BaseImage
from core.character import Adventurer, CharacterClass, GameWorld
from core.clickableimage import ClickableImage
from core.window import Window
from ui.button import Button


def get_taskbar_size_windows():
    """Получить размер панели задач в Windows"""
    taskbar_hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(taskbar_hwnd, ctypes.byref(rect))
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    if rect.top != 0:  # снизу
        return screen_height - rect.top


def draw_adventurer_info(screen, adventurer, rel_x, rel_y):
    """Отображает информацию об авантюристе с относительными координатами"""
    abs_x = int(rel_x * scaling_system.current_width)
    abs_y = int(rel_y * scaling_system.current_height)
    info_width = 0.1  # 10% ширины экрана
    info_height = 0.2  # 20% высоты экрана
    abs_width = int(info_width * scaling_system.current_width)
    abs_height = int(info_height * scaling_system.current_height)

    info_rect = pygame.Rect(abs_x, abs_y, abs_width, abs_height)
    pygame.draw.rect(screen, LIGHT_BLUE, info_rect)
    pygame.draw.rect(screen, WHITE, info_rect, scaling_system.scale(2))

    padding = scaling_system.scale(10)
    small_font_size = scaling_system.scale(16)
    small_font = pygame.font.SysFont('Arial', small_font_size)

    name_text = f"{adventurer.name} - {adventurer.character_class.value}"
    name_surface = small_font.render(name_text, True, BLACK)
    screen.blit(name_surface, (abs_x + padding, abs_y + padding))

    level_text = f"Ур. {adventurer.level}"
    level_surface = small_font.render(level_text, True, BLACK)
    screen.blit(level_surface, (abs_x + padding, abs_y + padding * 3))

    health_text = f"HP: {adventurer.health:.0f}/{adventurer.max_health:.0f}"
    health_surface = small_font.render(health_text, True, BLACK)
    screen.blit(health_surface, (abs_x + padding, abs_y + padding * 5))

    gold_text = f"Золото: {adventurer.gold}"
    gold_surface = small_font.render(gold_text, True, BLACK)
    gold_x = abs_x + int(0.05 * scaling_system.current_width)  # 5% от ширины экрана
    screen.blit(gold_surface, (gold_x, abs_y + padding * 3))


def create_class_buttons():
    """Создает кнопки для выбора класса с относительными размерами"""
    buttons = []

    # Относительные размеры кнопок
    class_button_width = 0.15  # 15% ширины
    class_button_height = 0.07  # 7% высоты
    button_spacing = 0.03  # 3% высоты между кнопками

    for i, (class_name, class_type, color) in enumerate(class_types):
        button = Button(
            0.5 - class_button_width / 2,  # Центр по X
            0.4 + i * (class_button_height + button_spacing),  # Вертикальное расположение
            class_button_width,
            class_button_height
        )
        button.text = class_name
        button.color = color
        button.color_text = WHITE
        button.font_size = 20
        button.set_action(create_adventurer, class_type, class_name)
        buttons.append(button)

    return buttons


def load_adventurer_images():
    """Загружает и масштабирует изображения авантюристов"""
    images = {}
    try:
        # Относительный размер персонажей
        base_width = 0.03  # 3% ширины экрана
        base_height = 0.08  # 8% высоты экрана

        abs_width = scaling_system.scale_absolute(base_width, True)
        abs_height = scaling_system.scale_absolute(base_height, False)
        base_size = (abs_width, abs_height)

        warrior_path = str(Path(os.path.dirname(__file__)) / "Images" / "Warrior_1lvl.png")
        if os.path.exists(warrior_path):
            warrior_img = pygame.image.load(warrior_path)
            images[CharacterClass.WARRIOR] = pygame.transform.scale(warrior_img, base_size)
        else:
            surf = pygame.Surface(base_size)
            surf.fill(RED)
            images[CharacterClass.WARRIOR] = surf

        # Заглушки для других классов
        for class_type, color in [(CharacterClass.MAGE, BLUE), (CharacterClass.RANGER, GREEN)]:
            surf = pygame.Surface(base_size)
            surf.fill(color)
            images[class_type] = surf

    except Exception as e:
        print(f"Ошибка загрузки изображений: {e}")
        base_size = (scaling_system.scale(50), scaling_system.scale(80))
        surf = pygame.Surface(base_size)
        surf.fill(GRAY)
        for class_type in CharacterClass:
            images[class_type] = surf

    return images


def set_creating_adventurer(value):
    global creating_adventurer, class_buttons
    creating_adventurer = value
    if value:
        class_buttons = create_class_buttons()
        print("Открыто меню выбора класса")


def create_adventurer(class_type, class_name):
    global adventurer_counter, creating_adventurer, class_buttons
    adventurer_name = f"Авантюрист {adventurer_counter}"
    new_adventurer = Adventurer(adventurer_name, class_type)
    adventurers.append(new_adventurer)
    adventurer_counter += 1
    creating_adventurer = False
    class_buttons = []
    print(f"Создан новый авантюрист: {adventurer_name} ({class_name})")


def update_ui_scale():
    """Обновляет масштаб всех UI элементов"""
    global buttons, class_buttons, adventurer_images, town, font, small_font, title_font

    # Обновляем системные шрифты
    font = pygame.font.SysFont('Arial', scaling_system.scale(20))
    small_font = pygame.font.SysFont('Arial', scaling_system.scale(16))
    title_font = pygame.font.SysFont('Arial', scaling_system.scale(24), bold=True)

    # Обновляем кнопки
    for button in buttons:
        button.update_scale()

    for button in class_buttons:
        button.update_scale()

    # Перезагружаем изображения с новым масштабом
    adventurer_images = load_adventurer_images()


def init_windows():
    """Инициализация всех окон на старте игры"""
    global current_window, cur_win_num, list_window
    # Загружаем и масштабируем фон
    town = BaseImage("Images/Town.png", 0, 0, (window_width, window_height))
    tavern = ClickableImage("Images/tavern.png",
                           scaling_system.scale_absolute(0.417),
                           scaling_system.scale_absolute(0.03, False))
    town_window = Window([town, tavern])

    test_img = ClickableImage("Images/Town1.png", 0, 0, (window_width, window_height))
    test_window = Window([test_img])
    # todo: пример для демонстрации работы смены окон, заменить на другое позже

    list_window = [town_window, test_window]
    cur_win_num = 0
    current_window = list_window[cur_win_num]


# Инициализация
pygame.init()

# Получаем размеры экрана
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Устанавливаем размер окна на 1/3 экрана по высоте
window_width = screen_width
window_height = screen_height // 3

# Инициализируем систему масштабирования
scaling_system.update(window_width, window_height)

# Создаем окно
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
pygame.display.set_caption("Adventure Town Manager")

# Позиционируем окно
hwnd = pygame.display.get_wm_info()["window"]
taskbar_height = get_taskbar_size_windows() or 40
ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, screen_height - window_height - taskbar_height, 0, 0, 0x0001)

# ОТНОСИТЕЛЬНЫЕ РАЗМЕРЫ ДЛЯ ВСЕГО UI
button_width = 0.12  # 12% ширины
button_height = 0.06  # 6% высоты
button_margin = 0.015  # 1.5% высоты
button_start_x = 0.85  # 85% ширины (правая часть)
button_start_y = 0.05  # 5% высоты (отступ сверху)

# Создаем список основных кнопок (справа)
buttons = []
button_texts = ["Город", "Гильдия", "Магазин", "Таверна", "Настройки"]

for i, text in enumerate(button_texts):
    button = Button(
        button_start_x,
        button_start_y + i * (button_height + button_margin),
        button_width,
        button_height
    )
    button.text = text
    button.color = WHITE
    button.color_text = BLACK
    button.set_action(lambda num: num, i)
    buttons.append(button)

# Кнопка создания авантюриста
create_adventurer_button = Button(
    button_start_x,
    button_start_y + len(button_texts) * (button_height + button_margin),
    button_width,
    button_height
)
create_adventurer_button.text = "Создать авантюриста"
create_adventurer_button.color = BLUE
create_adventurer_button.color_text = WHITE
create_adventurer_button.set_action(set_creating_adventurer, True)
buttons.append(create_adventurer_button)

# Инициализация шрифтов
font = pygame.font.SysFont('Arial', scaling_system.scale(20))
small_font = pygame.font.SysFont('Arial', scaling_system.scale(16))
title_font = pygame.font.SysFont('Arial', scaling_system.scale(24), bold=True)

# Состояния игры
creating_adventurer = False
adventurers = []
adventurer_counter = 1

# Классы авантюристов
class_types = [
    ("Воин", CharacterClass.WARRIOR, RED),
    ("Маг", CharacterClass.MAGE, BLUE),
    ("Рейнджер", CharacterClass.RANGER, GREEN)
]

class_buttons = []

clock = pygame.time.Clock()

# Загружаем изображения
adventurer_images = load_adventurer_images()

# Игровой мир
game_world = GameWorld()
init_windows()
running = True

curr_click_button = None

while running:
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            for button in buttons:
                if button.collidepoint(mouse_pos) and button.enabled:
                    button.set_highlight()
                    win_num = button.execute_action()
                    if win_num is not None and win_num != cur_win_num and len(list_window) > win_num:
                        cur_win_num = win_num
                        current_window = list_window[cur_win_num]
                    curr_click_button = button
                    break

            if creating_adventurer:
                for button in class_buttons:
                    if button.collidepoint(mouse_pos) and button.enabled:
                        button.execute_action()
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if curr_click_button is not None:
                curr_click_button.unset_highlight()
                curr_click_button = None

    for adventurer in adventurers:
        adventurer.update(game_world, time.time())

    current_window.draw(screen)

    for button in buttons:
        button.draw(screen)

    if creating_adventurer:
        # Затемнение фона
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        class_window_width = 0.3  # 30% ширины
        class_window_height = 0.4  # 40% высоты

        abs_width = scaling_system.scale_absolute(class_window_width, True)
        abs_height = scaling_system.scale_absolute(class_window_height, False)

        class_window = pygame.Rect(
            window_width // 2 - abs_width // 2,
            window_height // 2 - abs_height // 2,
            abs_width,
            abs_height
        )
        pygame.draw.rect(screen, WHITE, class_window)
        pygame.draw.rect(screen, BLACK, class_window, scaling_system.scale(3))

        # Заголовок
        title_text = title_font.render("Выберите класс авантюриста", True, BLACK)
        title_rect = title_text.get_rect(center=(window_width // 2,
                                                 scaling_system.scale_absolute(0.35, False)))
        screen.blit(title_text, title_rect)

        # Кнопки классов
        for button in class_buttons:
            button.draw(screen)

    for i, adventurer in enumerate(adventurers):
        row = i // 4  # 4 авантюриста в строке
        col = i % 4
        rel_x = 0.02 + col * 0.25  # 2% отступ + 25% на каждого
        rel_y = 0.02 + row * 0.15  # 2% отступ + 15% на строку
        draw_adventurer_info(screen, adventurer, rel_x, rel_y)

    for adventurer in adventurers:
        if adventurer.is_alive:
            image = adventurer_images.get(adventurer.character_class)
            if image:
                screen.blit(image, (adventurer.x, adventurer.y))

    stats_bg_width = 0.07  # 7% ширины
    stats_bg_height = 0.08  # 8% высоты
    stats_bg = pygame.Rect(
        scaling_system.scale_absolute(0.02, True),
        scaling_system.scale_absolute(0.02, False),
        scaling_system.scale_absolute(stats_bg_width, True),
        scaling_system.scale_absolute(stats_bg_height, False)
    )
    pygame.draw.rect(screen, WHITE, stats_bg)
    pygame.draw.rect(screen, WHITE, stats_bg, scaling_system.scale(1))

    total_adventurers = len(adventurers)
    stats_text = f"Авантюристы: {total_adventurers}"
    stats_surface = small_font.render(stats_text, True, BLACK)
    screen.blit(stats_surface, (scaling_system.scale_absolute(0.03),
                                scaling_system.scale_absolute(0.03, False)))

    # Подсказка
    if total_adventurers == 0 and not creating_adventurer:
        hint_text = "Нажмите 'Создать авантюриста' чтобы начать!"
        hint_surface = font.render(hint_text, True, YELLOW)
        hint_rect = hint_surface.get_rect(center=(window_width // 2,
                                                  scaling_system.scale_absolute(0.95, False)))
        screen.blit(hint_surface, hint_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
