from pathlib import Path


class Repository:
    repository_root_dir: Path
    git_dir: Path

    def __init__(self, current_dir: Path = Path.cwd()):
        self.repository_root_dir = self.__get_repository_root(current_dir)
        self.git_dir = self.repository_root_dir / ".git"

    def __get_repository_root(self, path: Path) -> Path:
        """Find the root of the git repository

        Args:
            path (Path): path to start searching

        Raises:
            FileNotFoundError: if the root of the git repository is not found

        Returns:
            Path: root of the git repository
        """

        # check if the path is a git repository
        git_dir = path / ".git"
        if git_dir.exists():
            return path

        # check if the path is the root of the filesystem
        parent = path.parent
        is_root = parent == path
        if is_root:
            raise FileNotFoundError("Not a git repository")

        # search the parent directory recursively
        return self.__get_repository_root(parent)
