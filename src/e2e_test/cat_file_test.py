from gachit.domain.entity import Blob, Commit, Tree, TreeEntryMode
from gachit.usecase import cat_file_use_case


def test_cat_blob() -> None:
    blob_sha = "00949da686b4111be68db672a34979fd58187663"
    blob = cat_file_use_case(sha_str=blob_sha)
    assert isinstance(blob, Blob)

    assert blob.data == (
        b"import click\n\n\n@click.group()"
        + b"\ndef main() -> int:\n    return 0\n\n@main.command()"
        + b'\ndef status() -> int:\n    click.echo("status")\n   '
        b" return 0"
    )


def test_cat_tree() -> None:
    tree_sha = "09a03838e0a1e227a94697f06860606af2c3aab2"
    tree = cat_file_use_case(sha_str=tree_sha)

    assert isinstance(tree, Tree)

    assert len(tree.entries) == 2
    for entry in tree.entries:
        assert entry.mode == TreeEntryMode.FILE


def test_cat_commit() -> None:
    tree_sha = "26172c045a573cd677da66845344484e0d900a9a"
    commit = cat_file_use_case(sha_str=tree_sha)

    assert isinstance(commit, Commit)
    assert commit.message == "Initial commit"
