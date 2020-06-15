import enum

class Category(enum.Enum):
    FUSION = 1
    WESTERN = 2
    ITALIAN = 3
    MEXICAN = 4
    ASIAN = 5
    KOREAN = 6
    JAPANESE = 7
    THAI = 8
    INDIAN = 9

class Diet(enum.Enum):
    VEG = 0
    VEGAN = 1
    NON = 2 # for non veg get 0/1/2, for veg get 0/1 and vegan get 1
