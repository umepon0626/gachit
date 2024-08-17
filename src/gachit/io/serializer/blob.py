from gachit.domain.entity import Blob


class BlobSerializer:
    @staticmethod
    def serialize(blob: Blob) -> bytes:
        return blob.data

    @staticmethod
    def deserialize(data: bytes) -> Blob:
        return Blob(data)
