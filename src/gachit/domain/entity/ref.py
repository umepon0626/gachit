from dataclasses import dataclass

from .sha import Sha


@dataclass
class Ref:
    name: str
    sha: Sha
