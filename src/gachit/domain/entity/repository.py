from pathlib import Path

from .error import RepositoryNotFoundError


class Repository:
    repository_root_dir: Path
    git_dir: Path

    def __init__(self, repository_root_dir: Path = Path.cwd()):
        self.repository_root_dir = self.__get_repository_root(repository_root_dir)
        self.git_dir = self.repository_root_dir / ".git"

    def __get_repository_root(self, path: Path) -> Path:
        git_dir = path / ".git"
        if git_dir.exists():
            return path

        parent = path.parent
        if parent == path:
            raise RepositoryNotFoundError("Not a git repository")

        return self.__get_repository_root(parent)
