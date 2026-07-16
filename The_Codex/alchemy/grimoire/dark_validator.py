from .dark_spellbook import dark_spell_allowed_ingredients


def dark_ingredients(ingredients: str) -> str:
    allowed_ingredints = ["bats", "frogs", "arsenic", "eyeball"]
    ingred: list[str] = []
    ingred = ingredients.split(", ")
    for item in ingred:
        if item in allowed_ingredints:
            return "VALID"
    return "INVALID"
