from pathlib import Path

from gachit.domain.entity import Repository
from gachit.io.database.blob import BlobIO
from gachit.io.index import IndexIO
from gachit.io.serializer import BlobSerializer
from gachit.io.workspace import Workspace


def add_use_case(path: Path, repository_root_dir: Path = Path(".")) -> None:
    repo = Repository(repository_root_dir=repository_root_dir)
    workspace = Workspace(repo.repository_root_dir)
    index_io = IndexIO(repo.git_dir)
    blob_io = BlobIO(repo.git_dir)

    # save the file content as a blob
    file_content = workspace.read_file(path)
    blob = BlobSerializer.deserialize(file_content)
    sha = blob_io.write(blob)

    # Load Index from index file
    index = index_io.read()
    # build index entry
    index_entry = workspace.create_index_entry(path, sha)
    # Add index entry to index
    index.add_or_update_entry(index_entry)
    # save index to index file
    index_io.write(index)
