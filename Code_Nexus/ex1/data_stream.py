from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._processed_count = 0
        self._data: list[Any] = []

    @abstractmethod
    def can_process(self, data: Any) -> bool:
        pass

    @abstractmethod
    def process(self, data: Any) -> None:
        pass

    def output(self) -> Any:
        if not self._data:
            print("No data available")
            return None
        return self._data.pop(0)

    @property
    def processed_count(self) -> int:
        return self._processed_count

    @property
    def remaining(self) -> int:
        return len(self._data)


class NumericProcessor(DataProcessor):
    def can_process(self, data: Any) -> bool:
        return isinstance(data, (int, float))

    def process(self, data: Any) -> None:
        self._data.append(data)
        self._processed_count += 1


class TextProcessor(DataProcessor):
    def can_process(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> None:
        self._data.append(data)
        self._processed_count += 1


class LogProcessor(DataProcessor):
    def can_process(self, data: Any) -> bool:
        if not isinstance(data, dict):
            return False

        return (
            "log_level" in data
            and "log_message" in data
            and isinstance(data["log_level"], str)
            and isinstance(data["log_message"], str)
        )

    def process(self, data: Any) -> None:
        self._data.append(data)
        self._processed_count += 1


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            self._process_element(element)

    def _process_element(self, element: Any) -> None:
        if isinstance(element, list):
            for item in element:
                self._process_element(item)
            return

        handled = False

        for processor in self._processors:
            if processor.can_process(element):
                processor.process(element)
                handled = True
                break

        if not handled:
            print(
                "DataStream error - Can't process element in stream:"
                f" {element}"
            )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return

        for processor in self._processors:
            name = processor.__class__.__name__.replace(
                "Processor",
                " Processor"
            )

            print(
                f"{name}: total {processor.processed_count} "
                f"items processed, remaining "
                f"{processor.remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")

    stream = DataStream()

    stream.print_processors_stats()

    print("\nRegistering Numeric Processor")

    numeric = NumericProcessor()

    stream.register_processor(numeric)

    batch = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]

    print(f"\nSend first batch of data on stream: {batch}")

    stream.process_stream(batch)

    stream.print_processors_stats()

    print("\nRegistering other data processors")

    text = TextProcessor()
    log = LogProcessor()

    stream.register_processor(text)
    stream.register_processor(log)

    print("\nSend the same batch again")

    stream.process_stream(batch)

    stream.print_processors_stats()

    print("\nConsume some elements from the data processors")

    print("Numeric:", numeric.output())
    print("Numeric:", numeric.output())
    print("Numeric:", numeric.output())

    print("Text:", text.output())
    print("Text:", text.output())

    print("Log:", log.output())

    print()

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
