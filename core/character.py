from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional


class CharacterClass(Enum):
    """Классы авантюристов"""
    WARRIOR = "Воин"
    MAGE = "Маг"
    RANGER = "Рейнджер"


class EnemyType(Enum):
    """Типы врагов"""
    GOBLIN = "Гоблин"
    ORC = "Орк"
    SPIDER = "Паук"
    SKELETON = "Скелет"


class Character(ABC):
    """
    Родительский класс для всех персонажей в игре.
    Содержит общие свойства и методы для Adventurer и Enemy.
    """

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
        self.inventory = {}

    @abstractmethod
    def take_damage(self, damage: float) -> None:
        """Получение урона - абстрактный метод"""
        pass

    @abstractmethod
    def attack(self, target: 'Character') -> None:
        """Атака цели - абстрактный метод"""
        pass

    def heal(self, amount: float) -> None:
        """Лечение персонажа"""
        if self.is_alive:
            self.health = min(self.max_health, self.health + amount)
            print(f"{self.name} восстановил {amount} здоровья. Теперь у него {self.health} HP")

    def level_up(self) -> None:
        """Повышение уровня"""
        self.level += 1
        self.max_health *= 1.2
        self.attack_power *= 1.15
        self.defense *= 1.1
        self.health = self.max_health  # Полное лечение при повышении уровня
        print(f"{self.name} достиг {self.level} уровня!")

    def get_status(self) -> str:
        """Получение статуса персонажа"""
        return (f"{self.name} | Ур. {self.level} | "
                f"HP: {self.health:.1f}/{self.max_health:.1f} | "
                f"АТК: {self.attack_power:.1f} | ЗАЩ: {self.defense:.1f}")

    def _check_health(self) -> None:
        """Проверка здоровья и обновление статуса жив/мертв"""
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"☠️ {self.name} пал в бою!")


class Adventurer(Character):
    """
    Класс авантюриста - игровой персонаж, который исследует мир
    """

    def __init__(self, name: str, character_class: CharacterClass, level: int = 1,
                 health: float = 100, attack_power: float = 10, defense: float = 5):

        # Базовые модификаторы в зависимости от класса
        class_modifiers = {
            CharacterClass.WARRIOR: {"health": 1.3, "attack": 1.2, "defense": 1.4},
            CharacterClass.MAGE: {"health": 0.8, "attack": 1.5, "defense": 0.7},
            CharacterClass.RANGER: {"health": 1.0, "attack": 1.2, "defense": 1.0}
        }

        mod = class_modifiers[character_class]

        super().__init__(
            name=name,
            level=level,
            health=health * mod["health"],
            max_health=health * mod["health"],
            attack_power=attack_power * mod["attack"],
            defense=defense * mod["defense"]
        )

        self.character_class = character_class
        self.experience = 0
        self.experience_to_next_level = 100
        self.gold = 50
        self.skills = {}

        # Профессии авантюриста
        self.professions = {
            "mining": 0,
            "herbalism": 0,
            "skinning": 0,
            "fishing": 0,
            "cooking": 0
        }

    def take_damage(self, damage: float) -> None:
        """Авантюрист получает урон с учетом защиты"""
        actual_damage = max(1, damage - self.defense * 0.5)
        self.health -= actual_damage
        print(f"⚔️ {self.name} получает {actual_damage:.1f} урона! Осталось {self.health:.1f} HP")
        self._check_health()

    def attack(self, target: Character) -> None:
        """Авантюрист атакует врага"""
        if not self.is_alive:
            print(f"{self.name} не может атаковать, так как он мертв!")
            return

        if not target.is_alive:
            print(f"{target.name} уже мертв!")
            return

        damage = self.attack_power
        print(f"🗡️ {self.name} атакует {target.name} и наносит {damage:.1f} урона!")
        target.take_damage(damage)

    def gain_experience(self, exp: int) -> None:
        """Получение опыта и проверка повышения уровня"""
        if not self.is_alive:
            return

        self.experience += exp
        print(f"✨ {self.name} получает {exp} опыта!")

        while self.experience >= self.experience_to_next_level:
            self.experience -= self.experience_to_next_level
            self.level_up()
            self.experience_to_next_level = int(self.experience_to_next_level * 1.5)

    def collect_loot(self, loot: Dict[str, int]) -> None:
        """Сбор лута с монстров"""
        for item, quantity in loot.items():
            self.inventory[item] = self.inventory.get(item, 0) + quantity
        print(f"🎒 {self.name} собрал лут: {loot}")

    def improve_profession(self, profession: str, amount: int = 1) -> None:
        """Улучшение навыка профессии"""
        if profession in self.professions:
            self.professions[profession] += amount
            print(f"🔧 {self.name} улучшил {profession} до {self.professions[profession]}")


class Enemy(Character):
    """
    Класс врага - противник авантюристов
    """

    def __init__(self, name: str, enemy_type: EnemyType, level: int = 1,
                 health: float = 50, attack_power: float = 8, defense: float = 3):

        super().__init__(
            name=name,
            level=level,
            health=health,
            max_health=health,
            attack_power=attack_power,
            defense=defense
        )

        self.enemy_type = enemy_type
        self.experience_reward = level * 10
        self.gold_reward = level * 5

        # Лут, который выпадает с врага
        self.loot_table = self._generate_loot_table()

    def _generate_loot_table(self) -> Dict[str, int]:
        """Генерация таблицы лута в зависимости от типа врага"""
        base_loot = {
            "gold": self.gold_reward,
            "experience": self.experience_reward
        }

        # Специфический лут для разных типов врагов
        specific_loot = {
            EnemyType.GOBLIN: {"goblin_ear": 1, "crude_weapon": 1},
            EnemyType.SPIDER: {"spider_silk": 2, "spider_venom": 1},
            EnemyType.SKELETON: {"ancient_bone": 3, "rusty_sword": 1},
        }

        base_loot.update(specific_loot.get(self.enemy_type, {}))
        return base_loot

    def take_damage(self, damage: float) -> None:
        """Враг получает урон"""
        actual_damage = max(1, damage - self.defense * 0.3)
        self.health -= actual_damage
        print(f"💥 {self.name} получает {actual_damage:.1f} урона! Осталось {self.health:.1f} HP")
        self._check_health()

    def attack(self, target: Character) -> None:
        """Враг атакует авантюриста"""
        if not self.is_alive:
            return

        if not target.is_alive:
            return

        damage = self.attack_power
        print(f"👹 {self.name} атакует {target.name} и наносит {damage:.1f} урона!")
        target.take_damage(damage)

    def get_loot(self) -> Dict[str, int]:
        """Получение лута после смерти врага"""
        if self.is_alive:
            return {}
        return self.loot_table


# # Пример использования классов
# if __name__ == "__main__":
#     # Создаем авантюриста
#     warrior = Adventurer("Боромир", CharacterClass.WARRIOR)
#     mage = Adventurer("Гэндальф", CharacterClass.MAGE)
#
#     # Создаем врагов
#     goblin = Enemy("Грязноклык", EnemyType.GOBLIN, level=2)
#     spider = Enemy("Паук-охотник", EnemyType.SPIDER, level=3)
#
#     print("=== НАЧАЛО БОЯ ===")
#     print(warrior.get_status())
#     print(goblin.get_status())
#     print()
#
#     # Бой
#     warrior.attack(goblin)
#     goblin.attack(warrior)
#     warrior.attack(goblin)  # Добиваем гоблина
#
#     if not goblin.is_alive:
#         loot = goblin.get_loot()
#         warrior.collect_loot(loot)
#         warrior.gain_experience(goblin.experience_reward)
#
#     print("\n=== ПОСЛЕ БОЯ ===")
#     print(warrior.get_status())
#     print(f"Золото: {warrior.gold}")
#     print(f"Инвентарь: {warrior.inventory}")
