import random

from core.ai.aibehaivor import AIBehavior
from core import AdventurerState, Location, CharacterClass


class AdventurerAI(AIBehavior):
    """ИИ для авантюристов с оптимизированными обновлениями"""

    def __init__(self, update_interval: float = 0.5):  # Обновляем 2 раза в секунду
        super().__init__(update_interval)
        self.last_need_check_time = 0
        self.need_check_interval = 2.0  # Проверка потребностей раз в 2 секунды

    def update(self, current_time: float, adventurer: 'Adventurer', world: 'GameWorld') -> None:
        if not self.should_update(current_time) or not adventurer.is_alive:
            return

        self.record_update(current_time)

        # Обновляем потребности реже, чем основные действия
        if current_time - self.last_need_check_time >= self.need_check_interval:
            self._update_needs(adventurer)
            self.last_need_check_time = current_time

        # Выбираем и выполняем действие
        self._choose_action(adventurer, world)
        self._execute_action(adventurer, world)

    def _update_needs(self, adventurer: 'Adventurer') -> None:
        """Обновляет состояние потребностей (вызывается реже)"""
        health_ratio = adventurer.health / adventurer.max_health
        adventurer.needs_healing = health_ratio < 0.5
        adventurer.needs_equipment = adventurer.gold > 100 and random.random() > 0.7

    def _choose_action(self, adventurer: 'Adventurer', world: 'GameWorld') -> None:
        """Выбирает следующее действие на основе приоритетов"""
        # УРОВЕНЬ 1: Базовые потребности (здоровье)
        if adventurer.needs_healing:
            if adventurer.inventory.get("health_potion", 0) > 0:
                self._set_immediate_action(adventurer, "use_health_potion")
                return
            else:
                self._set_goal(adventurer, Location.TAVERN, "лечение")
                return

        # УРОВЕНЬ 2: Основные стремления
        if adventurer.needs_equipment and world.has_better_equipment(adventurer):
            shop_location = self._choose_equipment_shop(adventurer)
            self._set_goal(adventurer, shop_location, "покупка снаряжения")
            return

        # Проверяем заказы в таверне
        if world.has_tavern_orders() and random.random() > 0.5:
            resource_type = world.get_tavern_order()
            if resource_type == "fish":
                self._set_goal(adventurer, Location.LAKE, "рыбалка для таверны")
                return
            elif resource_type == "herbs":
                self._set_goal(adventurer, Location.FOREST, "сбор трав для таверны")
                return

        # По умолчанию - идти за опытом и добычей
        self._choose_adventure_location(adventurer)

    def _choose_equipment_shop(self, adventurer: 'Adventurer') -> Location:
        """Выбирает магазин для покупки снаряжения"""
        if adventurer.character_class == CharacterClass.WARRIOR:
            return random.choice([Location.BLACKSMITH, Location.LEATHERWORKING])
        elif adventurer.character_class == CharacterClass.MAGE:
            return random.choice([Location.ALCHEMY_SHOP, Location.TAILOR])
        else:  # RANGER
            return random.choice([Location.BLACKSMITH, Location.LEATHERWORKING, Location.TAILOR])

    def _choose_adventure_location(self, adventurer: 'Adventurer') -> None:
        """Выбирает локацию для приключений"""
        locations = [Location.DUNGEON, Location.FOREST]
        weights = [0.6, 0.4]
        target = random.choices(locations, weights=weights)[0]
        self._set_goal(adventurer, target, "поиск приключений")

    def _set_goal(self, adventurer: 'Adventurer', location: Location, reason: str) -> None:
        """Устанавливает новую цель"""
        if adventurer.target_location != location:
            adventurer.target_location = location
            adventurer.current_goal = reason
            adventurer.state = AdventurerState.MOVING
            print(f"{adventurer.name} направляется в {location.value} для {reason}")

    def _set_immediate_action(self, adventurer: 'Adventurer', action: str) -> None:
        """Устанавливает немедленное действие"""
        adventurer.current_immediate_action = action

    def _execute_action(self, adventurer: 'Adventurer', world: 'GameWorld') -> None:
        """Выполняет текущее действие"""
        # Сначала проверяем немедленные действия
        if hasattr(adventurer, 'current_immediate_action'):
            if adventurer.current_immediate_action == "use_health_potion":
                self._use_health_potion(adventurer)
                adventurer.current_immediate_action = None
                return

        # Затем обычные действия
        if adventurer.state == AdventurerState.MOVING:
            self._move_to_target(adventurer)
        elif adventurer.state == AdventurerState.IDLE:
            self._wander_around(adventurer)
        elif adventurer.state in [AdventurerState.IN_DUNGEON, AdventurerState.IN_FOREST,
                                  AdventurerState.IN_LAKE, AdventurerState.IN_FARM]:
            self._perform_location_action(adventurer, world)

    def _use_health_potion(self, adventurer: 'Adventurer') -> None:
        """Использование зелья здоровья"""
        if adventurer.inventory.get("health_potion", 0) > 0:
            heal_amount = adventurer.max_health * 0.5
            adventurer.health = min(adventurer.max_health, adventurer.health + heal_amount)
            adventurer.inventory["health_potion"] -= 1
            adventurer.needs_healing = False
            print(f"{adventurer.name} использовал зелье здоровья")

    def _move_to_target(self, adventurer: 'Adventurer') -> None:
        """Движение к целевой локации"""
        if adventurer.current_location == Location.TOWN:
            if adventurer.direction == 1:
                adventurer.x += adventurer.speed
                if adventurer.x > 800:
                    adventurer.direction = -1
            else:
                adventurer.x -= adventurer.speed
                if adventurer.x < 100:
                    adventurer.direction = 1

            if random.random() < 0.01:
                self._arrive_at_target(adventurer)

    def _wander_around(self, adventurer: 'Adventurer') -> None:
        """Блуждание без конкретной цели"""
        if random.random() < 0.02:
            adventurer.direction *= -1

        adventurer.x += adventurer.speed * adventurer.direction

        if adventurer.x < 100:
            adventurer.x = 100
            adventurer.direction = 1
        elif adventurer.x > 800:
            adventurer.x = 800
            adventurer.direction = -1

    def _arrive_at_target(self, adventurer: 'Adventurer') -> None:
        """Достижение целевой локации"""
        if adventurer.target_location:
            adventurer.current_location = adventurer.target_location

            # Устанавливаем соответствующее состояние
            location_to_state = {
                Location.DUNGEON: AdventurerState.IN_DUNGEON,
                Location.FOREST: AdventurerState.IN_FOREST,
                Location.LAKE: AdventurerState.IN_LAKE,
                Location.FARM: AdventurerState.IN_FARM,
                Location.TAVERN: AdventurerState.IN_TAVERN
            }

            adventurer.state = location_to_state.get(
                adventurer.target_location,
                AdventurerState.SHOPPING
            )

            print(f"{adventurer.name} прибыл в {adventurer.target_location.value}")
            adventurer.target_location = None

    def _perform_location_action(self, adventurer: 'Adventurer', world: 'GameWorld') -> None:
        """Выполняет действие в текущей локации"""
        action_methods = {
            AdventurerState.IN_TAVERN: self._heal_in_tavern,
            AdventurerState.IN_DUNGEON: self._explore_dungeon,
            AdventurerState.IN_FOREST: self._explore_forest,
            AdventurerState.IN_LAKE: self._fish_in_lake,
            AdventurerState.SHOPPING: self._buy_equipment
        }

        if adventurer.state in action_methods:
            action_methods[adventurer.state](adventurer)

        # После выполнения действия возвращаемся в город
        if random.random() < 0.05:
            self._return_to_town(adventurer)

    def _heal_in_tavern(self, adventurer: 'Adventurer') -> None:
        """Лечение в таверне"""
        heal_amount = adventurer.max_health * 0.3
        adventurer.health = min(adventurer.max_health, adventurer.health + heal_amount)
        cost = 10
        adventurer.gold -= cost
        print(f"{adventurer.name} поел в таверне и восстановил {heal_amount} здоровья (-{cost} золота)")
        adventurer.needs_healing = adventurer.health < adventurer.max_health * 0.8

    def _explore_dungeon(self, adventurer: 'Adventurer') -> None:
        """Исследование подземелья"""
        exp_gained = random.randint(10, 25)
        gold_gained = random.randint(5, 15)
        damage_taken = random.randint(5, 20)

        adventurer.experience += exp_gained
        adventurer.gold += gold_gained
        adventurer.health -= damage_taken

        if random.random() > 0.8:
            adventurer.inventory["health_potion"] += 1
            print(f"{adventurer.name} нашел зелье здоровья в подземелье!")

        print(
            f"{adventurer.name} исследовал подземелье: +{exp_gained} опыта, +{gold_gained} золота, -{damage_taken} здоровья")
        self._check_level_up(adventurer)

    def _explore_forest(self, adventurer: 'Adventurer') -> None:
        """Исследование леса"""
        resources_gained = random.randint(1, 3)
        gold_gained = random.randint(3, 10)

        adventurer.gold += gold_gained
        adventurer.inventory["herbs"] += resources_gained
        adventurer.inventory["wood"] += random.randint(1, 2)

        if random.random() > 0.7:
            adventurer.inventory["seeds"] += 1
            print(f"{adventurer.name} нашел редкие семена в лесу!")

        print(f"{adventurer.name} исследовал лес: +{resources_gained} трав, +{gold_gained} золота")

    def _fish_in_lake(self, adventurer: 'Adventurer') -> None:
        """Рыбалка на озере"""
        fish_caught = random.randint(1, 4)
        adventurer.inventory["fish"] += fish_caught

        if random.random() > 0.9:
            rare_fish = random.randint(1, 2)
            adventurer.inventory["fish"] += rare_fish
            print(f"{adventurer.name} поймал редкую рыбу!")

        print(f"{adventurer.name} порыбачил на озере: +{fish_caught} рыбы")

    def _buy_equipment(self, adventurer: 'Adventurer') -> None:
        """Покупка снаряжения"""
        if adventurer.gold >= 50:
            adventurer.gold -= 50
            equipment_type = "weapon" if random.random() > 0.5 else "armor"
            old_equipment = adventurer.equipment[equipment_type]
            adventurer.equipment[equipment_type] = f"улучшенный {equipment_type}"
            adventurer.needs_equipment = False
            print(
                f"{adventurer.name} купил {equipment_type} за 50 золота ({old_equipment} -> {adventurer.equipment[equipment_type]})")

    def _return_to_town(self, adventurer: 'Adventurer') -> None:
        """Возвращение в город"""
        adventurer.current_location = Location.TOWN
        adventurer.state = AdventurerState.IDLE
        print(f"{adventurer.name} вернулся в город")

    def _check_level_up(self, adventurer: 'Adventurer') -> None:
        """Проверка повышения уровня"""
        while adventurer.experience >= adventurer.experience_to_next_level:
            adventurer.experience -= adventurer.experience_to_next_level
            self._level_up(adventurer)

    def _level_up(self, adventurer: 'Adventurer') -> None:
        """Повышение уровня"""
        adventurer.level += 1
        adventurer.max_health *= 1.2
        adventurer.attack_power *= 1.15
        adventurer.defense *= 1.1
        adventurer.health = adventurer.max_health
        adventurer.experience_to_next_level = int(adventurer.experience_to_next_level * 1.5)
        print(f"🎉 {adventurer.name} достиг {adventurer.level} уровня!")