from pathlib import Path

from gachit.domain.entity import Commit, Ref, Repository, Sha, Tree
from gachit.domain.service.diff.tree_to_tree import TreeDiffService
from gachit.domain.service.migrate import MigrationService
from gachit.io.database import DataBase
from gachit.io.ref import BranchIO, HeadIO
from gachit.io.serializer import CommitSerializer, TreeSerializer


def get_commit_tree(db: DataBase, commit_sha: Sha) -> Tree:
    header, data = db.read_object(commit_sha)
    if header.object_type != Commit:
        raise ValueError(f"Invalid object type: {header.object_type}")
    commit = CommitSerializer.deserialize(data)
    header, data = db.read_object(commit.tree)
    if header.object_type != Tree:
        raise ValueError(f"Invalid object type: {header.object_type}")
    tree = TreeSerializer.deserialize(data, db)
    return tree


def checkout_use_case(branch_name: str, repository_root_dir: Path = Path(".")) -> None:
    repo = Repository(repository_root_dir=repository_root_dir)
    head_io = HeadIO(repo.git_dir)
    db = DataBase(repo.git_dir)
    branch_io = BranchIO(repo.git_dir)

    current_commit_ref = head_io.read()
    target_commit_ref = branch_io.read(branch_name)

    current_tree = get_commit_tree(db, current_commit_ref.sha)
    target_tree = get_commit_tree(db, target_commit_ref.sha)

    tree_diff_service = TreeDiffService(current_tree, target_tree)
    tree_diff_service.compare()

    migration_service = MigrationService(tree_diff_service.diff, repo=repo)
    migration_service.migrate()

    new_branch_ref = Ref(branch_name, current_commit_ref.sha)
    head_io.write(new_branch_ref)
