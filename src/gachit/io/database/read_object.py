import zlib
from pathlib import Path

from .error import InvalidObjectFormatError
from .object_header import ObjectHeader


def read_object(file_path: Path) -> tuple[ObjectHeader, bytes]:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "rb") as f:
        raw = zlib.decompress(f.read())

    null_byte_end = raw.find(b"\x00")
    header = ObjectHeader.from_data(raw[: null_byte_end + 1])

    if header.content_size != len(raw) - null_byte_end - 1:
        raise InvalidObjectFormatError(f"Malformed object {file_path}")

    return header, raw[null_byte_end + 1 :]
