def validate_ingredients(ingredients: str) -> str:
    allowed_ingredints = ["Earth", "Air", "Fire", "Water"]
    ingred: list[str] = []
    ingred = ingredients.split(", ")
    for item in ingred:
        if item in allowed_ingredints:
            return "VALID"
    return "INVALID"
