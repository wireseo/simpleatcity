import enum

class Category(enum.Enum):
    FUSION = 0
    WESTERN = 1
    ITALIAN = 2
    MEXICAN = 3
    ASIAN = 4
    KOREAN = 5
    JAPANESE = 6
    THAI = 7
    INDIAN = 8

class Diet(enum.Enum):
    VEG = 0
    VEGAN = 1
    NON = 2
