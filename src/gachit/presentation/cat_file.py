from gachit.domain.entity import Blob


def cat_file_presentation(data: Blob) -> None:
    print(data.data.decode("ascii"))
