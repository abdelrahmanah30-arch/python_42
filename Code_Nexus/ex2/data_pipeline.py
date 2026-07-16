from abc import ABC, abstractmethod
from typing import Any, Protocol


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

    def output(self) -> tuple[int, str] | None:
        if not self._data:
            return None

        value = self._data.pop(0)

        return (
            self._processed_count,
            self.format_output(value),
        )

    @abstractmethod
    def format_output(self, value: Any) -> str:
        pass

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

    def format_output(self, value: Any) -> str:
        return str(value)


class TextProcessor(DataProcessor):
    def can_process(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> None:
        self._data.append(data)
        self._processed_count += 1

    def format_output(self, value: Any) -> str:
        return value


class LogProcessor(DataProcessor):
    def can_process(self, data: Any) -> bool:
        if not isinstance(data, dict):
            return False

        return (
            "log_level" in data
            and "log_message" in data
        )

    def process(self, data: Any) -> None:
        self._data.append(data)
        self._processed_count += 1

    def format_output(self, value: Any) -> str:
        return (
            f"{value['log_level']}: "
            f"{value['log_message']}"
        )


class ExportPlugin(Protocol):
    def process_output(
        self,
        data: list[tuple[int, str]]
    ) -> None:
        pass


class CSVExportPlugin:
    def process_output(
        self,
        data: list[tuple[int, str]]
    ) -> None:
        values: list[str] = []

        for _, text in data:
            values.append(text)

        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:
    def process_output(
        self,
        data: list[tuple[int, str]]
    ) -> None:
        parts: list[str] = []

        for index, (item_id, text) in enumerate(data):
            part = (
                f"\"item_{item_id - len(data) + index + 1}\": "
                f"\"{text}\""
            )
            parts.append(part)

        print("JSON Output:")
        print("{" + ", ".join(parts) + "}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(
        self,
        proc: DataProcessor
    ) -> None:
        self._processors.append(proc)

    def process_stream(
        self,
        stream: list[Any]
    ) -> None:
        for element in stream:
            self._process_element(element)

    def _process_element(
        self,
        element: Any
    ) -> None:
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
                f"DataStream error - "
                f"Can't process element in stream: "
                f"{element}"
            )

    def output_pipeline(
        self,
        nb: int,
        plugin: ExportPlugin
    ) -> None:
        for processor in self._processors:
            exported: list[tuple[int, str]] = []

            for _ in range(nb):
                item = processor.output()

                if item is None:
                    break

                exported.append(item)

            if exported:
                plugin.process_output(exported)

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return

        for processor in self._processors:
            name = processor.__class__.__name__
            name = name.replace(
                "Processor",
                " Processor"
            )

            print(
                f"{name}: total "
                f"{processor.processed_count} "
                f"items processed, remaining "
                f"{processor.remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")

    stream = DataStream()

    numeric = NumericProcessor()
    text = TextProcessor()
    logs = LogProcessor()

    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(logs)

    batch1 = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message":
                "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message":
                "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]

    stream.process_stream(batch1)

    stream.print_processors_stats()

    print(
        "\nSend 3 processed data "
        "from each processor "
        "to a CSV plugin:"
    )

    stream.output_pipeline(
        3,
        CSVExportPlugin()
    )

    stream.print_processors_stats()

    batch2 = [
        21,
        [
            "I love AI",
            "LLMs are wonderful",
            "Stay healthy",
        ],
        [
            {
                "log_level": "ERROR",
                "log_message":
                "500 server crash",
            },
            {
                "log_level": "NOTICE",
                "log_message":
                "Certificate expires "
                "in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]

    print("\nSend another batch")

    stream.process_stream(batch2)

    stream.print_processors_stats()

    print(
        "\nSend 5 processed data "
        "from each processor "
        "to a JSON plugin:"
    )

    stream.output_pipeline(
        5,
        JSONExportPlugin()
    )

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
