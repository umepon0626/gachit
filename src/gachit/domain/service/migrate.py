from dataclasses import dataclass

from gachit.domain.entity import Blob, Repository, TreeDiff
from gachit.domain.entity.diff import DiffType
from gachit.domain.service.diff import (
    IndexToTreeDiffService,
    WorkspaceToIndexDiffService,
)
from gachit.io.database import DataBase
from gachit.io.index import IndexIO
from gachit.io.serializer import BlobSerializer
from gachit.io.workspace import Workspace


class ConflictError(Exception):
    pass


@dataclass
class MigrationService:
    # TODO: Separate this class into two classes:
    # MigrateWorkspaceService and MigrationIndexService ?
    diff: TreeDiff
    repo: Repository

    def __post_init__(self) -> None:
        self.workspace = Workspace(self.repo.git_dir.parent)
        self.database = DataBase(self.repo.git_dir)
        self.index_io = IndexIO(self.repo.git_dir)
        self.index = self.index_io.read()

    def check_conflicts(self) -> None:
        index = self.index_io.read()

        workspace_to_index_diff_service = WorkspaceToIndexDiffService(
            self.workspace, index
        )
        index_to_tree_diff_service = IndexToTreeDiffService(index, self.diff.before)

        for path in self.diff.blob_diffs.keys():
            conflict_between_workspace_and_index = (
                workspace_to_index_diff_service.check_one(path)
            )
            if (
                conflict_between_workspace_and_index
                and conflict_between_workspace_and_index != DiffType.NO_CHANGE
            ):
                raise ConflictError(f"Conflict between workspace and index: {path}")

            conflict_between_index_and_tree = index_to_tree_diff_service.check_one(path)

            if (
                conflict_between_index_and_tree
                and conflict_between_index_and_tree != DiffType.NO_CHANGE
            ):
                raise ConflictError(
                    f"Conflict ({conflict_between_index_and_tree}) "
                    f"between index and tree: {path}"
                )

    def update_workspace(self) -> None:
        for path, blob_diff in self.diff.blob_diffs.items():
            if blob_diff.after is None:
                self.workspace.delete_file(path)
            else:
                header, data = self.database.read_object(blob_diff.after)
                if header.object_type != Blob:
                    self.rollback_workspace()
                    print(f"Expected blob, got {header}. Rollback applied.")
                updated_file_content = BlobSerializer.deserialize(data).data
                self.workspace.write_file(path, updated_file_content, exist_ok=True)

    def update_index(self) -> None:
        for path, blob_diff in self.diff.blob_diffs.items():
            if blob_diff.after is None:
                self.index.remove_entry(str(path))
            else:
                index_entry = self.workspace.create_index_entry(path, blob_diff.after)
                self.index.entries.append(index_entry)
        self.index_io.write(self.index)

    def rollback_workspace(self) -> None:
        for path, blob_diff in self.diff.blob_diffs.items():
            if blob_diff.before is None:
                self.workspace.delete_file(path)
            else:
                header, data = self.database.read_object(blob_diff.before)
                if header.object_type != Blob:
                    continue
                original_file_content = BlobSerializer.deserialize(data).data
                self.workspace.write_file(path, original_file_content, exist_ok=True)

    def migrate(self) -> None:
        self.check_conflicts()
        self.update_workspace()
        self.update_index()
