from pathlib import Path

from gachit.domain.entity import Index
from gachit.domain.entity.diff import DiffType
from gachit.domain.service.hash_object import hash_object_service
from gachit.io.serializer import BlobSerializer
from gachit.io.workspace import Workspace


class WorkspaceToIndexDiffService:
    def __init__(self, workspace: Workspace, index: Index) -> None:
        self.workspace = workspace
        self.index = index

    def check_one(self, full_path: Path) -> DiffType | None:
        index_entry = self.index.find_entry(full_path)
        try:
            data = self.workspace.read_file(full_path)
            blob = BlobSerializer.deserialize(data)
            sha = hash_object_service(blob)
        except FileNotFoundError:
            if index_entry is None:
                return None
            return DiffType.DELETED

        if index_entry is None:
            return DiffType.UNTRACKED

        if index_entry.sha != sha:
            return DiffType.MODIFIED

        return DiffType.NO_CHANGE
