from abc import ABC, abstractmethod
from typing import Any


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
            raise Exception("Invalid numeric data")

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


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    num = 42
    print(f"Trying to validate input ’42’: {numeric.validate(num)}")
    hel = "hello"
    print(f"Trying to validate input ’Hello’: {numeric.validate(hel)}")
    foo = "foo"
    print(
        f"Test invalid ingestion of string ’{foo}’"
        " without prior validation:"
    )
    try:
        numeric.ingest(foo)
    except Exception as error:
        print(f"Got exception: {error}")
    lis = [1, 2, 3, 4, 5]
    i = 0
    print(f"Processing data: {list(lis)}")
    print("Extracting 3 values...")
    numeric.ingest(lis)
    key, value_num = numeric.output()
    i = 0
    while i < 3:
        print(f"Numeric value {i}: {value_num}")
        key, value_num = numeric.output()
        i += 1
    print("\nTesting Text Processor...")
    text = TextProcessor()
    num = 42
    text_list = ["Hello", "Nexus", "World"]
    print(f"Trying to validate input ’{num}’: {text.validate(num)}")
    text.ingest(text_list)
    rank_text, value_text = text.output()
    print(f"Processing data: {text_list}")
    print("Extracting 1 value...")
    print(f"Text value {rank_text - 1}: {value_text}\n")

    print("Testing Log Processor...")
    hel_log = "hello"
    leg = LogProcessor()
    data_process = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"}
    ]
    print(f"Trying to validate input ’{hel_log}’: {leg.validate(hel_log)}")
    print(f"Processing data: {data_process}")
    print("Extracting 2 values...")
    leg.ingest(data_process)
    rank, value = leg.output()
    print(f"Log entry {rank - 1}: {value}")
    rank, value = leg.output()
    print(f"Log entry {rank - 1}: {value}")


if __name__ == "__main__":
    main()
