from dataclasses import dataclass


class InvalidShaError(Exception):
    pass


@dataclass
class Sha:
    value: str

    def __post_init__(self) -> None:
        self.validate_sha(self.value)

    def validate_sha(self, sha_str: str) -> None:
        if len(sha_str) != 40:
            raise InvalidShaError(f"Invalid sha: {sha_str}")
