from pathlib import Path

from gachit.domain.entity import Blob, Repository
from gachit.domain.service.hash_object import hash_object_service
from gachit.io.database import DataBase
from gachit.io.database.object_header import ObjectHeader
from gachit.io.index import IndexIO
from gachit.io.serializer import BlobSerializer
from gachit.io.workspace import Workspace


def add_use_case(path: Path, repository_root_dir: Path = Path(".")) -> None:
    repo = Repository(repository_root_dir=repository_root_dir)
    db = DataBase(repo.git_dir)
    workspace = Workspace(repo.repository_root_dir)
    index_io = IndexIO(repo.git_dir)

    # save the file content as a blob
    file_content = workspace.read_file(path)
    blob = BlobSerializer.deserialize(file_content)
    sha = hash_object_service(blob)
    header = ObjectHeader(Blob, len(file_content))
    db.write_object(header, file_content, sha, exist_ok=True)

    # Load Index from index file
    index = index_io.read()
    # build index entry
    index_entry = workspace.create_index_entry(path, sha)
    # Add index entry to index
    index.entries.append(index_entry)
    # save index to index file
    index_io.write(index)
