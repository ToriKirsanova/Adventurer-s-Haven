from transitions import Machine
import random
import time

"""
FSM (Finite State Machine) - Конечный автомат
Что это:
Программа, которая может находиться в одном из конечного числа состояний. Переход между состояниями происходит по определенным правилам.
FSM - когда поведение предсказуемо и имеет четкие состояния
"""
class Civilian:
    """Мирный житель с FSM"""

    states = ['работа', 'отдых', 'общение', 'сон', 'еда']

    def __init__(self, name):
        self.name = name
        self.energy = 100
        self.hunger = 0
        self.social_need = 50

        # Инициализация FSM
        self.machine = Machine(
            model=self,
            states=Civilian.states,
            initial='сон'
        )

        # Добавляем переходы между состояниями
        self.machine.add_transition(
            trigger='проснуться',
            source='сон',
            dest='еда',
            conditions=['is_hungry']
        )

        self.machine.add_transition(
            trigger='проснуться',
            source='сон',
            dest='работа',
            unless=['is_hungry']
        )

        self.machine.add_transition(
            trigger='пора_работать',
            source='еда',
            dest='работа'
        )

        self.machine.add_transition(
            trigger='устал',
            source='работа',
            dest='отдых',
            conditions=['is_tired']
        )

        self.machine.add_transition(
            trigger='скучно',
            source='отдых',
            dest='общение',
            conditions=['needs_social']
        )

        self.machine.add_transition(
            trigger='спать',
            source=['общение', 'отдых'],
            dest='сон',
            conditions=['is_sleepy']
        )

        print(f"{self.name} создан. Начальное состояние: {self.state}")

    def is_hungry(self):
        return self.hunger > 70

    def is_tired(self):
        return self.energy < 30

    def needs_social(self):
        return self.social_need > 60

    def is_sleepy(self):
        return self.energy < 20

    def update(self):
        """Обновление состояния жителя"""
        # Изменяем потребности
        self.energy -= random.randint(1, 5)
        self.hunger += random.randint(2, 8)
        self.social_need += random.randint(1, 3)

        # Логика автоматических переходов
        if self.state == 'работа':
            print(f"{self.name} работает...")
            if self.is_tired():
                self.устал()

        elif self.state == 'еда':
            print(f"{self.name} ест...")
            self.hunger = max(0, self.hunger - 50)
            self.пора_работать()

        elif self.state == 'отдых':
            print(f"{self.name} отдыхает...")
            self.energy = min(100, self.energy + 10)
            if self.needs_social():
                self.скучно()
            elif self.is_sleepy():
                self.спать()

        elif self.state == 'общение':
            print(f"{self.name} общается с соседями...")
            self.social_need = max(0, self.social_need - 30)
            self.energy -= 5
            if self.is_sleepy():
                self.спать()

        elif self.state == 'сон':
            print(f"{self.name} спит...")
            self.energy = min(100, self.energy + 20)
            if self.energy > 80:
                self.проснуться()


# Использование
civilian = Civilian("Иван")
for i in range(10):
    # Симуляция дня
    for hour in range(24):
        print(f"\n--- Час {hour}:00 ---")
        civilian.update()
        time.sleep(0.5)
