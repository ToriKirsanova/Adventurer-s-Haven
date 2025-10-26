from enum import Enum


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