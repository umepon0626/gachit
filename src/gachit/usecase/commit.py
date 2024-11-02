import hashlib
from datetime import datetime
from pathlib import Path

from gachit.domain.entity import Commit, Ref, Repository, Sha, Tree
from gachit.domain.service import build_tree_from_index
from gachit.io.database import DataBase, ObjectHeader
from gachit.io.index import IndexIO
from gachit.io.ref import BranchIO, HeadIO
from gachit.io.serializer import CommitSerializer, TreeSerializer
from gachit.io.user import UserIO


def commit_use_case(message: str, repository_root_dir: Path) -> None:
    repo = Repository(repository_root_dir=repository_root_dir)
    db = DataBase(repo.git_dir)
    index_io = IndexIO(repo.git_dir)
    index = index_io.read()

    tree = build_tree_from_index(index, db)
    tree_data = TreeSerializer.serialize(tree)
    tree_sha = Sha(hashlib.sha1(tree_data).hexdigest())
    header = ObjectHeader(Tree, len(tree_data))
    db.write_object(header, tree_data, tree_sha)

    head_io = HeadIO(repo.git_dir)
    head_ref = head_io.read()

    user = UserIO.read()

    commit = Commit(
        tree_sha, [head_ref.sha], user, datetime.now(), user, datetime.now(), message
    )
    commit_data = CommitSerializer.serialize(commit)
    commit_sha = Sha(hashlib.sha1(commit_data).hexdigest())
    commit_header = ObjectHeader(Commit, len(commit_data))
    db.write_object(commit_header, commit_data, commit_sha)

    branch_io = BranchIO(repo.git_dir)
    branch_io.write(ref=Ref(head_ref.name, commit_sha))
