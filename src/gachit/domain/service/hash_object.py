import hashlib

from gachit.domain.entity import Blob, Sha, Tree
from gachit.io.database import ObjectHeader
from gachit.io.serializer import BlobSerializer, TreeSerializer


def hash_object_service(data: Blob | Tree) -> Sha:
    if isinstance(data, Blob):
        header = ObjectHeader(Blob, len(data.data))
        written_data = header.value + BlobSerializer.serialize(data)
    elif isinstance(data, Tree):
        data_body = TreeSerializer.serialize(data)
        header = ObjectHeader(Tree, len(data_body))
        written_data = header.value + data_body
    sha = Sha(hashlib.sha1(written_data).hexdigest())
    return sha
