from typing import List, Dict, Optional
from enum import Enum


class BuildingType(Enum):
    TAVERN = "Таверна"
    BLACKSMITH = "Кузница"
    ALCHEMY_SHOP = "Магазин зелий"
    ARMOR_SHOP = "Магазин доспехов"


class TavernService(Enum):
    FOOD = "Еда"
    DRINK = "Выпивка"
    ROOM_REST = "Комната для отдыха"


class FoodType(Enum):
    BASIC_MEAL = "Простая еда"
    HEARTY_STEW = "Сытное рагу"
    GRILLED_MEAT = "Жареное мясо"
    FISH_PLATE = "Рыбное блюдо"


class DrinkType(Enum):
    ALE = "Эль"
    WINE = "Вино"
    MAGIC_BREW = "Магический напиток"
    ENERGY_DRINK = "Энергетический напиток"


class CityLocation:
    """
    Класс, отвечающий за локацию города и управление зданиями
    """

    def __init__(self, name: str = "Старград"):
        self.name = name
        self.buildings = {}
        self.tavern_level = 1
        self.tavern_popularity = 0
        self._initialize_buildings()

    def _initialize_buildings(self) -> None:
        """Инициализация начальных зданий в городе"""
        self.buildings = {
            BuildingType.TAVERN: {
                'level': 1,
                'name': 'Подвыпивший дракон',
                'services_unlocked': [TavernService.FOOD, TavernService.DRINK, TavernService.ROOM_REST],
                'daily_visitors': 0
            },
            BuildingType.BLACKSMITH: {
                'level': 1,
                'name': 'Стальная кузня',
                'is_unlocked': True
            },
            BuildingType.ALCHEMY_SHOP: {
                'level': 1,
                'name': 'Склянка и жаба',
                'is_unlocked': True
            },
            BuildingType.ARMOR_SHOP: {
                'level': 1,
                'name': 'Щит и кольчуга',
                'is_unlocked': True
            }
        }

    class Tavern:
        """
        Вложенный класс Таверны для управления услугами
        """

        def __init__(self, city: 'CityLocation'):
            self.city = city

            # Цены на основные типы услуг
            self.service_prices = {
                TavernService.FOOD: 15,
                TavernService.DRINK: 10,
                TavernService.ROOM_REST: 30
            }

            # Еда: баффы + небольшое восстановление здоровья
            self.food_menu = {
                FoodType.BASIC_MEAL: {
                    "price": 15,
                    "health_restore": 0.2,
                    "buff": {"type": "strength", "value": 1.05, "duration": 3600},
                    "ingredients": {"bread": 1, "vegetables": 1}
                },
                FoodType.HEARTY_STEW: {
                    "price": 25,
                    "health_restore": 0.4,
                    "buff": {"type": "health", "value": 1.1, "duration": 5400},
                    "ingredients": {"meat": 1, "vegetables": 2, "bread": 1}
                },
                FoodType.GRILLED_MEAT: {
                    "price": 35,
                    "health_restore": 0.3,
                    "buff": {"type": "attack", "value": 1.15, "duration": 7200},
                    "ingredients": {"meat": 2, "vegetables": 1}
                },
                FoodType.FISH_PLATE: {
                    "price": 30,
                    "health_restore": 0.25,
                    "buff": {"type": "agility", "value": 1.12, "duration": 4800},
                    "ingredients": {"fish": 2, "vegetables": 1, "bread": 1}
                }
            }

            # Выпивка: восстановление маны + различные эффекты
            self.drink_menu = {
                DrinkType.ALE: {
                    "price": 10,
                    "mana_restore": 0.3,
                    "effect": {"type": "morale", "value": 1.08, "duration": 1800},
                    "ingredients": {"wheat": 2}
                },
                DrinkType.WINE: {
                    "price": 20,
                    "mana_restore": 0.5,
                    "effect": {"type": "charisma", "value": 1.1, "duration": 2700},
                    "ingredients": {"grapes": 3}
                },
                DrinkType.MAGIC_BREW: {
                    "price": 40,
                    "mana_restore": 0.8,
                    "effect": {"type": "magic_power", "value": 1.2, "duration": 3600},
                    "ingredients": {"magic_herbs": 2, "crystal_dust": 1}
                },
                DrinkType.ENERGY_DRINK: {
                    "price": 25,
                    "mana_restore": 0.4,
                    "effect": {"type": "stamina", "value": 1.15, "duration": 2400},
                    "ingredients": {"energy_herbs": 2, "sugar": 1}
                }
            }

            # Ингредиенты в таверне
            self.available_ingredients = {
                "meat": 0, "fish": 0, "vegetables": 0, "bread": 0,
                "wheat": 0, "grapes": 0, "magic_herbs": 0,
                "crystal_dust": 0, "energy_herbs": 0, "sugar": 0
            }

        def order_food(self, adventurer, food_type: FoodType) -> bool:
            """
            Заказ еды авантюристом

            Args:
                adventurer: Объект авантюриста
                food_type: Тип еды

            Returns:
                bool: Успешно ли оказана услуга
            """
            if not adventurer.is_alive:
                print(f"{adventurer.name} мёртв и не может есть!")
                return False

            food_data = self.food_menu.get(food_type)
            if not food_data:
                print(f"Блюдо {food_type.value} недоступно!")
                return False

            # Проверка денег
            if adventurer.gold < food_data["price"]:
                print(f"У {adventurer.name} недостаточно золота для {food_type.value}!")
                return False

            # Проверка ингредиентов
            if not self._check_ingredients(food_data["ingredients"]):
                print(f"Недостаточно ингредиентов для {food_type.value}!")
                return False

            # Оплата
            adventurer.gold -= food_data["price"]
            print(f"💰 {adventurer.name} платит {food_data['price']} золота за {food_type.value}")

            # Восстановление здоровья
            health_restore = adventurer.max_health * food_data["health_restore"]
            old_health = adventurer.health
            adventurer.health = min(adventurer.max_health, adventurer.health + health_restore)
            actual_restore = adventurer.health - old_health

            print(f"❤️ {adventurer.name} восстанавливает {actual_restore:.1f} здоровья")
            print(f"❤️ Теперь у {adventurer.name} {adventurer.health:.1f}/{adventurer.max_health:.1f} HP")

            # Применение баффа
            self._apply_buff(adventurer, food_data["buff"])

            # Расход ингредиентов
            self._use_ingredients(food_data["ingredients"])

            self._record_visit()
            return True

        def order_drink(self, adventurer, drink_type: DrinkType) -> bool:
            """
            Заказ выпивки авантюристом

            Args:
                adventurer: Объект авантюриста
                drink_type: Тип напитка

            Returns:
                bool: Успешно ли оказана услуга
            """
            if not adventurer.is_alive:
                print(f"{adventurer.name} мёртв и не может пить!")
                return False

            drink_data = self.drink_menu.get(drink_type)
            if not drink_data:
                print(f"Напиток {drink_type.value} недоступен!")
                return False

            # Проверка денег
            if adventurer.gold < drink_data["price"]:
                print(f"У {adventurer.name} недостаточно золота для {drink_type.value}!")
                return False

            # Проверка ингредиентов
            if not self._check_ingredients(drink_data["ingredients"]):
                print(f"Недостаточно ингредиентов для {drink_type.value}!")
                return False

            # Оплата
            adventurer.gold -= drink_data["price"]
            print(f"💰 {adventurer.name} платит {drink_data['price']} золота за {drink_type.value}")

            # Восстановление маны (если у авантюриста есть мана)
            if hasattr(adventurer, 'mana') and hasattr(adventurer, 'max_mana'):
                mana_restore = adventurer.max_mana * drink_data["mana_restore"]
                old_mana = adventurer.mana
                adventurer.mana = min(adventurer.max_mana, adventurer.mana + mana_restore)
                actual_restore = adventurer.mana - old_mana
                print(f"🔮 {adventurer.name} восстанавливает {actual_restore:.1f} маны")
                print(f"🔮 Теперь у {adventurer.name} {adventurer.mana:.1f}/{adventurer.max_mana:.1f} MP")
            else:
                print(f"💡 {adventurer.name} наслаждается напитком, но мана не восстановлена")

            # Применение эффекта
            self._apply_effect(adventurer, drink_data["effect"])

            # Расход ингредиентов
            self._use_ingredients(drink_data["ingredients"])

            self._record_visit()
            return True

        def rent_room(self, adventurer) -> bool:
            """
            Аренда комнаты для отдыха

            Args:
                adventurer: Объект авантюриста

            Returns:
                bool: Успешно ли оказана услуга
            """
            if not adventurer.is_alive:
                print(f"{adventurer.name} мёртв и не может отдыхать!")
                return False

            price = self.service_prices[TavernService.ROOM_REST]

            # Проверка денег
            if adventurer.gold < price:
                print(f"У {adventurer.name} недостаточно золота для аренды комнаты!")
                return False

            # Оплата
            adventurer.gold -= price
            print(f"💰 {adventurer.name} платит {price} золота за комнату отдыха")

            # Полное восстановление здоровья
            old_health = adventurer.health
            adventurer.health = adventurer.max_health
            health_restored = adventurer.health - old_health

            print(f"❤️ {adventurer.name} полностью восстановил здоровье! +{health_restored:.1f} HP")
            print(f"❤️ Теперь у {adventurer.name} {adventurer.health:.1f}/{adventurer.max_health:.1f} HP")

            # Восстановление маны (если есть)
            if hasattr(adventurer, 'mana') and hasattr(adventurer, 'max_mana'):
                old_mana = adventurer.mana
                adventurer.mana = adventurer.max_mana
                mana_restored = adventurer.mana - old_mana
                print(f"🔮 {adventurer.name} полностью восстановил ману! +{mana_restored:.1f} MP")
                print(f"🔮 Теперь у {adventurer.name} {adventurer.mana:.1f}/{adventurer.max_mana:.1f} MP")

            print(f"😴 {adventurer.name} хорошо отдохнул и готов к новым приключениям!")

            self._record_visit()
            return True

        def _check_ingredients(self, required_ingredients: Dict[str, int]) -> bool:
            """Проверка наличия ингредиентов"""
            for ingredient, amount in required_ingredients.items():
                if self.available_ingredients.get(ingredient, 0) < amount:
                    return False
            return True

        def _use_ingredients(self, ingredients: Dict[str, int]) -> None:
            """Расход ингредиентов"""
            for ingredient, amount in ingredients.items():
                self.available_ingredients[ingredient] = max(0, self.available_ingredients.get(ingredient, 0) - amount)

        def _apply_buff(self, adventurer, buff: Dict) -> None:
            """Применение баффа от еды"""
            buff_type = buff["type"]
            value = buff["value"]
            duration = buff["duration"]

            if buff_type == "strength":
                adventurer.attack_power *= value
                print(f"💪 {adventurer.name} получает бафф силы! Атака ×{value}")
            elif buff_type == "health":
                adventurer.max_health *= value
                print(f"❤️ {adventurer.name} получает бафф здоровья! Макс. здоровье ×{value}")
            elif buff_type == "attack":
                adventurer.attack_power *= value
                print(f"⚔️ {adventurer.name} получает бафф атаки! Сила атаки ×{value}")
            elif buff_type == "agility":
                if hasattr(adventurer, 'agility'):
                    adventurer.agility *= value
                print(f"🏹 {adventurer.name} получает бафф ловкости! Ловкость ×{value}")

            print(f"⏰ Длительность баффа: {duration // 60} минут")

        def _apply_effect(self, adventurer, effect: Dict) -> None:
            """Применение эффекта от выпивки"""
            effect_type = effect["type"]
            value = effect["value"]
            duration = effect["duration"]

            if effect_type == "morale":
                print(f"😊 {adventurer.name} в приподнятом настроении! Мораль ×{value}")
            elif effect_type == "charisma":
                print(f"🎭 {adventurer.name} становится более убедительным! Харизма ×{value}")
            elif effect_type == "magic_power":
                if hasattr(adventurer, 'spell_power'):
                    adventurer.spell_power *= value
                print(f"🔮 {adventurer.name} чувствует прилив магической силы! Сила заклинаний ×{value}")
            elif effect_type == "stamina":
                print(f"⚡ {adventurer.name} полон энергии! Выносливость ×{value}")

            print(f"⏰ Длительность эффекта: {duration // 60} минут")

        def _record_visit(self) -> None:
            """Учет посещения таверны"""
            self.city.buildings[BuildingType.TAVERN]['daily_visitors'] += 1
            self.city.tavern_popularity += 1

        def add_ingredients(self, ingredients: Dict[str, int]) -> None:
            """Добавление ингредиентов в таверну"""
            for ingredient, amount in ingredients.items():
                self.available_ingredients[ingredient] = self.available_ingredients.get(ingredient, 0) + amount
            print(f"📦 Таверна получила ингредиенты: {ingredients}")

        def get_available_food(self) -> List[FoodType]:
            """Получение списка доступной еды"""
            return list(self.food_menu.keys())

        def get_available_drinks(self) -> List[DrinkType]:
            """Получение списка доступных напитков"""
            return list(self.drink_menu.keys())

        def get_ingredients_status(self) -> str:
            """Получение статуса ингредиентов"""
            status = "🍖 Ингредиенты в таверне:\n"
            for ingredient, amount in self.available_ingredients.items():
                if amount > 0:
                    status += f"   - {ingredient}: {amount}\n"
            return status

    def get_tavern(self) -> 'Tavern':
        """Получение объекта таверны"""
        return self.Tavern(self)

    def get_city_status(self) -> str:
        """Получение статуса города"""
        status = f"🏰 Город: {self.name}\n"
        status += f"📊 Уровень таверны: {self.tavern_level}\n"
        status += f"👥 Популярность таверны: {self.tavern_popularity}\n"
        status += f"🏠 Посещений таверны сегодня: {self.buildings[BuildingType.TAVERN]['daily_visitors']}\n"
        return status


# Пример использования
if __name__ == "__main__":
    # Создаем город и таверну
    city = CityLocation("Старград")
    tavern = city.get_tavern()


    # Создаем авантюристов (добавим ману для демонстрации)
    class MageAdventurer:
        def __init__(self, name):
            self.name = name
            self.is_alive = True
            self.health = 40
            self.max_health = 100
            self.mana = 20
            self.max_mana = 100
            self.gold = 200
            self.attack_power = 15
            self.spell_power = 25


    mage = MageAdventurer("Гэндальф")

    print("=== ДО ПОСЕЩЕНИЯ ТАВЕРНЫ ===")
    print(f"{mage.name}: {mage.health}/{mage.max_health} HP, {mage.mana}/{mage.max_mana} MP")

    # Добавляем ингредиенты
    tavern.add_ingredients({
        "meat": 10, "fish": 8, "vegetables": 15, "bread": 12,
        "wheat": 20, "grapes": 10, "magic_herbs": 5
    })

    print("\n=== ПОСЕЩЕНИЕ ТАВЕРНЫ ===")
    # Заказываем еду
    tavern.order_food(mage, FoodType.GRILLED_MEAT)
    print()

    # Заказываем выпивку
    tavern.order_drink(mage, DrinkType.MAGIC_BREW)
    print()

    # Арендуем комнату для полного восстановления
    tavern.rent_room(mage)

    print("\n=== СТАТУС ИНГРЕДИЕНТОВ ===")
    print(tavern.get_ingredients_status())

    print("\n=== СТАТУС ГОРОДА ===")
    print(city.get_city_status())