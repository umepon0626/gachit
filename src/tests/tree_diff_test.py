from pathlib import Path

from gachit.domain.entity import Mode, Sha, Tree, TreeLeaf
from gachit.domain.service.diff.tree_to_tree import TreeDiffService


def test_tree_diff() -> None:
    """
    Test the TreeDiffService.compare_trees method.

    Before:
    .
    └── hoge
        ├── README.md (sha: `89421b07810f80d5a6ae393587733a80a34661e2`)
        ├── LICENSE.md (sha: `32bb9315c35a92995d0a5dbc2dd6179616202c0c`)
        └── src (sha: `8d9ec2e2c951124ecf4bc56dcb491fb06a7d6e5a`)
            └── main.py (sha: `3bbbd448a70bee0a672fc5502c28dfd8a6c88987`)

    After:
    .
    └── hoge
        ├── README.md (sha: `89421b07810f80d5a6ae393587733a80a34661e2`)
        ├── LICENSE.md (sha: `467644d9095952223c6402a46ad545174d8bae12`)
        └── src (sha: `15ea5656dcec2be3ec658b0fce5a88a50ea64a99`)
            └── test.py (sha: `683db051e198700f73438e30ce503b774bb7ce2d`)

    Expected:
    TreeDiff([
        BlobDiff(Path("hoge/LICENSE.md"), "32bb9315c35a92995d0a5dbc2dd6179616202c0c",
        "467644d9095952223c6402a46ad545174d8bae12"),
        BlobDiff(Path("hoge/src/main.py"), "3bbbd448a70bee0a672fc5502c28dfd8a6c88987",
        None),
        BlobDiff(Path("hoge/src/test.py"), None,
        "683db051e198700f73438e30ce503b774bb7ce2d"),
    ])
    """

    root_directory = Path("hoge")
    readme = TreeLeaf(
        Mode.FILE,
        root_directory / "README.md",
        Sha("89421b07810f80d5a6ae393587733a80a34661e2"),
    )
    before_license = TreeLeaf(
        Mode.FILE,
        root_directory / "LICENSE.md",
        Sha("32bb9315c35a92995d0a5dbc2dd6179616202c0c"),
    )
    after_license = TreeLeaf(
        Mode.FILE,
        root_directory / "LICENSE.md",
        Sha("467644d9095952223c6402a46ad545174d8bae12"),
    )
    main_py = TreeLeaf(
        Mode.FILE,
        root_directory / "src" / "main.py",
        Sha("3bbbd448a70bee0a672fc5502c28dfd8a6c88987"),
    )
    test_py = TreeLeaf(
        Mode.FILE,
        root_directory / "src" / "test.py",
        Sha("683db051e198700f73438e30ce503b774bb7ce2d"),
    )

    before = Tree(root_directory, [])
    before.add_entry(readme)
    before.add_entry(before_license)
    before.add_entry(main_py)

    after = Tree(root_directory, [])
    after.add_entry(readme)
    after.add_entry(after_license)
    after.add_entry(test_py)
    tree_diff_service = TreeDiffService(before, after)
    tree_diff_service.compare()
    assert tree_diff_service.diff.blob_diffs[Path("hoge/LICENSE.md")].before == Sha(
        "32bb9315c35a92995d0a5dbc2dd6179616202c0c"
    )
    assert tree_diff_service.diff.blob_diffs[Path("hoge/LICENSE.md")].after == Sha(
        "467644d9095952223c6402a46ad545174d8bae12"
    )

    assert tree_diff_service.diff.blob_diffs[Path("hoge/src/main.py")].before == Sha(
        "3bbbd448a70bee0a672fc5502c28dfd8a6c88987"
    )
    assert tree_diff_service.diff.blob_diffs[Path("hoge/src/main.py")].after is None

    assert tree_diff_service.diff.blob_diffs[Path("hoge/src/test.py")].before is None
    assert tree_diff_service.diff.blob_diffs[Path("hoge/src/test.py")].after == Sha(
        "683db051e198700f73438e30ce503b774bb7ce2d"
    )
