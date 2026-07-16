from .dark_validator import dark_ingredients


def dark_spell_allowed_ingredients() -> list[str]:
    ingredients: list[str] = ["bats", "frogs", "arsenic", "eyeball"]
    return ingredients


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    ingred: list[str] = []
    allowed_ingredints = dark_spell_allowed_ingredients()
    ingred = ingredients.split(", ")
    for item in ingred:
        if item not in allowed_ingredints:
            return "rejected"
    return "recorded"
