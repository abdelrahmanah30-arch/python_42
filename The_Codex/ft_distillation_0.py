from alchemy.potions import healing_potion, strength_potion
from elements import create_fire, create_water

print("=== Distillation 0 ===")
print(
    f"Testing strength_potion: {strength_potion()} "
    f"'{create_fire()}' and '{create_water()}'"
)
print(f"Testing healing_potion: {healing_potion()}")
