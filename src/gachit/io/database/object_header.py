from dataclasses import dataclass

from gachit.domain.entity import Blob, Commit, Tree


@dataclass
class ObjectHeader:
    object_type: type[Blob | Tree | Commit]
    content_size: int

    @property
    def value(self) -> bytes:
        """header bytes

        Returns:
            bytes: return `<object type> <content size>\x00`. \x00 stands for null byte
        """
        return (
            self.object_type.format.encode()
            + b" "
            + str(self.content_size).encode()
            + b"\x00"
        )

    @classmethod
    def from_data(cls, data: bytes) -> "ObjectHeader":
        """Create an ObjectHeader from data

        Args:
            data (bytes): `<object type> <content size>\x00` formatted bytes

        Returns:
            ObjectHeader: object header
        """
        # detect object type
        object_type_end = data.find(b" ")
        object_format = data[:object_type_end].decode("ascii")

        # detect content size
        header_end = data.find(b"\x00", object_type_end)
        content_size = int(data[object_type_end:header_end].decode("ascii"))

        return cls(
            object_type=Blob
            if object_format == Blob.format
            else Tree
            if object_format == Tree.format
            else Commit,
            content_size=content_size,
        )
