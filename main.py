import time
from pathlib import Path

import pygame
import ctypes
from ctypes import wintypes
import sys
import os

from configs.config import *

# Импортируем классы персонажей
from core.character import Adventurer, CharacterClass, GameWorld
from ui.button import Button


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


def create_class_buttons():
    """Создает и возвращает список кнопок для выбора класса"""
    buttons = []
    class_button_width = 200
    class_button_height = 50

    for i, (class_name, class_type, color) in enumerate(class_types):
        button = Button(
            window_width // 2 - class_button_width // 2,
            window_height // 2 - 50 + i * (class_button_height + 20),
            class_button_width,
            class_button_height
        )
        button.text = class_name
        button.color = color
        button.color_text = WHITE
        # Устанавливаем действие с параметрами
        button.set_action(create_adventurer, class_type, class_name)
        buttons.append(button)

    return buttons


def load_adventurer_images():
    """Загружает изображения авантюристов"""
    images = {}
    try:
        # Проверяем существование файлов и загружаем их
        warrior_path = str(Path(os.path.dirname(__file__)) / "Images" / "Warrior_1lvl.png")
        if os.path.exists(warrior_path):
            warrior_img = pygame.image.load(warrior_path)
            images[CharacterClass.WARRIOR] = pygame.transform.scale(warrior_img, (50, 80))
        else:
            print(f"Файл не найден: {warrior_path}")
            # Создаем заглушку
            surf = pygame.Surface((50, 80))
            surf.fill(RED)
            images[CharacterClass.WARRIOR] = surf

        # Заглушки для других классов (будут заменены реальными изображениями)
        mage_surf = pygame.Surface((50, 80))
        mage_surf.fill(BLUE)
        images[CharacterClass.MAGE] = mage_surf

        ranger_surf = pygame.Surface((50, 80))
        ranger_surf.fill(GREEN)
        images[CharacterClass.RANGER] = ranger_surf

    except Exception as e:
        print(f"Ошибка загрузки изображений: {e}")
        # Создаем базовые заглушки
        surf = pygame.Surface((50, 80))
        surf.fill(GRAY)
        images[CharacterClass.WARRIOR] = surf
        images[CharacterClass.MAGE] = surf
        images[CharacterClass.RANGER] = surf

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
    class_buttons = []  # Очищаем кнопки
    print(f"Создан новый авантюрист: {adventurer_name} ({class_name})")


# Инициализация
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
    button = Button(
        button_x,
        button_start_y + i * (button_height + button_margin),
        button_width,
        button_height
    )
    button.text = f"Color {i + 1}"
    button.color = WHITE
    buttons.append(button)

# Кнопка создания авантюриста
create_adventurer_button = Button(
    button_x,
    button_start_y + 5 * (button_height + button_margin),
    button_width,
    button_height
)
create_adventurer_button.text = "Создать авантюриста"
create_adventurer_button.color = BLUE
create_adventurer_button.set_action(set_creating_adventurer, True)
buttons.append(create_adventurer_button)

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

# Переменные для хранения кнопок классов
class_buttons = []  # Содержит объекты Button

clock = pygame.time.Clock()

# Загружаем изображения авантюристов
adventurer_images = load_adventurer_images()

# Игровой мир
game_world = GameWorld()

# Основной игровой цикл
town = pygame.image.load("Images/Town.png")
town = pygame.transform.scale(town, (window_width, window_height))
running = True

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

            # Проверяем клик по основным кнопкам
            for button in buttons:
                if button.collidepoint(mouse_pos) and button.enabled:
                    button.execute_action()

            # Кнопки выбора класса (только когда меню открыто)
            if creating_adventurer:
                for button in class_buttons:
                    if button.collidepoint(mouse_pos) and button.enabled:
                        button.execute_action()
                        break  # Выходим из цикла после создания

    # Обновление авантюристов
    for adventurer in adventurers:
        adventurer.update(game_world, time.time())

    # Отрисовка фона
    screen.blit(town, town.get_rect())

    # Рисуем основные кнопки
    for button in buttons:
        button.draw(screen)

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

        # Кнопки классов (используем объекты Button)
        for button in class_buttons:
            button.draw(screen)

            # Описание класса (дополнительная информация)
            desc_y = button.bottom + 5
            if button.action_args and len(button.action_args) > 0:
                class_type = button.action_args[0]
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

    # Отрисовка авантюристов
    for adventurer in adventurers:
        if adventurer.is_alive:
            # Получаем изображение для класса авантюриста
            image = adventurer_images.get(adventurer.character_class)
            if image:
                # Отображаем авантюриста
                screen.blit(image, (adventurer.x, adventurer.y))

                # Отображаем имя и здоровье над авантюристом
                name_text = small_font.render(adventurer.name, True, BLACK)
                screen.blit(name_text, (adventurer.x - 10, adventurer.y - 20))

                # Полоска здоровья
                health_width = 50
                health_ratio = adventurer.health / adventurer.max_health
                current_health_width = int(health_width * health_ratio)

                health_bg = pygame.Rect(adventurer.x, adventurer.y - 10, health_width, 5)
                health_bar = pygame.Rect(adventurer.x, adventurer.y - 10, current_health_width, 5)

                pygame.draw.rect(screen, RED, health_bg)
                pygame.draw.rect(screen, GREEN, health_bar)

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
