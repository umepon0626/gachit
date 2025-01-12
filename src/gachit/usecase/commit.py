from datetime import datetime
from pathlib import Path

from gachit.domain.entity import Commit, Ref, Repository
from gachit.domain.service import build_tree_from_index
from gachit.io.database.commit import CommitIO
from gachit.io.database.tree import TreeIO
from gachit.io.index import IndexIO
from gachit.io.ref import BranchIO, HeadIO
from gachit.io.user import UserIO


def commit_use_case(message: str, current_dir: Path) -> None:
    repo = Repository(current_dir=current_dir)
    commit_io = CommitIO(repo.git_dir)
    tree_io = TreeIO(repo.git_dir)
    index_io = IndexIO(repo.git_dir)
    index = index_io.read()

    tree = build_tree_from_index(index)
    tree_sha = tree_io.write(tree)

    head_io = HeadIO(repo.git_dir)
    head_ref = head_io.read()

    user = UserIO.read()

    commit = Commit(
        tree_sha, [head_ref.sha], user, datetime.now(), user, datetime.now(), message
    )
    commit_sha = commit_io.write(commit)

    branch_io = BranchIO(repo.git_dir)
    branch_io.write(ref=Ref(head_ref.name, commit_sha))
