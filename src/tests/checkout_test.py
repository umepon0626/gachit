from pathlib import Path

import pytest
from gachit.domain.service.migrate import ConflictError
from gachit.usecase.checkout import checkout_use_case
from git import Repo

playground_path = Path("/workspace/playground")
main_py = playground_path / Path("main.py")
test_py = playground_path / Path("test.py")


def setup() -> None:
    new_branch = "new_branch_name"
    repo = Repo(playground_path)
    current = repo.create_head(new_branch)
    current.checkout()

    # delete `main.py` and create new file `test.py`
    main_py.unlink()
    with open(test_py, "w") as f:
        f.write("print('hello, world!')")
    repo.git.add(".")
    repo.git.add(str(test_py))
    repo.git.commit("-m", "add test.py")


def test_checkout_without_conflict() -> None:
    setup()
    original_branch = "master"
    checkout_use_case(original_branch, current_dir=playground_path)
    repo = Repo(playground_path)
    assert repo.active_branch.name == original_branch
    assert not test_py.exists()
    assert main_py.exists()


def test_checkout_with_conflict_workspace() -> None:
    setup()
    with open(main_py, "w") as f:
        f.write("print('This is main.py')")
    original_branch = "master"
    with pytest.raises(ConflictError):
        checkout_use_case(original_branch, current_dir=playground_path)


def test_checkout_with_conflict_index() -> None:
    setup()
    with open(main_py, "w") as f:
        f.write("print('This is main.py')")
    repo = Repo(playground_path)
    repo.git.add(str(main_py))
    original_branch = "master"
    with pytest.raises(ConflictError):
        checkout_use_case(original_branch, current_dir=playground_path)
