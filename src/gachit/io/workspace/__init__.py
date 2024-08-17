from pathlib import Path

from gachit.domain.entity.error import RepositoryNotFoundError
from gachit.domain.entity.index import IndexEntry
from gachit.domain.entity.sha import Sha


class Workspace:
    root_dir: Path

    def __init__(self, root_dir: Path = Path.cwd()):
        self.root_dir = self.__get_workspace_root(root_dir)

    def __get_workspace_root(self, path: Path) -> Path:
        git_dir = path / ".git"
        if git_dir.exists():
            return path

        parent = path.parent
        if parent == path:
            raise RepositoryNotFoundError("Not a git repository")

        return self.__get_workspace_root(parent)

    def read_file(self, file_path: Path) -> bytes:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if file_path.is_dir():
            raise IsADirectoryError(f"Is a directory: {file_path}")
        with open(file_path, "rb") as f:
            return f.read()

    def create_index_entry(self, file_path: Path, blob_sha: Sha) -> IndexEntry:
        """create index entry with file path and blob sha

        Args:
            file_path (Path): path of file
            blob_sha (Sha): sha of blob
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        relative_path = file_path.relative_to(self.root_dir, walk_up=True)
        stat = file_path.stat()
        ctime_s = int(stat.st_ctime)
        ctime_ns = stat.st_ctime_ns % 10**9
        mtime_s = int(stat.st_mtime)
        mtime_ns = stat.st_mtime_ns % 10**9
        entry = IndexEntry(
            ctime=(ctime_s, ctime_ns),
            mtime=(mtime_s, mtime_ns),
            dev=stat.st_dev,
            ino=stat.st_ino,
            mode_type=0b1000,
            mode_perms=0o644,
            uid=stat.st_uid,
            gid=stat.st_gid,
            fsize=stat.st_size,
            sha=blob_sha,
            flag_assume_valid=False,
            flag_stage=False,
            path=str(relative_path),
        )
        return entry
