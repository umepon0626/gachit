from enum import StrEnum
from typing import Literal

ObjectType = Literal["blob", "tree", "commit"]


class Mode(StrEnum):
    FILE = "100644"
    EXECUTABLE = "100755"
    DIRECTORY = "40000"
    SYMLINK = "120000"
    SUBMODULE = "160000"

    @property
    def object_type(self) -> ObjectType:
        return "blob" if self in {Mode.FILE, Mode.EXECUTABLE} else "tree"
