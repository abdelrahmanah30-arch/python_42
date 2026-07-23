from typing import Callable


def mage_counter() -> Callable[[], int]:
    count = 0

    def counters() -> int:
        nonlocal count
        count += 1
        return count

    return counters


def spell_accumulator(
        initial_power: int
) -> Callable[[int], int]:

    power = initial_power

    def accumulator(amount: int) -> int:
        nonlocal power
        power += amount
        return power

    return accumulator


def enchantment_factory(
        enchantment_type: str
) -> Callable[[str], str]:

    def enchantment(item_type: str) -> str:
        return f"{enchantment_type} {item_type}"

    return enchantment


def memory_vault() -> dict[str, Callable[..., object]]:
    vault: dict[str, str] = {}

    def store(key: str, value: str) -> None:
        vault[key] = value

    def recall(key: str) -> str:
        if key in vault:
            return vault[key]
        return "Memory not found"

    return {
        "store": store,
        "recall": recall,
    }


def main() -> None:
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    base = 100
    accumulator = spell_accumulator(base)
    num1 = 20
    num2 = 30
    print(f"Base {base}, add {num1}:  {accumulator(num1)}")
    print(f"Base {base}, add {num2}:  {accumulator(num2)}")

    print("\nTesting enchantment factory...")
    Flaming = enchantment_factory("Flaming")
    Frozen = enchantment_factory("Frozen")
    print(Flaming("Sword"))
    print(Frozen("Shield"))

    print("\nTesting memory vault...")
    memory = memory_vault()
    value = "42"
    unknown = "mage"
    memory["store"]("secret", value)
    print(f"Store ’secret’ = {value}")
    print(f"Recall ’secret’: {memory["recall"]("secret")}")
    print(f"Recall ’unknown’: {memory["recall"](unknown)}")


if __name__ == "__main__":
    main()
