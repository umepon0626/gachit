from pathlib import Path

from gachit.domain.entity import Ref, Repository, Sha, Tree
from gachit.domain.service.diff.tree_to_tree import TreeDiffService
from gachit.domain.service.migrate import MigrationService
from gachit.io.database.commit import CommitIO
from gachit.io.database.tree import TreeIO
from gachit.io.ref import BranchIO, HeadIO


def get_commit_tree(git_dir: Path, commit_sha: Sha) -> Tree:
    commit_io = CommitIO(git_dir)
    tree_io = TreeIO(git_dir)
    commit = commit_io.get(commit_sha)
    tree = tree_io.get(commit.tree)
    return tree


def checkout_use_case(branch_name: str, repository_root_dir: Path = Path(".")) -> None:
    repo = Repository(repository_root_dir=repository_root_dir)
    head_io = HeadIO(repo.git_dir)

    branch_io = BranchIO(repo.git_dir)

    current_commit_ref = head_io.read()
    target_commit_ref = branch_io.read(branch_name)

    current_tree = get_commit_tree(repo.git_dir, current_commit_ref.sha)
    target_tree = get_commit_tree(repo.git_dir, target_commit_ref.sha)

    tree_diff_service = TreeDiffService(current_tree, target_tree)
    tree_diff_service.compare()

    migration_service = MigrationService(tree_diff_service.diff, repo=repo)
    migration_service.migrate()

    new_branch_ref = Ref(branch_name, current_commit_ref.sha)
    head_io.write(new_branch_ref)
