from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import random


class AIBehavior(ABC):
    """Абстрактный базовый класс для поведения ИИ"""

    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.last_update_time = 0
        self.current_goal = None
        self.state = None

    @abstractmethod
    def update(self, current_time: float, entity: Any, world: Any) -> None:
        """Основной метод обновления ИИ"""
        pass

    def should_update(self, current_time: float) -> bool:
        """Проверяет, нужно ли обновлять ИИ в этом кадре"""
        return current_time - self.last_update_time >= self.update_interval

    def record_update(self, current_time: float) -> None:
        """Записывает время последнего обновления"""
        self.last_update_time = current_time