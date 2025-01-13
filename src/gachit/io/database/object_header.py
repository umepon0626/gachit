from dataclasses import dataclass

from gachit.domain.entity import Blob, Commit, Tree


@dataclass
class ObjectHeader:
    object_type: type[Blob | Tree | Commit]
    content_size: int

    @property
    def value(self) -> bytes:
        return (
            self.object_type.format.encode("ascii")
            + b" "
            + str(self.content_size).encode()
            + b"\x00"
        )

    @classmethod
    def from_data(cls, data: bytes) -> "ObjectHeader":
        header_end = data.find(b" ")
        object_format = data[:header_end].decode("ascii")
        null_byte_end = data.find(b"\x00", header_end)
        content_size = int(data[header_end:null_byte_end].decode("ascii"))
        return cls(
            object_type=Blob
            if object_format == Blob.format
            else Tree
            if object_format == Tree.format
            else Commit,
            content_size=content_size,
        )


# TODO: delete from_data method and use __init__ instead.
# TODO: delete value property and use __bytes__ instead.
