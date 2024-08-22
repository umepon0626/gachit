from enum import StrEnum


class Mode(StrEnum):
    FILE = "100644"
    EXECUTABLE = "100755"
    DIRECTORY = "040000"
    SYMLINK = "120000"
    SUBMODULE = "160000"
