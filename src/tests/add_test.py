from pathlib import Path

from gachit.usecase.add import add_use_case
from git import Repo


def test_add() -> None:
    playground_path = Path("/workspace/playground")
    repo = Repo(playground_path)
    repo.git.stash()
    p = playground_path / Path("test.txt")
    with open(p, "w") as f:
        f.write("test\n")

    add_use_case(p, repository_root_dir=playground_path)
    repo.git.commit(str(playground_path), "-n", "-m", "'add test.txt'")
    assert repo.head.commit.tree["test.txt"].data_stream.read() == b"test\n"
