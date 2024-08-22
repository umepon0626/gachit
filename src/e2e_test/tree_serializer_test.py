from pathlib import Path

from gachit.domain.entity import Mode, Repository, Sha, Tree, TreeLeaf
from gachit.io.database import DataBase
from gachit.io.serializer import TreeSerializer

playground_path = Path("/workspace/playground")


def test_cat_tree() -> None:
    tree_sha = "b0ab15557329cd5f0389548de7117fc79630d52a"
    repo = Repository(repository_root_dir=playground_path)
    db = DataBase(repo.git_dir)
    sha = Sha(tree_sha)
    header, body = db.read_object(sha)

    tree = TreeSerializer.deserialize(body, db)
    assert isinstance(tree, Tree)

    assert len(tree.entries) == 1
    for entry in tree.entries:
        assert isinstance(entry, TreeLeaf)
        assert entry.mode == Mode.FILE

    data_body = TreeSerializer.serialize(tree)
    assert body == data_body
