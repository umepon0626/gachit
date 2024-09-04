from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from .sha import Sha
from .user import User


@dataclass
class Commit:
    """Commit

    Args:
        tree (Sha): Tree SHA
        parent (list[Sha]): Parent commit SHA
        author (User): Author
        created_at (datetime): timestamp when commit is written by author.
        committer (User): Committer
        committed_at (datetime): timestamp when commit is committed by committer.
        message (str): Commit message
    """

    format: ClassVar[str] = "commit"
    tree: Sha
    parents: list[Sha]
    author: User
    created_at: datetime
    committer: User
    committed_at: datetime
    message: str
