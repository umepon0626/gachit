from dataclasses import dataclass


@dataclass(frozen=True)
class Sha:
    value: str

    def __post_init__(self) -> None:
        self.__validate_sha(self.value)

    def __validate_sha(self, sha_str: str) -> None:
        if len(sha_str) != 40:
            raise ValueError(f"Invalid sha: {sha_str}")
