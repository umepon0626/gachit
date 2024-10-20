from dataclasses import dataclass

from .sha import Sha


@dataclass(frozen=True)
class Ref:
    name: str
    sha: Sha
