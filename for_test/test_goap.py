
"""
GOAP (Goal-Oriented Action Planning)
Что это:
Система планирования, где ИИ ставит цели и находит последовательность действий для их достижения.
GOAP - для тактического планирования и адаптивного поведения
"""
class GoapAction:
    """Действие для GOAP"""

    def __init__(self, name, cost, preconditions, effects):
        self.name = name
        self.cost = cost
        self.preconditions = preconditions  # Словарь условий
        self.effects = effects  # Словарь эффектов

    def is_valid(self, world_state):
        """Проверяет можно ли выполнить действие в текущем состоянии"""
        for key, value in self.preconditions.items():
            if world_state.get(key) != value:
                return False
        return True

    def execute(self, entity):
        """Выполняет действие"""
        print(f"  Выполняется: {self.name}")
        return True


class GoapGoal:
    """Цель для GOAP"""

    def __init__(self, name, priority=1):
        self.name = name
        self.priority = priority
        self.desired_state = {}

    def is_achieved(self, world_state):
        """Проверяет достигнута ли цель"""
        for key, value in self.desired_state.items():
            if world_state.get(key) != value:
                return False
        return True


class SimpleGoapPlanner:
    """Упрощенный планировщик GOAP"""

    def __init__(self):
        self.actions = []
        self.goals = []

    def find_plan(self, world_state, max_depth=5):
        """Находит план достижения цели"""
        # Ищем самую приоритетную невыполненную цель
        sorted_goals = sorted(self.goals, key=lambda g: g.priority, reverse=True)

        for goal in sorted_goals:
            if goal.is_achieved(world_state):
                continue

            plan = self._build_plan(world_state, goal, [], max_depth)
            if plan:
                return plan

        return None

    def _build_plan(self, current_state, goal, current_plan, max_depth):
        """Рекурсивно строит план"""
        if len(current_plan) >= max_depth:
            return None

        # Если цель достигнута
        if goal.is_achieved(current_state):
            return current_plan

        # Ищем действия которые приближают к цели
        for action in self.actions:
            if (action.is_valid(current_state) and
                    action not in current_plan):

                # Применяем эффекты действия
                new_state = current_state.copy()
                new_state.update(action.effects)

                # Рекурсивно ищем план
                new_plan = current_plan + [action]
                result = self._build_plan(new_state, goal, new_plan, max_depth)

                if result:
                    return result

        return None


# Пример для врага
class Enemy:
    def __init__(self, name):
        self.name = name
        self.health = 50
        self.has_weapon = False
        self.near_player = False
        self.player_health = 100

        # GOAP система
        self.planner = SimpleGoapPlanner()
        self._setup_goap()

    def _setup_goap(self):
        """Настраиваем GOAP систему"""

        # Действия
        find_weapon = GoapAction(
            name="Найти оружие",
            cost=1,
            preconditions={'see_weapon': True},
            effects={'has_weapon': True}
        )

        move_to_player = GoapAction(
            name="Подойти к игроку",
            cost=1,
            preconditions={'see_player': True},
            effects={'near_player': True}
        )

        attack_player = GoapAction(
            name="Атаковать игрока",
            cost=2,
            preconditions={'near_player': True, 'has_weapon': True},
            effects={'player_health': -20}
        )

        flee = GoapAction(
            name="Бежать",
            cost=1,
            preconditions={'low_health': True},
            effects={'safe': True}
        )

        self.planner.actions = [find_weapon, move_to_player, attack_player, flee]

        # Цели
        attack_goal = GoapGoal("Атаковать игрока", priority=2)
        attack_goal.desired_state = {'player_health': 0}

        survive_goal = GoapGoal("Выжить", priority=3)
        survive_goal.desired_state = {'safe': True}

        self.planner.goals = [attack_goal, survive_goal]

    def get_world_state(self):
        """Возвращает текущее состояние мира"""
        return {
            'see_weapon': True,
            'see_player': True,
            'has_weapon': self.has_weapon,
            'near_player': self.near_player,
            'low_health': self.health < 30,
            'player_health': self.player_health,
            'safe': False
        }

    def update(self):
        """Обновление врага"""
        print(f"\n{self.name}:")

        world_state = self.get_world_state()
        plan = self.planner.find_plan(world_state)

        if plan:
            print(f"  План: {' -> '.join([action.name for action in plan])}")
            # Выполняем первое действие плана
            if plan:
                action = plan[0]
                action.execute(self)

                # Обновляем состояние на основе действия
                if action.name == "Найти оружие":
                    self.has_weapon = True
                elif action.name == "Подойти к игроку":
                    self.near_player = True
                elif action.name == "Атаковать игрока":
                    self.player_health -= 20
                    self.health -= 5  # Получаем урон в бою
                elif action.name == "Бежать":
                    self.near_player = False
        else:
            print("  Нет доступного плана")


# Использование
enemy = Enemy("Орк")
for turn in range(5):
    print(f"\n--- Ход {turn + 1} ---")
    enemy.update()

    # Меняем состояние для демонстрации
    if turn == 2:
        enemy.health = 25
        print("  Враг получил ранение!")
