import alchemy
from elements import create_fire, create_water

print("=== Distillation 1 ===")
print("Using: ’import alchemy’ structure to access potions")
print(
    f"Testing strength_potion: {alchemy.strength_potion()} "
    f"'{create_fire()}' and '{create_water()}'"
)
print(f"Testing heal alias: {alchemy.heal()}")
