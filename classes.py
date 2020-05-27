class User:
    # requires tele_id at initialization
    # Initializes all fields but sets everything except tele_id to None (null)
    def __init__(self, tele_id, diet = None, liked_recipes = None, dislikes = None,
                likes = None, uploaded_recipes = None, fridge = None, utensils = None):
        self.tele_id = tele_id

class Utensil:
    # requires name and id at initialization
    def __init__(self, name, id):
        self.name = name
        self.id = id

class Recipe:
    # requires all fields, import from database
    # not sure if necessary at all
    def __init__(self, name, id, cat, main, sub, rating, veg, vegan, utensils,
                link, is_user_made):
        self.name = name
        self.id = id
        self.cat = cat
        self.main = main
        self.sub = sub
        self.rating = rating
        self.veg = veg
        self.vegan = vegan
        self.utensils = utensils
        self.link = link
        self.is_user_made = is_user_made

class Ingredient:
    def __init__(self, name, id, type):
        self.name = name
        self.id = id
        self.type = type
