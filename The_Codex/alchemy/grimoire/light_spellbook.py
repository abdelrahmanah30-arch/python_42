def light_spell_allowed_ingredients() -> list[str]:
    list_light: list[str] = ["Earth", "Air", "Fire", "Water"]
    return list_light


def light_spell_record(spell_name: str, ingredients: str) -> str:
    ingred: list[str] = []
    allowed_ingredints = light_spell_allowed_ingredients()
    ingred = ingredients.split(", ")
    for item in ingred:
        if item not in allowed_ingredints:
            return "rejected"
    return "recorded"
