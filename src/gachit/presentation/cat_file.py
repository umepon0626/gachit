from gachit.domain.entity import Blob, Tree


def cat_file_presentation(data: Blob | Tree) -> None:
    if isinstance(data, Blob):
        print(data.data.decode("ascii"))
    elif isinstance(data, Tree):
        raise NotImplementedError("Tree is not supported yet")
    else:
        raise ValueError(f"Unknown data type: {data}")
