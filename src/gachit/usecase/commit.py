import hashlib

from gachit.domain.entity import Repository, Sha, Tree
from gachit.domain.service import build_tree_from_index
from gachit.io.database import DataBase
from gachit.io.database.object_header import ObjectHeader
from gachit.io.index import IndexIO
from gachit.io.serializer import TreeSerializer


def commit_usecase(message: str) -> None:
    repo = Repository()
    db = DataBase(repo.git_dir)
    index_io = IndexIO(repo.git_dir)
    index = index_io.read()

    tree = build_tree_from_index(index, db)
    tree_data = TreeSerializer.serialize(tree)
    tree_sha = Sha(hashlib.sha1(tree_data).hexdigest())
    header = ObjectHeader(Tree, len(tree_data))
    db.write_object(header, tree_data, tree_sha)

    # TODO: get HEAD sha
    # TODO: get USER data.

    # commit = Commit(tree_sha, [Sha("")], User(), User(), message)
    # commit_data = CommitSerializer.serialize(commit)
    # commit_sha = Sha(hashlib.sha1(commit_data).hexdigest())
    # commit_header = ObjectHeader(Commit, len(commit_data))
    # db.write_object(commit_header, commit_data, commit_sha)

    # TODO: update HEAD sha
