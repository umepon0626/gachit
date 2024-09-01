from pathlib import Path

from gachit.domain.entity import Ref, Repository
from gachit.io.ref import BranchIO, HeadIO


def switch_use_case(branch_name: str, repository_root_dir: Path = Path(".")) -> None:
    repo = Repository(repository_root_dir=repository_root_dir)
    head_io = HeadIO(repo.git_dir)
    branch_io = BranchIO(repo.git_dir)

    current_ref = head_io.read()
    new_branch_ref = Ref(branch_name, current_ref.sha)
    branch_io.write(new_branch_ref)
    head_io.write(new_branch_ref)
