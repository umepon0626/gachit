from gachit.domain.entity import Blob


def deserialize_blob(data: bytes) -> Blob:
    return Blob(data=data)
