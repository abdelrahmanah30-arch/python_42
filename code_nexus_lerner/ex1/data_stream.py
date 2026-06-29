from abc import ABC, abstractmethod
from typing import Any
import typing


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise Exception("storage is empty")

        key, value = self._storage.pop(0)
        return key, value


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, int | float):
            return True
        elif isinstance(data, list):
            return all(isinstance(item, int | float) for item in data)

        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")

        if isinstance(data, int | float):
            self._rank += 1
            self._storage.append((self._rank, str(data)))
        if isinstance(data, list):
            for item in data:
                if not self.validate(item):
                    raise Exception("Improper numeric data")
                self._rank += 1
                self._storage.append((self._rank, str(item)))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        elif isinstance(data, list):
            return all(isinstance(item, str) for item in data)

        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise Exception("Invalid text process data")
        if isinstance(data, str):
            self._rank += 1
            self._storage.append((self._rank, str(data)))

        elif isinstance(data, list):
            for item in data:
                if not self.validate(item):
                    raise Exception("Invalid text process data")

                self._rank += 1
                self._storage.append((self._rank, str(item)))


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(key, str) and
                isinstance(value, str)
                for key, value in data.items()
            )
        elif isinstance(data, list):
            return all(
                isinstance(item, dict) and
                all(
                    isinstance(key, str) and
                    isinstance(value, str) for key, value in item.items()
                )
                for item in data
            )
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:

        if isinstance(data, dict):
            if not self.validate(data):
                raise Exception("Invalid log data")
            self._rank += 1
            self._storage.append(
                (self._rank, self._format_log(data))
            )
        elif isinstance(data, list):
            for item in data:
                if not self.validate(item):
                    raise Exception("Invalid log data in list")

                self._rank += 1
                self._storage.append(
                    (self._rank, self._format_log(item))
                )
        else:
            raise Exception("Invalid log data type")

    def _format_log(self, log: dict[str, str]) -> str:
        return ": ".join(f"{value}" for key, value in log.items())


class DataStream():
    def __init__(self) -> None:
        self.processor: list[typing.Any] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processor.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:

        if not stream:
            print("No processor found, no data\n")
            return

        for item in stream:
            if not any(process.validate(item) for process in self.processor):
                print("No processor can handle item")
                continue

            for process in self.processor:
                if process.validate(item):
                    process.ingest(item)
                    break

    def print_processors_stats(self) -> None:
        for processor in self.processor:
            print(
                type(processor).__name__,
                "→",
                len(processor._storage),
                "items processed"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    print("== DataStream statistics ==")
    test: list[typing.Any] = []
    stream_test = DataStream()
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    stream_test.register_processor(numeric)
    stream_test.register_processor(text)
    stream_test.register_processor(log)
    stream_test.process_stream(test)
    print("Registering Numeric Processor\n")
    data = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead"
            },
            {
                "log_level": "INFO", "log_message":
                "User willis is connected"
            }
        ],
        42,
        ["Hi", "five"]
    ]

    stream_test.process_stream(data)
    print(f"Send first batch of data on stream: {data}")
    for item in data:
        if not numeric.validate(item):
            print(
                "DataStream error - Can’t process"
                f" element in stream: {item}"
            )
    print("== DataStream statistics ==")
    print(
        f"Numeric Processor: total {len(numeric._storage)}"
        f" items processed, remaining {numeric._rank} on processor\n"
    )

    print("Registering other data processors")
    print("Send the same batch again")
    print("== DataStream statistics ==")
    remaining = len(text._storage)
    total = text._rank
    remaining_log = len(log._storage)
    total_log = log._rank
    n = 0
    while n < 1:
        numeric.output()
        text.output()
        log.output()
        n += 1
    remaining_numeric = len(numeric._storage)
    remaining = len(text._storage)
    remaining_log = len(log._storage)
    text.output()
    remaining_tex = len(text._storage)
    stream_test.process_stream(data)
    print(
        f"Numeric Processor: total {len(numeric._storage)}"
        f" items processed, remaining {numeric._rank} on processor"
    )
    print(
        f"Text Processor: total {remaining} items"
        f" processed, remaining {total} on processor"
    )
    print(
        f"Log Processor: total {remaining_log} items"
        f" processed, remaining {total_log} on processor"
    )
    print(
        "\nConsume some elements from the data processors: "
        f"Numeric {remaining_numeric}, Text {remaining},"
        f" Log {remaining_log}"
    )
    print("== DataStream statistics ==")
    i = 0
    t = 0
    a = 0
    while i < 2:
        numeric.output()
        if t != 2:
            text.output()
            t += 1
        if a == 0:
            log.output()
            a = 1
        i += 1
    print(
        f"Numeric Processor: total {numeric._rank} items processed,"
        f" remaining {len(numeric._storage)} on processor"
    )
    print(
        f"Text Processor: total {total} items processed,"
        f" remaining {remaining_tex} on processor"
    )
    print(
        f"Log Processor: total {total_log} items processed,"
        f" remaining {remaining_log} on processor"
    )
    print()
    stream_test.print_processors_stats()


if __name__ == "__main__":
    main()
