from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Blob:
    format: ClassVar[str] = "blob"
    data: bytes
