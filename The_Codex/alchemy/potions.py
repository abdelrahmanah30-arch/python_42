from alchemy.elements import create_air, create_earth


def healing_potion() -> str:
    return (
        f"Healing potion brewed with '{create_earth()}'"
        f" and '{create_air()}'"
    )


def strength_potion() -> str:
    return (
        "Strength potion brewed with"
    )
