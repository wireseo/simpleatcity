import enum

class Category(enum.Enum):
    FUSION = 0
    WESTERN = 1
    ITALIAN = 2
    SPANISH = 3
    MEXICAN = 4
    ASIAN = 5
    KOREAN = 6
    CHINESE = 7
    JAPANESE = 8
    THAI = 9
    INDIAN = 10

class Diet(enum.Enum):
    VEG = 0
    VEGAN = 1
    NON = 2
