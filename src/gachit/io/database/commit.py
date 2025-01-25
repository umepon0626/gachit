from pathlib import Path

from gachit.domain.entity import Commit, Sha
from gachit.io.serializer import CommitSerializer

from .db import DataBase
from .object_header import ObjectHeader


class CommitIO:
    def __init__(self, git_dir: Path) -> None:
        self.db = DataBase(git_dir)

    def get(self, sha: Sha) -> Commit:
        header, data = self.db.read_object(sha)
        if header.object_type != Commit:
            raise ValueError(f"Object type is not Commit: {header.object_type}")
        return CommitSerializer.deserialize(data)

    def write(self, commit: Commit) -> Sha:
        commit_data = CommitSerializer.serialize(commit)
        commit_header = ObjectHeader(Commit, len(commit_data))
        return self.db.write_object(commit_header, commit_data)
