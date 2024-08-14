import zlib
from pathlib import Path

from gachit.domain.entity import Sha

from .object_header import ObjectHeader


def write_object(
    header: ObjectHeader,
    body: bytes,
    sha: Sha,
    git_object_dir: Path,
    exist_ok: bool = True,
) -> None:
    object_path = git_object_dir / sha.value[:2] / sha.value[2:]
    if not exist_ok and object_path.exists():
        raise FileExistsError(f"Object already exists: {object_path}")
    object_path.parent.mkdir(parents=True, exist_ok=True)
    object_path.write_bytes(zlib.compress(header.value + body))
