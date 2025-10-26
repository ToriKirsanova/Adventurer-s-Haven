
"""
Utility AI - Система полезности
Что это:
Система, которая оценивает "полезность" каждого возможного действия и выбирает наиболее подходящее.
Utility AI - когда нужно выбирать из множества вариантов с разной "ценностью"
"""
class UtilityAction:
    """Действие для Utility AI"""

    def __init__(self, name, utility_func, execute_func):
        self.name = name
        self.utility_func = utility_func
        self.execute_func = execute_func

    def calculate_utility(self, entity, world):
        return self.utility_func(entity, world)

    def execute(self, entity, world):
        return self.execute_func(entity, world)


class UtilityAI:
    """Система полезности для принятия решений"""

    def __init__(self):
        self.actions = []
        self.last_action = None

    def add_action(self, action):
        self.actions.append(action)

    def decide(self, entity, world):
        """Выбирает и выполняет лучшее действие"""
        best_action = None
        best_utility = -1

        # Оцениваем полезность каждого действия
        for action in self.actions:
            utility = action.calculate_utility(entity, world)
            print(f"  {action.name}: {utility:.2f}")

            if utility > best_utility:
                best_utility = utility
                best_action = action

        # Выполняем действие если оно достаточно полезно
        if best_action and best_utility > 0.1:
            if best_action != self.last_action:
                print(f"{entity.name} решает: {best_action.name}")
                self.last_action = best_action

            best_action.execute(entity, world)
            return best_action

        return None


# Пример для торговца
class Merchant:
    def __init__(self, name):
        self.name = name
        self.gold = 150
        self.inventory = 30
        self.max_inventory = 100
        self.customers = 3
        self.energy = 80

        # Настраиваем Utility AI
        self.ai = UtilityAI()
        self._setup_actions()

    def _setup_actions(self):
        """Настраиваем возможные действия торговца"""

        # Закупка товаров
        buy_action = UtilityAction(
            name="закупить товары",
            utility_func=lambda e, w: self._calc_buy_utility(),
            execute_func=lambda e, w: self._execute_buy()
        )

        # Продажа товаров
        sell_action = UtilityAction(
            name="продавать товары",
            utility_func=lambda e, w: self._calc_sell_utility(),
            execute_func=lambda e, w: self._execute_sell()
        )

        # Реклама
        advertise_action = UtilityAction(
            name="рекламировать",
            utility_func=lambda e, w: self._calc_advertise_utility(),
            execute_func=lambda e, w: self._execute_advertise()
        )

        # Отдых
        rest_action = UtilityAction(
            name="отдыхать",
            utility_func=lambda e, w: self._calc_rest_utility(),
            execute_func=lambda e, w: self._execute_rest()
        )

        self.ai.add_action(buy_action)
        self.ai.add_action(sell_action)
        self.ai.add_action(advertise_action)
        self.ai.add_action(rest_action)

    # Расчет полезности
    def _calc_buy_utility(self):
        """Полезность закупки товаров"""
        inventory_ratio = self.inventory / self.max_inventory
        money_ratio = self.gold / 200  # Предполагаем максимум 200 золота

        # Чем меньше товаров и больше денег - тем полезнее закупать
        utility = (1 - inventory_ratio) * money_ratio
        return utility * 0.8

    def _calc_sell_utility(self):
        """Полезность продажи"""
        if self.customers > 0 and self.inventory > 0:
            customer_pressure = min(1.0, self.customers / 5.0)
            inventory_ratio = self.inventory / self.max_inventory
            return customer_pressure * inventory_ratio * 0.9
        return 0.0

    def _calc_advertise_utility(self):
        """Полезность рекламы"""
        if self.customers < 3 and self.gold > 30:
            customer_need = 1.0 - (self.customers / 5.0)
            money_ratio = self.gold / 200
            return customer_need * money_ratio * 0.7
        return 0.0

    def _calc_rest_utility(self):
        """Полезность отдыха"""
        energy_ratio = self.energy / 100.0
        return (1.0 - energy_ratio) * 0.6

    # Выполнение действий
    def _execute_buy(self):
        cost = 25
        if self.gold >= cost:
            self.gold -= cost
            self.inventory += 20
            print(f"  Куплено товаров на {cost} золота")

    def _execute_sell(self):
        if self.inventory >= 5 and self.customers >= 1:
            self.inventory -= 5
            self.gold += 15
            self.customers -= 1
            print(f"  Продано товаров за 15 золота")

    def _execute_advertise(self):
        cost = 10
        if self.gold >= cost:
            self.gold -= cost
            self.customers += 2
            print(f"  Потрачено {cost} золота на рекламу")

    def _execute_rest(self):
        self.energy = min(100, self.energy + 20)
        print(f"  Отдых: энергия +20")

    def update(self, world):
        """Обновление торговца"""
        print(f"\n{self.name}:")

        # Обновляем состояние
        self.energy = max(0, self.energy - 5)
        self.customers = max(0, self.customers - 0.5)

        # Принимаем решение
        self.ai.decide(self, world)


# Использование
merchant = Merchant("Петр-торговец")
for day in range(3):
    print(f"\n=== День {day + 1} ===")
    for hour in range(3):  # 3 действия в день
        merchant.update(None)
