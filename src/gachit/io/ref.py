from pathlib import Path

from gachit.domain.entity import Ref, Sha


class BranchIO:
    def __init__(self, git_dir: Path):
        self.refs_dir = git_dir / "refs" / "heads"

    def read(self, name: str) -> Ref:
        ref_path = self.refs_dir / name
        if not ref_path.exists():
            raise FileNotFoundError(f"Ref {name} does not exist.")
        with ref_path.open("r") as f:
            sha = Sha(f.read().strip())
        return Ref(name, sha)

    def write(self, ref: Ref) -> None:
        ref_path = self.refs_dir / ref.name
        with ref_path.open("w+") as f:
            f.write(ref.sha.value + "\n")


class HeadIO:
    def __init__(self, git_dir: Path):
        self.head_file_path = git_dir / "HEAD"
        self.ref_io = BranchIO(git_dir)

    def read(self) -> Ref:
        with self.head_file_path.open("r") as f:
            parse_result = f.read().split("heads/")
            if len(parse_result) != 2:
                raise ValueError("HEAD file is not well formatted.")
            ref_name = parse_result[1].strip()
            return self.ref_io.read(ref_name)

    def write(self, ref: Ref) -> None:
        with self.head_file_path.open("w") as f:
            f.write(f"ref: refs/heads/{ref.name}\n")
