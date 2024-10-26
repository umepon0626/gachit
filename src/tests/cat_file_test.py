from pathlib import Path

from gachit.domain.entity import Blob, Commit, Mode, Tree, TreeLeaf
from gachit.usecase import cat_file_use_case

playground_path = Path("/workspace/playground")


def test_cat_blob() -> None:
    blob_sha = "897afe774be03b564fdcc0961a8760bb3b702904"
    blob = cat_file_use_case(sha_str=blob_sha, repository_root_dir=playground_path)
    assert isinstance(blob, Blob)

    assert blob.data == (b"# gachit_practice")


def test_cat_tree() -> None:
    tree_sha = "b0ab15557329cd5f0389548de7117fc79630d52a"
    tree = cat_file_use_case(sha_str=tree_sha, repository_root_dir=playground_path)

    assert isinstance(tree, Tree)

    assert len(tree.entries) == 1
    for entry in tree.entries.values():
        assert isinstance(entry, TreeLeaf)
        assert entry.mode == Mode.FILE


def test_cat_commit() -> None:
    tree_sha = "613cb901d050fa723c3b880a60643de39866d157"
    commit = cat_file_use_case(sha_str=tree_sha, repository_root_dir=playground_path)

    assert isinstance(commit, Commit)
    assert commit.message == "Update README.md"
