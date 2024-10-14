from dataclasses import dataclass

from .sha import Sha


@dataclass
class IndexEntry:
    """Index entry

    Args:
        ctime (tuple[int, int]): Creation time
        mtime (tuple[int, int]): Modification time
        dev (int): Device
        ino (int): Inode
        mode_type (int): Mode type
        mode_perms (int): Mode permissions
        uid (int): User ID
        gid (int): Group ID
        fsize (int): File size
        sha (Sha): SHA
        flag_assume_valid (bool): Assume valid flag
        flag_stage (bool): Stage flag
        path (str): relative file path string to workspace root
    """

    ctime: tuple[int, int]
    mtime: tuple[int, int]
    dev: int
    ino: int
    mode_type: int
    mode_perms: int
    uid: int
    gid: int
    fsize: int
    sha: Sha
    flag_assume_valid: bool
    flag_stage: bool
    path: str


@dataclass
class Index:
    """Index

    Args:
        entries (list[IndexEntry]): Index entries.
        version (int): Version, defaults to 2
    """

    entries: list[IndexEntry]
    version: int = 2

    def remove_entry(self, path: str) -> None:
        """Remove entry by path

        Args:
            path (str): relative file path string to workspace root
        """
        self.entries = [e for e in self.entries if e.path != path]

    def find_entry(self, path: str) -> IndexEntry | None:
        for e in self.entries:
            if e.path == path:
                return e
        return None
