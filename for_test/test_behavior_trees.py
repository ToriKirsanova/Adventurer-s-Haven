
"""
Behavior Trees - Деревья поведения
Что это:
Иерархическая структура узлов, где каждый узел представляет действие или условие.
Behavior Trees - для сложного иерархического поведения
"""
class BTNode:
    """Базовый класс узла дерева поведения"""

    def __init__(self, name):
        self.name = name

    def execute(self, entity):
        return True


class SequenceNode(BTNode):
    """Последовательность - выполняет всех детей пока они успешны"""

    def __init__(self, name, children):
        super().__init__(name)
        self.children = children

    def execute(self, entity):
        for child in self.children:
            if not child.execute(entity):
                return False
        return True


class SelectorNode(BTNode):
    """Селектор - выполняет первого успешного ребенка"""

    def __init__(self, name, children):
        super().__init__(name)
        self.children = children

    def execute(self, entity):
        for child in self.children:
            if child.execute(entity):
                return True
        return False


class ConditionNode(BTNode):
    """Условие - проверяет условие"""

    def __init__(self, name, condition_func):
        super().__init__(name)
        self.condition_func = condition_func

    def execute(self, entity):
        return self.condition_func(entity)


class ActionNode(BTNode):
    """Действие - выполняет действие"""

    def __init__(self, name, action_func):
        super().__init__(name)
        self.action_func = action_func

    def execute(self, entity):
        return self.action_func(entity)


class BehaviorTree:
    """Дерево поведения"""

    def __init__(self, root_node):
        self.root = root_node

    def update(self, entity):
        """Выполняет дерево поведения"""
        return self.root.execute(entity)


# Пример для магазина
class Shop:
    def __init__(self, name):
        self.name = name
        self.is_open = True
        self.customers_waiting = 2
        self.inventory = 15
        self.cleanliness = 80
        self.money = 100

        # Создаем Behavior Tree
        self.behavior_tree = self._create_behavior_tree()

    def _create_behavior_tree(self):
        """Создает дерево поведения для магазина"""

        # Листовые узлы (условия и действия)
        is_late = ConditionNode("Поздно?", lambda s: not s.is_open)
        close_shop = ActionNode("Закрыть", lambda s: print("  Магазин закрыт"))

        has_customers = ConditionNode("Есть клиенты?", lambda s: s.customers_waiting > 0)
        has_inventory = ConditionNode("Есть товары?", lambda s: s.inventory > 0)
        sell_goods = ActionNode("Продать", lambda s: s._sell_to_customer())

        low_inventory = ConditionNode("Мало товаров?", lambda s: s.inventory < 10)
        order_goods = ActionNode("Заказать", lambda s: s._order_goods())

        is_dirty = ConditionNode("Грязно?", lambda s: s.cleanliness < 50)
        clean_shop = ActionNode("Убраться", lambda s: s._clean())

        rest = ActionNode("Отдых", lambda s: print("  Владелец отдыхает"))

        # Построение дерева
        root = SelectorNode("Главный селектор", [
            SequenceNode("Закрытие", [is_late, close_shop]),

            SequenceNode("Обслуживание", [
                has_customers,
                SelectorNode("Стратегия обслуживания", [
                    SequenceNode("Продажа", [has_inventory, sell_goods]),
                    ActionNode("Извиниться", lambda s: print("  'Товара нет в наличии'"))
                ])
            ]),

            SequenceNode("Пополнение", [low_inventory, order_goods]),

            SequenceNode("Уборка", [is_dirty, clean_shop]),

            rest  # Действие по умолчанию
        ])

        return BehaviorTree(root)

    def _sell_to_customer(self):
        if self.inventory > 0 and self.customers_waiting > 0:
            self.inventory -= 1
            self.customers_waiting -= 1
            self.money += 10
            print("  Продан товар клиенту")
            return True
        return False

    def _order_goods(self):
        if self.money >= 15:
            self.money -= 15
            self.inventory += 10
            print("  Заказаны новые товары")
            return True
        return False

    def _clean(self):
        self.cleanliness = 100
        print("  Магазин убран")
        return True

    def update(self):
        """Обновление магазина"""
        print(f"\n{self.name}:")
        self.behavior_tree.update(self)

        # Симуляция изменений в мире
        self.cleanliness = max(0, self.cleanliness - 5)
        if self.is_open:
            self.customers_waiting += 1


# Использование
shop = Shop("Уголок")
for i in range(5):
    print(f"\n--- Цикл {i + 1} ---")
    shop.update()
