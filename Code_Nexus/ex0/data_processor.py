from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data available")

    return self._storage.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list):
            return all(
                isinstance(item, (int, float))
                for item in data
            )

        return False

    def ingest(
        self,
        data: int | float | list[int | float]
    ) -> None:
        if isinstance(data, list):
            for item in data:
                self._rank += 1
                self._storage.append(
                    (self._rank, str(item))
            )
        else:
            self._rank += 1
            self._storage.append(
                (self._rank, str(data)
        )
    )


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(
                isinstance(item, str)
                for item in data
            )

        return False

    def ingest(
        self,
        data: str | list[str]
    ) -> None:
        if isinstance(data, list):
    for item in data:
        self._rank += 1
        self._storage.append(
            (self._rank, item)
        )
    else:
        self._rank += 1
        self._storage.append(
            (self._rank, data)
    )


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(key, str)
                and isinstance(value, str)
                for key, value in data.items()
            )

        if isinstance(data, list):
            return all(
                isinstance(item, dict)
                and all(
                    isinstance(key, str)
                    and isinstance(value, str)
                    for key, value in item.items()
                )
                for item in data
            )

        return False

    def ingest(
        self,
        data: dict[str, str]
        | list[dict[str, str]]
    ) -> None:
       self._rank += 1
    self._storage.append(
        (
            self._rank,
            self._format_log(item)
    )
    )

    def _format_log(
        self,
        log: dict[str, str]
    ) -> str:
        level = log.get(
            "log_level",
            ""
        )
        message = log.get(
            "log_message",
            ""
        )
        return f"{level}: {message}"


def main() -> None:
    print(
        "=== Code Nexus "
        "- Data Processor ==="
    )

    print(
        "\nTesting Numeric Processor..."
    )
    numeric = NumericProcessor()

    print(
        "Trying to validate input "
        "'42': "
        f"{numeric.validate(42)}"
    )

    print(
        "Trying to validate input "
        "'Hello': "
        f"{numeric.validate('Hello')}"
    )

    print(
        "Test invalid ingestion "
        "of string 'foo' "
        "without prior validation:"
    )


    try:
        numeric.ingest("foo")
    except ValueError as exc:
        print(
            f"Got exception: {exc}"
        )

    data_num: list[int | float] = [
        1,
        2,
        3,
        4,
        5,
    ]

    print(
        f"Processing data: {data_num}"
    )
    numeric.ingest(data_num)

    print(
        "Extracting 3 values..."
    )

    for _ in range(3):
        rank, value = numeric.output()
        print(
            f"Numeric value "
            f"{rank}: {value}"
        )

    print(
        "\nTesting Text Processor..."
    )
    text = TextProcessor()

    print(
        "Trying to validate input "
        "'42': "
        f"{text.validate(42)}"
    )

    data_text: list[str] = [
        "Hello",
        "Nexus",
        "World",
    ]

    print(
        f"Processing data: "
        f"{data_text}"
    )

    text.ingest(data_text)

    print(
        "Extracting 1 value..."
    )

    rank, value = text.output()

    print(
        f"Text value "
        f"{rank}: {value}"
    )

    print(
        "\nTesting Log Processor..."
    )

    logs = LogProcessor()

    print(
        "Trying to validate input "
        "'Hello': "
        f"{logs.validate('Hello')}"
    )

    log_data: list[
        dict[str, str]
    ] = [
        {
            "log_level": "NOTICE",
            "log_message":
                "Connection to server",
        },
        {
            "log_level": "ERROR",
            "log_message":
                "Unauthorized access!!",
        },
    ]

    print(
        f"Processing data: "
        f"{log_data}"
    )

    logs.ingest(log_data)

    print(
        "Extracting 2 values..."
    )

    for _ in range(2):
        rank, value = logs.output()
        print(
            f"Log entry "
            f"{rank}: {value}"
        )


if __name__ == "__main__":
    main()
