from pathlib import Path

from gachit.domain.entity import Mode, Repository, Sha, Tree, TreeLeaf
from gachit.io.database import DataBase
from gachit.io.serializer import TreeSerializer

playground_path = Path("/workspace/playground")


def test_tree_serializer() -> None:
    tree_sha = "2cf65514b868b8cc830dd82f26dbf97db5f56eea"
    repo = Repository(repository_root_dir=playground_path)
    db = DataBase(repo.git_dir)
    sha = Sha(tree_sha)
    header, body = db.read_object(sha)

    tree = TreeSerializer.deserialize(body, db)
    assert isinstance(tree, Tree)

    assert len(tree.entries) == 2
    for entry in tree.entries:
        assert isinstance(entry, TreeLeaf)
        assert entry.mode == Mode.FILE

    data_body = TreeSerializer.serialize(tree)

    assert body == data_body
