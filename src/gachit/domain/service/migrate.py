from dataclasses import dataclass

from gachit.domain.entity import DiffType, Repository, TreeDiff
from gachit.domain.service.diff import (
    IndexToTreeDiffService,
    WorkspaceToIndexDiffService,
)
from gachit.io.database.blob import BlobIO
from gachit.io.index import IndexIO
from gachit.io.workspace import Workspace


class ConflictError(Exception):
    pass


@dataclass
class MigrationWorkspaceService:
    diff: TreeDiff
    repo: Repository

    def __post_init__(self) -> None:
        self.workspace = Workspace(self.repo.git_dir.parent)
        self.blob_io = BlobIO(self.repo.git_dir)
        self.index_io = IndexIO(self.repo.git_dir)

    def check_conflicts(self) -> None:
        index = self.index_io.read()

        workspace_to_index_diff_service = WorkspaceToIndexDiffService(
            self.workspace, index
        )

        for path in self.diff.blob_diffs.keys():
            conflict_between_workspace_and_index = (
                workspace_to_index_diff_service.check_one(path)
            )
            if (
                conflict_between_workspace_and_index
                and conflict_between_workspace_and_index != DiffType.NO_CHANGE
            ):
                raise ConflictError(f"Conflict between workspace and index: {path}")

    def update_workspace(self) -> None:
        for path, blob_diff in self.diff.blob_diffs.items():
            if blob_diff.after is None:
                self.workspace.delete_file(path)
            else:
                blob = self.blob_io.get(blob_diff.after)
                updated_file_content = blob.data
                self.workspace.write_file(path, updated_file_content, exist_ok=True)

    def migrate(self) -> None:
        self.check_conflicts()
        self.update_workspace()


@dataclass
class MigrationIndexService:
    diff: TreeDiff
    repo: Repository

    def __post_init__(self) -> None:
        self.workspace = Workspace(self.repo.git_dir.parent)
        self.index_io = IndexIO(self.repo.git_dir)
        self.index = self.index_io.read()

    def check_conflicts(self) -> None:
        index_to_tree_diff_service = IndexToTreeDiffService(
            self.index, self.diff.before
        )

        for path in self.diff.blob_diffs.keys():
            conflict_between_index_and_tree = index_to_tree_diff_service.check_one(path)

            if (
                conflict_between_index_and_tree
                and conflict_between_index_and_tree != DiffType.NO_CHANGE
            ):
                raise ConflictError(
                    f"Conflict ({conflict_between_index_and_tree}) "
                    f"between index and tree: {path}"
                )

    def update_index(self) -> None:
        for path, blob_diff in self.diff.blob_diffs.items():
            if blob_diff.after is None:
                self.index.remove_entry(path)
            else:
                index_entry = self.workspace.create_index_entry(path, blob_diff.after)
                self.index.add_or_update_entry(index_entry)

        self.index_io.write(self.index)

    def migrate(self) -> None:
        self.check_conflicts()
        self.update_index()
