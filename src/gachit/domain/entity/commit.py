from dataclasses import dataclass
from typing import ClassVar

from .sha import Sha
from .user import User


@dataclass
class Commit:
    """Commit

    Args:
        tree (Sha): Tree SHA
        parent (list[Sha]): Parent commit SHA
        authors (User): Author
        committers (User): Committer
        message (str): Commit message
    """

    format: ClassVar[str] = "commit"
    tree: Sha
    parents: list[Sha]
    author: User
    committer: User
    message: str
