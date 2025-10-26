import os
from pathlib import Path
import random

from core import CharacterClass, AdventurerState, Location
from core.ai.adventurerai import AdventurerAI


class Character:
    """Базовый класс для всех персонажей"""

    def __init__(self, name: str, level: int = 1, health: float = 100,
                 max_health: float = 100, attack_power: float = 10,
                 defense: float = 5):
        self.name = name
        self.level = level
        self.health = health
        self.max_health = max_health
        self.attack_power = attack_power
        self.defense = defense
        self.is_alive = True

    def take_damage(self, damage: float) -> None:
        actual_damage = max(1.0, damage - self.defense * 0.3)
        self.health -= actual_damage
        self._check_health()

    def attack(self, target: 'Character') -> None:
        if not self.is_alive or not target.is_alive:
            return
        damage = self.attack_power
        target.take_damage(damage)

    def _check_health(self) -> None:
        if self.health <= 0:
            self.health = 0
            self.is_alive = False


class Adventurer(Character):
    """
    Класс авантюриста с базовым ИИ и системой целей
    """

    def __init__(self, name: str, character_class: CharacterClass, level: int = 1):
        # Базовые модификаторы в зависимости от класса
        class_modifiers = {
            CharacterClass.WARRIOR: {"health": 1.3, "attack": 1.2, "defense": 1.4},
            CharacterClass.MAGE: {"health": 0.8, "attack": 1.5, "defense": 0.7},
            CharacterClass.RANGER: {"health": 0.9, "attack": 1.3, "defense": 0.9}
        }

        mod = class_modifiers[character_class]

        super().__init__(
            name=name,
            level=level,
            health=100 * mod["health"],
            max_health=100 * mod["health"],
            attack_power=10 * mod["attack"],
            defense=5 * mod["defense"]
        )

        self.character_class = character_class
        self.experience = 0
        self.experience_to_next_level = 100
        self.gold = 50

        # ИИ параметры
        self.ai = AdventurerAI()
        self.state = AdventurerState.IDLE
        self.current_location = Location.TOWN
        self.target_location = None
        self.current_goal = None
        self.needs_healing = False
        self.needs_equipment = False

        # Визуальные параметры
        self.image_path = self._get_image_path()
        self.x = random.randint(100, 700)
        self.y = 200
        self.speed = 2
        self.direction = 1

        # Инвентарь
        self.inventory = {
            "health_potion": 0,
            "fish": 0,
            "herbs": 0,
            "ore": 0,
            "wood": 0,
            "seeds": 0
        }

        # Снаряжение
        self.equipment = {
            "weapon": "начальное оружие",
            "armor": "начальные доспехи"
        }

        # Цели и приоритеты
        self.needs_healing = False
        self.needs_equipment = False
        self.current_goal = None

        print(f"Создан авантюрист: {name} ({character_class.value})")

    def _get_image_path(self) -> str:
        """Получает путь к изображению в зависимости от класса"""
        base_path = Path(os.path.abspath(os.path.dirname(__file__))) / ".." / "Images"
        if self.character_class == CharacterClass.WARRIOR:
            return str(base_path / "Warrior_1lvl.png")
        elif self.character_class == CharacterClass.MAGE:
            return str(base_path / "Mage_1lvl.png")
        elif self.character_class == CharacterClass.RANGER:
            return str(base_path / "Ranger_1lvl.png")
        return str(base_path / "Adventurer_1lvl.png")

    def update(self, game_world, current_time: float) -> None:
        """Основной метод обновления ИИ авантюриста"""
        if not self.is_alive:
            return

        self.ai.update(current_time, self, game_world)


class GameWorld:
    """Класс для управления игровым миром и заказами"""

    def __init__(self):
        self.tavern_orders = {"fish": True, "herbs": False}
        self.farm_orders = {"seeds": True}

    def has_better_equipment(self, adventurer):
        return random.random() > 0.7

    def has_tavern_orders(self):
        return any(self.tavern_orders.values())

    def get_tavern_order(self):
        available_orders = [k for k, v in self.tavern_orders.items() if v]
        return random.choice(available_orders) if available_orders else None

    def has_farm_orders(self):
        return any(self.farm_orders.values())