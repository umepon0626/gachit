from pathlib import Path

from gachit.domain.entity import Ref, Repository
from gachit.domain.service.commit_tree import get_commit_tree
from gachit.domain.service.diff.tree_to_tree import TreeDiffService
from gachit.domain.service.migrate import (
    MigrationIndexService,
    MigrationWorkspaceService,
)
from gachit.io.index import IndexIO
from gachit.io.ref import BranchIO, HeadIO


def checkout_use_case(branch_name: str, current_dir: Path = Path(".")) -> None:
    repo = Repository(current_dir=current_dir)
    head_io = HeadIO(repo.git_dir)
    branch_io = BranchIO(repo.git_dir)

    current_commit_ref = head_io.read()
    target_commit_ref = branch_io.read(branch_name)

    current_tree = get_commit_tree(repo.git_dir, current_commit_ref.sha)
    target_tree = get_commit_tree(repo.git_dir, target_commit_ref.sha)

    index = IndexIO(repo.git_dir).read()

    tree_diff_service = TreeDiffService(current_tree, target_tree)
    tree_diff_service.compare()

    migration_workspace_service = MigrationWorkspaceService(
        tree_diff_service.diff, repo=repo, index=index
    )
    migration_workspace_service.migrate()

    migration_index_service = MigrationIndexService(
        tree_diff_service.diff, repo=repo, index=index
    )
    migration_index_service.migrate()

    new_branch_ref = Ref(branch_name, current_commit_ref.sha)
    head_io.write(new_branch_ref)
