from pathlib import Path

from git import Repo

from gachit.usecase.merge import merge_use_case

"""
This test file checks following use case:

(master)     A -> B -> M 
              \      /
(new branch)   C ---・

- `M` is merged commit.
- `A` is the original commit.
"""

playground_path = Path("/workspace/playground")
hoge = playground_path / Path("hoge.txt")
fuga = playground_path / Path("fuga.txt")


def test_basic_merge() -> None:
    repo = Repo(playground_path)

    # Make a commit `A`
    # write `1`` to `hoge.txt` and `fuga.txt`
    with open(hoge, "w") as f:
        f.write("1")
    with open(fuga, "w") as f:
        f.write("1")

    repo.git.add(".")
    repo.git.commit("-m", "Commit A: add hoge.txt and fuga.txt")

    commits = list(repo.iter_commits())
    original_commit_num = len(commits)

    # Make a commit `C`
    # check out to new branch
    new_branch = "new_branch"
    current = repo.create_head(new_branch)
    current.checkout()

    # write `2` to `hoge.txt`
    with open(hoge, "w") as f:
        f.write("2")

    repo.git.add(hoge)
    repo.git.commit("-m", "Commit C: update hoge.txt")

    # Make a commit `B`
    # check out to master branch
    master = repo.heads.master
    master.checkout()

    # write `3` to `fuga.txt`
    with open(fuga, "w") as f:
        f.write("3")

    repo.git.add(fuga)
    repo.git.commit("-m", "Commit B: update fuga.txt")

    # Merge `C` into `B`
    merge_use_case(new_branch, "master", repository_root_dir=playground_path)

    # Check the result
    with open(hoge, "r") as f:
        assert f.read() == "2"
    with open(fuga, "r") as f:
        assert f.read() == "3"
