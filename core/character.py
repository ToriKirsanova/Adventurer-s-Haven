from enum import Enum
from typing import Dict, List, Optional
import random


class CharacterClass(Enum):
    WARRIOR = "Воин"
    MAGE = "Маг"
    RANGER = "Рейнджер"


class AdventurerState(Enum):
    IDLE = "бездействие"
    MOVING = "движение"
    IN_DUNGEON = "в подземелье"
    IN_FOREST = "в лесу"
    IN_TAVERN = "в таверне"
    IN_LAKE = "на озере"
    IN_FARM = "на ферме"
    FISHING = "рыбалка"
    GATHER = "собирательство"
    SHOPPING = "покупки"
    RESTING = "отдых"


class Location(Enum):
    TOWN = "город"
    DUNGEON = "подземелье"
    FOREST = "лес"
    LAKE = "озеро"
    FARM = "ферма"
    TAVERN = "таверна"
    BLACKSMITH = "кузница"
    ALCHEMY_SHOP = "магазин зелий"
    TAILOR = "портняжная мастерская"
    LEATHERWORKING = "мастерская кожевника"


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
        actual_damage = max(1, damage - self.defense * 0.3)
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
        self.state = AdventurerState.IDLE
        self.current_location = Location.TOWN
        self.target_location = None
        self.current_action = None

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
        base_path = "C:\\Git\\Adventurer-s-Haven\\Images\\"
        if self.character_class == CharacterClass.WARRIOR:
            return base_path + "Warrior_1lvl.png"
        elif self.character_class == CharacterClass.MAGE:
            return base_path + "Mage_1lvl.png"
        elif self.character_class == CharacterClass.RANGER:
            return base_path + "Ranger_1lvl.png"
        return base_path + "Adventurer_1lvl.png"

    def update(self, game_world) -> None:
        """Основной метод обновления ИИ авантюриста"""
        if not self.is_alive:
            return

        # Обновляем состояние потребностей
        self._update_needs()

        # Выбираем действие на основе приоритетов
        self._choose_action(game_world)

        # Выполняем текущее действие
        self._execute_action()

    def _update_needs(self) -> None:
        """Обновляет состояние потребностей авантюриста"""
        # Проверяем здоровье (первый уровень потребностей)
        health_ratio = self.health / self.max_health
        self.needs_healing = health_ratio < 0.5

        # Проверяем необходимость в снаряжении
        self.needs_equipment = self.gold > 100 and random.random() > 0.7

    def _choose_action(self, game_world) -> None:
        """Выбирает следующее действие на основе приоритетов"""

        # УРОВЕНЬ 1: Базовые потребности (здоровье)
        if self.needs_healing:
            if self.inventory.get("health_potion", 0) > 0:
                self._use_health_potion()
                return
            else:
                self._set_goal(Location.TAVERN, "лечение")
                return

        # УРОВЕНЬ 2: Основные стремления
        if self.needs_equipment and game_world.has_better_equipment(self):
            shop_location = self._choose_equipment_shop()
            self._set_goal(shop_location, "покупка снаряжения")
            return

        # Проверяем заказы в таверне
        if game_world.has_tavern_orders() and random.random() > 0.5:
            resource_type = game_world.get_tavern_order()
            if resource_type == "fish":
                self._set_goal(Location.LAKE, "рыбалка для таверны")
                return
            elif resource_type == "herbs":
                self._set_goal(Location.FOREST, "сбор трав для таверны")
                return

        # Проверяем заказы на ферме
        if game_world.has_farm_orders() and random.random() > 0.5:
            self._set_goal(Location.FOREST, "поиск семян для фермы")
            return

        # По умолчанию - идти за опытом и добычей
        self._choose_adventure_location()

    def _choose_equipment_shop(self) -> Location:
        """Выбирает магазин для покупки снаряжения"""
        if self.character_class == CharacterClass.WARRIOR:
            return random.choice([Location.BLACKSMITH, Location.LEATHERWORKING])
        elif self.character_class == CharacterClass.MAGE:
            return random.choice([Location.ALCHEMY_SHOP, Location.TAILOR])
        else:  # RANGER
            return random.choice([Location.BLACKSMITH, Location.LEATHERWORKING, Location.TAILOR])

    def _choose_adventure_location(self) -> None:
        """Выбирает локацию для приключений"""
        locations = [Location.DUNGEON, Location.FOREST]
        weights = [0.6, 0.4]  # Больше шансов пойти в подземелье

        target = random.choices(locations, weights=weights)[0]
        self._set_goal(target, "поиск приключений")

    def _set_goal(self, location: Location, reason: str) -> None:
        """Устанавливает новую цель для авантюриста"""
        if self.target_location != location:
            self.target_location = location
            self.current_goal = reason
            self.state = AdventurerState.MOVING
            print(f"{self.name} направляется в {location.value} для {reason}")

    def _execute_action(self) -> None:
        """Выполняет текущее действие"""
        if self.state == AdventurerState.MOVING:
            self._move_to_target()
        elif self.state == AdventurerState.IDLE:
            self._wander_around()
        elif self.state in [AdventurerState.IN_DUNGEON, AdventurerState.IN_FOREST,
                            AdventurerState.IN_LAKE, AdventurerState.IN_FARM]:
            self._perform_location_action()

    def _move_to_target(self) -> None:
        """Движение к целевой локации"""
        if self.current_location == Location.TOWN:
            if self.direction == 1:
                self.x += self.speed
                if self.x > 800:
                    self.direction = -1
            else:
                self.x -= self.speed
                if self.x < 100:
                    self.direction = 1

            # Имитация достижения цели
            if random.random() < 0.01:
                self._arrive_at_target()

    def _wander_around(self) -> None:
        """Блуждание без конкретной цели"""
        if random.random() < 0.02:
            self.direction *= -1

        self.x += self.speed * self.direction

        if self.x < 100:
            self.x = 100
            self.direction = 1
        elif self.x > 800:
            self.x = 800
            self.direction = -1

    def _arrive_at_target(self) -> None:
        """Достижение целевой локации"""
        if self.target_location:
            self.current_location = self.target_location

            # Устанавливаем соответствующее состояние
            if self.target_location == Location.DUNGEON:
                self.state = AdventurerState.IN_DUNGEON
            elif self.target_location == Location.FOREST:
                self.state = AdventurerState.IN_FOREST
            elif self.target_location == Location.LAKE:
                self.state = AdventurerState.IN_LAKE
            elif self.target_location == Location.FARM:
                self.state = AdventurerState.IN_FARM
            elif self.target_location == Location.TAVERN:
                self.state = AdventurerState.IN_TAVERN
            else:
                self.state = AdventurerState.SHOPPING

            print(f"{self.name} прибыл в {self.target_location.value}")
            self.target_location = None

    def _perform_location_action(self) -> None:
        """Выполняет действие в текущей локации"""
        if self.state == AdventurerState.IN_TAVERN:
            self._heal_in_tavern()
        elif self.state == AdventurerState.IN_DUNGEON:
            self._explore_dungeon()
        elif self.state == AdventurerState.IN_FOREST:
            self._explore_forest()
        elif self.state == AdventurerState.IN_LAKE:
            self._fish_in_lake()
        elif self.state == AdventurerState.SHOPPING:
            self._buy_equipment()

        # После выполнения действия возвращаемся в город
        if random.random() < 0.05:  # 5% шанс закончить действие
            self._return_to_town()

    def _use_health_potion(self) -> None:
        """Использование зелья здоровья"""
        if self.inventory.get("health_potion", 0) > 0:
            heal_amount = self.max_health * 0.5
            self.health = min(self.max_health, self.health + heal_amount)
            self.inventory["health_potion"] -= 1
            self.needs_healing = False
            print(f"{self.name} использовал зелье здоровья")

    def _heal_in_tavern(self) -> None:
        """Лечение в таверне"""
        heal_amount = self.max_health * 0.3
        self.health = min(self.max_health, self.health + heal_amount)
        cost = 10
        self.gold -= cost
        print(f"{self.name} поел в таверне и восстановил {heal_amount} здоровья (-{cost} золота)")
        self.needs_healing = self.health < self.max_health * 0.8

    def _explore_dungeon(self) -> None:
        """Исследование подземелья"""
        exp_gained = random.randint(10, 25)
        gold_gained = random.randint(5, 15)
        damage_taken = random.randint(5, 20)

        self.experience += exp_gained
        self.gold += gold_gained
        self.health -= damage_taken

        # Шанс найти зелье
        if random.random() > 0.8:
            self.inventory["health_potion"] += 1
            print(f"{self.name} нашел зелье здоровья в подземелье!")

        print(
            f"{self.name} исследовал подземелье: +{exp_gained} опыта, +{gold_gained} золота, -{damage_taken} здоровья")
        self._check_level_up()

    def _explore_forest(self) -> None:
        """Исследование леса"""
        resources_gained = random.randint(1, 3)
        gold_gained = random.randint(3, 10)

        self.gold += gold_gained
        self.inventory["herbs"] += resources_gained
        self.inventory["wood"] += random.randint(1, 2)

        # Шанс найти семена
        if random.random() > 0.7:
            self.inventory["seeds"] += 1
            print(f"{self.name} нашел редкие семена в лесу!")

        print(f"{self.name} исследовал лес: +{resources_gained} трав, +{gold_gained} золота")

    def _fish_in_lake(self) -> None:
        """Рыбалка на озере"""
        fish_caught = random.randint(1, 4)
        self.inventory["fish"] += fish_caught

        # Шанс поймать редкую рыбу
        if random.random() > 0.9:
            rare_fish = random.randint(1, 2)
            self.inventory["fish"] += rare_fish
            print(f"{self.name} поймал редкую рыбу!")

        print(f"{self.name} порыбачил на озере: +{fish_caught} рыбы")

    def _buy_equipment(self) -> None:
        """Покупка снаряжения"""
        if self.gold >= 50:
            self.gold -= 50
            equipment_type = "weapon" if random.random() > 0.5 else "armor"
            old_equipment = self.equipment[equipment_type]
            self.equipment[equipment_type] = f"улучшенный {equipment_type}"
            self.needs_equipment = False
            print(
                f"{self.name} купил {equipment_type} за 50 золота ({old_equipment} -> {self.equipment[equipment_type]})")

    def _return_to_town(self) -> None:
        """Возвращение в город"""
        self.current_location = Location.TOWN
        self.state = AdventurerState.IDLE
        print(f"{self.name} вернулся в город")

    def _check_level_up(self) -> None:
        """Проверка повышения уровня"""
        while self.experience >= self.experience_to_next_level:
            self.experience -= self.experience_to_next_level
            self.level_up()

    def level_up(self) -> None:
        """Повышение уровня"""
        self.level += 1
        self.max_health *= 1.2
        self.attack_power *= 1.15
        self.defense *= 1.1
        self.health = self.max_health
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)

        print(f"🎉 {self.name} достиг {self.level} уровня!")


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