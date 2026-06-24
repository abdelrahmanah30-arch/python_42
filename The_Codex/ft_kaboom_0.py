import alchemy.grimoire

spell_name = "Fantasy"
ingredients = "Earth, wind and fire"
print("=== Kaboom 0 ===")
print("Using grimoire module directly")
print(
    "Testing record light spell: Spell recorded: "
    f"{spell_name} ({ingredients} - "
    f"{alchemy.grimoire.validate_ingredients(ingredients)})")
