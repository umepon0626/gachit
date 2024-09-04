from pathlib import Path

from gachit.usecase import commit_use_case
from git import Repo


def test_commit() -> None:
    playground_path = Path("/workspace/playground")
    config_path = Path.home() / ".gitconfig"
    with open(config_path, "w") as f:
        f.writelines(["[user]\n", "\temail = test@example.com\n", "\tname = test\n"])

    repo = Repo(playground_path)
    repo.git.stash()
    p = playground_path / Path("test.txt")
    with open(p, "w") as f:
        f.write("test\n")

    repo.git.add(str(p))
    commit_use_case("add test.txt", repository_root_dir=playground_path)

    # assert repo.head.commit.tree["test.txt"].data_stream.read() == b"test\n"
