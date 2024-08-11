from gachit.domain.entity import Blob, Commit, Tree


def cat_file_presentation(data: Blob | Tree | Commit) -> None:
    if isinstance(data, Blob):
        print(data.data.decode("ascii"))
    elif isinstance(data, Tree):
        raise NotImplementedError("Tree is not supported yet")
    else:
        raise ValueError(f"Unknown data type: {data}")
