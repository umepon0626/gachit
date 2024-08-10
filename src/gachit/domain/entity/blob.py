from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Blob:
    format: ClassVar[str] = "blob"
    data: bytes
