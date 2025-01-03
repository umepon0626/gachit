from pathlib import Path

from gachit.domain.entity import Sha, Tree
from gachit.io.database.commit import CommitIO
from gachit.io.database.tree import TreeIO


def get_commit_tree(git_dir: Path, commit_sha: Sha) -> Tree:
    commit_io = CommitIO(git_dir)
    tree_io = TreeIO(git_dir)
    commit = commit_io.get(commit_sha)
    tree = tree_io.get(commit.tree)
    return tree
