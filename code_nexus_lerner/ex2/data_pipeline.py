from abc import ABC, abstractmethod
from typing import Any
from typing import Protocol
import typing


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage:  list[tuple[int, str]] = []
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

        ran, value = self._storage.pop(0)
        return ran, value


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, int | float):
            return True
        if isinstance(data, list):
            return all(isinstance(item, int | float) for item in data)

        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise Exception("Invalid numeric data")
        if isinstance(data, int | float):
            self._rank += 1
            self._storage.append((self._rank, str(data)))
        elif isinstance(data, list):
            for item in data:
                if not isinstance(item, int | float):
                    raise Exception("Invalid numeric data")

                self._rank += 1
                self._storage.append((self._rank, str(item)))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
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
        if isinstance(data, list):
            return all(
                isinstance(item, dict) and
                all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in item.items()
                )
                for item in data
            )
        return False

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if isinstance(data, dict):
            if not self.validate(data):
                raise ValueError("Invalid log data")
            self._rank += 1
            self._storage.append(
                (self._rank, self._format_log(data))
            )
        elif isinstance(data, list):
            for item in data:
                if not self.validate(item):
                    raise ValueError("Invalid log data in list")
                self._rank += 1
                self._storage.append(
                    (self._rank, self._format_log(item))
                )
        else:
            raise ValueError("Invalid log data type")

    def _format_log(self, log: dict[str, str]) -> str:
        return ": ".join(f"{v}" for k, v in log.items())


class DataStream():
    def __init__(self) -> None:
        self.processor: list[typing.Any] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processor.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        if not stream:
            print("No processor found, no data")
            return

        for item in stream:
            if not any(process.validate(item) for process in self.processor):
                print("No processor can handle item")
                continue

            for process in self.processor:
                if process.validate(item):
                    process.ingest(item)
                    break

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:

        for processor in self.processor:

            collected = []

            i = 0
            while i < nb:
                collected.append(processor.output())
                i += 1

            plugin.process_output(collected)


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class JSONPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        result = "JSON Output:\n{"

        length = len(data)

        for i, (rank, value) in enumerate(data):
            result += f'"item_{rank}": "{value}"'

            if i < length - 1:
                result += ", "

        result += "}"

        print(result)


class CSVPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        result = "CSV Output:\n"

        values = []
        for rank, value in data:
            values.append(str(value))

        result += ",".join(values)

        print(result)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")
    print("Initialize Data Stream...\n")
    print("== DataStream statistics ==")

    stream = DataStream()

    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())
    empty: list[typing.Any] = []
    stream.process_stream(empty)
    data1 = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead"
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected"
            }
        ],
        42,
        ["Hi", "five"]
    ]

    print("\nRegistering Processors")
    print("Send first batch of data on stream:", data1)

    stream.process_stream(data1)

    print("\n== DataStream statistics ==")
    for p in stream.processor:
        print(
            f"{p.__class__.__name__}: "
            f"total {p._rank} items processed, "
            f"remaining {len(p._storage)} on processor"
        )

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    csv_plugin = CSVPlugin()
    stream.output_pipeline(3, csv_plugin)

    print("\n== DataStream statistics ==")
    for p in stream.processor:
        print(
            f"{p.__class__.__name__}: "
            f"total {p._rank} items processed, "
            f"remaining {len(p._storage)} on processor"
        )

    # second batch
    data2 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days"
            }
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]

    print(f"\nSend another batch of data: {data2}")

    stream.process_stream(data2)

    print("\n== DataStream statistics ==")
    for p in stream.processor:
        print(
            f"{p.__class__.__name__}: "
            f"total {p._rank} items processed, "
            f"remaining {len(p._storage)} on processor"
        )

    # JSON export phase
    print("\nSend 5 processed data from each processor to a JSON plugin:")
    json_plugin = JSONPlugin()
    stream.output_pipeline(5, json_plugin)

    print("\n== DataStream statistics ==")
    for p in stream.processor:
        print(
            f"{p.__class__.__name__}: "
            f"total {p._rank} items processed, "
            f"remaining {len(p._storage)} on processor"
        )


if __name__ == "__main__":
    main()
