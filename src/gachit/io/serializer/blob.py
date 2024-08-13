from gachit.domain.entity import Blob


class BlobSerializer:
    @classmethod
    def serialize(cls, blob: Blob) -> bytes:
        return blob.data

    @classmethod
    def deserialize(cls, data: bytes) -> Blob:
        return Blob(data)
