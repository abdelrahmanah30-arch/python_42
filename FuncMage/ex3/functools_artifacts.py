import functools
import operator
from typing import Any, Callable


def partial_enchanter(
    base_enchantment: Callable[[int, str, str], str],
) -> dict[str, Callable[[str], str]]:
    fire_enchantment = functools.partial(
        base_enchantment,
        50,
        "Fire",
    )

    ice_enchantment = functools.partial(
        base_enchantment,
        50,
        "Ice",
    )

    lightning_enchantment = functools.partial(
        base_enchantment,
        50,
        "Lightning",
    )

    return {
        "fire": fire_enchantment,
        "ice": ice_enchantment,
        "lightning": lightning_enchantment,
    }


def base_enchantment(
    power: int,
    element: str,
    target: str,
) -> str:
    return f"{element} enchantment hits {target} with {power} power"


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n

    return (
        memoized_fibonacci(n - 1)
        + memoized_fibonacci(n - 2)
    )


def spell_dispatcher() -> Callable[[Any], str]:
    @functools.singledispatch
    def dispatcher(data: Any) -> str:
        return "Unknown spell type"

    @dispatcher.register
    def patch_int(data: int) -> str:
        return f"{data}"

    @dispatcher.register
    def patch_str(data: str) -> str:
        return f"{data}"

    @dispatcher.register(list)
    def patch_list(data: list[Any]) -> str:
        return f"{len(data)}"

    return dispatcher


def spell_reducer(
    spells: list[int],
    operation: str,
) -> int:
    if not spells:
        return 0

    operations: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max_number,
        "min": min_number,
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")

    operation_function = operations[operation]
    return functools.reduce(operation_function, spells)


def min_number(num_max: int, num_min: int) -> int:
    if num_max <= num_min:
        return num_min
    return num_max


def max_number(num_max: int, num_min: int) -> int:
    if num_max >= num_min:
        return num_max
    return num_min


def main_test() -> None:
    lis = [30, 20, 40, 10]
    print("Testing spell reducer...")
    print(f"Sum:  {spell_reducer(lis, "add")}")
    print(f"Product:  {spell_reducer(lis, "multiply")}")
    print(f"Max:  {spell_reducer(lis, "max")}")

    print("\n### this is test partial enchantment ###")
    enchanters = partial_enchanter(base_enchantment)

    print(enchanters["fire"]("Dragon"))
    print(enchanters["ice"]("Sword"))
    print(enchanters["lightning"]("Wizard"))

    print("\nTesting memoized Fibonacci...")

    print(f"Fib(0):  {memoized_fibonacci(0)}")
    print(f"Fib(1):  {memoized_fibonacci(1)}")
    print(f"Fib(10):  {memoized_fibonacci(10)}")
    print(f"Fib(15):  {memoized_fibonacci(15)}")
    dispatcher = spell_dispatcher()
    print("\nTesting spell dispatcher...")
    print(f"Damage spell: {dispatcher(42)} damage")
    print(f"Enchantment: {dispatcher("Fireball")}")
    print(f"Multi-cast: {dispatcher([1, 2, 3])} spells")
    print(dispatcher(3.5))


def main() -> None:
    lis = [30, 20, 40, 10]
    print("Testing spell reducer...")
    print(f"Sum:  {spell_reducer(lis, "add")}")
    print(f"Product:  {spell_reducer(lis, "multiply")}")
    print(f"Max:  {spell_reducer(lis, "max")}")

    print("\nTesting memoized Fibonacci...")

    print(f"Fib(0):  {memoized_fibonacci(0)}")
    print(f"Fib(1):  {memoized_fibonacci(1)}")
    print(f"Fib(10):  {memoized_fibonacci(10)}")
    print(f"Fib(15):  {memoized_fibonacci(15)}")

    dispatcher = spell_dispatcher()
    print("\nTesting spell dispatcher...")
    print(f"Damage spell: {dispatcher(42)} damage")
    print(f"Enchantment: {dispatcher("Fireball")}")
    print(f"Multi-cast: {dispatcher([1, 2, 3])} spells")
    print(dispatcher(3.5))


if __name__ == "__main__":
    main()
