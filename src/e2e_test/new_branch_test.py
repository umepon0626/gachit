from pathlib import Path

from gachit.usecase import switch_use_case
from git import Repo


def test_new_branch() -> None:
    playground_path = Path("/workspace/playground")
    repo = Repo(playground_path)
    new_branch_name = "new_branch"
    switch_use_case(branch_name=new_branch_name, repository_root_dir=playground_path)
    assert repo.active_branch.name == new_branch_name
