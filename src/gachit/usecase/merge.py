from datetime import datetime
from pathlib import Path

from gachit.domain.entity import Commit, Ref, Repository
from gachit.domain.service.build_tree import build_tree_from_index
from gachit.domain.service.commit_tree import get_commit_tree
from gachit.domain.service.common_ancestor import CommonAncestorService
from gachit.domain.service.diff.tree_to_tree import TreeDiffService
from gachit.domain.service.migrate import (
    MigrationIndexService,
    MigrationWorkspaceService,
)
from gachit.io.database.commit import CommitIO
from gachit.io.database.tree import TreeIO
from gachit.io.index import IndexIO
from gachit.io.ref import BranchIO


def merge_use_case(from_branch: str, to_branch: str, repository_root_dir: Path) -> None:
    repo = Repository(repository_root_dir=repository_root_dir)
    branch_io = BranchIO(repo.git_dir)
    commit_io = CommitIO(repo.git_dir)
    tree_io = TreeIO(repo.git_dir)

    from_commit_ref = branch_io.read(from_branch)
    to_commit_ref = branch_io.read(to_branch)

    from_commit = commit_io.get(from_commit_ref.sha)
    to_commit = commit_io.get(to_commit_ref.sha)

    common_ancestor_service = CommonAncestorService(commit_io)
    common_ancestor = common_ancestor_service.find(from_commit, to_commit)
    common_ancestor_tree = tree_io.get(common_ancestor.tree)

    from_tree = get_commit_tree(repo.git_dir, from_commit_ref.sha)

    tree_diff_service = TreeDiffService(common_ancestor_tree, from_tree)
    tree_diff_service.compare()

    migration_workspace_service = MigrationWorkspaceService(
        tree_diff_service.diff, repo=repo
    )
    migration_workspace_service.migrate()

    migration_index_service = MigrationIndexService(tree_diff_service.diff, repo=repo)
    migration_index_service.migrate()

    # create merge commit
    index = IndexIO(repo.git_dir).read()
    tree = build_tree_from_index(index)
    tree_sha = tree_io.write(tree)
    commit = Commit(
        tree_sha,
        [to_commit_ref.sha, from_commit_ref.sha],
        from_commit.author,
        datetime.now(),
        to_commit.author,
        datetime.now(),
        f"Merge {from_branch} into {to_branch}",
    )
    merge_sha = commit_io.write(commit)
    branch_io.write(Ref(to_branch, merge_sha))
