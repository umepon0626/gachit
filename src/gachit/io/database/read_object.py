import zlib
from pathlib import Path

from gachit.domain.entity import Blob, Tree
from gachit.io.database.tree import deserialize_tree

from .error import InvalidObjectFormatError, InvalidObjectTypeError

GitObjectTypes = Blob | Tree
GitObjectFormats = {Blob: Blob.format, Tree: Tree.format}


def read_object(
    file_path: Path, object_type: type[GitObjectTypes] | None = None
) -> GitObjectTypes:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "rb") as f:
        raw = zlib.decompress(f.read())

    header_end = raw.find(b" ")
    object_format = raw[:header_end].decode("ascii")
    null_byte_end = raw.find(b"\x00", header_end)
    content_size = int(raw[header_end:null_byte_end].decode("ascii"))

    if content_size != len(raw) - null_byte_end - 1:
        raise InvalidObjectFormatError(f"Malformed object {file_path}")

    if (object_type is not None) and (GitObjectFormats[object_type] != object_format):
        raise InvalidObjectTypeError(
            f"Expected object type {object_type}, but got {object_format}"
        )

    match object_format:
        case Blob.format:
            return Blob(raw[null_byte_end + 1 :])
        case Tree.format:
            return deserialize_tree(raw[null_byte_end + 1 :])
        case _:
            raise InvalidObjectTypeError(f"Unknown object type: {object_format}")
