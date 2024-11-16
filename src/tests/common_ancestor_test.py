import datetime
from pathlib import Path

from gachit.domain.entity import Commit, Sha, User
from gachit.domain.service.common_ancestor import CommonAncestorService
from gachit.io.database.commit import CommitIO
from pytest_mock import MockFixture


def get_sha(label: str) -> Sha:
    data = (label * 40)[:40]
    return Sha(data)


COMMIT_DATE = datetime.datetime.now()
AUTHOR = User("author", "test@example.com")

COMMIT_SHA_MAP = {
    "A": get_sha("A"),
    "B": get_sha("B"),
    "C": get_sha("C"),
    "D": get_sha("D"),
    "E": get_sha("E"),
    "F": get_sha("F"),
    "G": get_sha("G"),
    "H": get_sha("H"),
    "I": get_sha("I"),
    "J": get_sha("J"),
    "K": get_sha("K"),
    "L": get_sha("L"),
    "M": get_sha("M"),
    "N": get_sha("N"),
    "O": get_sha("O"),
    "P": get_sha("P"),
    "Q": get_sha("Q"),
    "R": get_sha("R"),
    "S": get_sha("S"),
    "T": get_sha("T"),
    "U": get_sha("U"),
    "V": get_sha("V"),
    "W": get_sha("W"),
    "X": get_sha("X"),
    "Y": get_sha("Y"),
    "Z": get_sha("Z"),
}


def get_mock_commit(sha: Sha, parents_sha: list[Sha]) -> Commit:
    return Commit(
        tree=get_sha(sha.value + "tree"),
        author=AUTHOR,
        committer=AUTHOR,
        message="message",
        created_at=COMMIT_DATE,
        committed_at=COMMIT_DATE,
        parents=parents_sha,
    )


def build_commit_graph(sha_graph: dict[Sha, list[Sha]]) -> dict[Sha, Commit]:
    sha_commit_map = {}
    for sha, parents_sha in sha_graph.items():
        sha_commit_map[sha] = get_mock_commit(sha, parents_sha)
    return sha_commit_map


class MockCommitIO:
    def __init__(self, sha_graph: dict[Sha, list[Sha]]) -> None:
        self.sha_graph = sha_graph

    def get(self, sha: Sha) -> Commit:
        parents_sha = self.sha_graph.get(sha, [])
        return get_mock_commit(sha, parents_sha)


def test_normal_common_ancestor(mocker: MockFixture) -> None:
    """Test common ancestor

    Graph:
    A -> B -> D -> F
      \
        -> C -> E -> G
    """

    commit_graph = {
        COMMIT_SHA_MAP["A"]: [],
        COMMIT_SHA_MAP["B"]: [COMMIT_SHA_MAP["A"]],
        COMMIT_SHA_MAP["D"]: [COMMIT_SHA_MAP["B"]],
        COMMIT_SHA_MAP["C"]: [COMMIT_SHA_MAP["A"]],
        COMMIT_SHA_MAP["E"]: [COMMIT_SHA_MAP["C"]],
        COMMIT_SHA_MAP["F"]: [COMMIT_SHA_MAP["D"]],
        COMMIT_SHA_MAP["G"]: [COMMIT_SHA_MAP["E"]],
    }
    sha_commit_map = build_commit_graph(commit_graph)
    mock_commit_io = MockCommitIO(commit_graph)
    mocker.patch.object(CommitIO, "get", mock_commit_io.get)
    common_ancestor = CommonAncestorService(CommitIO(Path("."))).find(
        sha_commit_map.get(COMMIT_SHA_MAP["D"]),  # type: ignore
        sha_commit_map.get(COMMIT_SHA_MAP["G"]),  # type: ignore
    )
    assert common_ancestor == sha_commit_map.get(COMMIT_SHA_MAP["A"])


def test_merged_common_ancestor(mocker: MockFixture) -> None:
    """Test common ancestor

    Graph:
    A -> B -> D -> F
      \      /
        -> C -> E -> G
    """

    commit_graph = {
        COMMIT_SHA_MAP["A"]: [],
        COMMIT_SHA_MAP["B"]: [COMMIT_SHA_MAP["A"]],
        COMMIT_SHA_MAP["D"]: [COMMIT_SHA_MAP["B"], COMMIT_SHA_MAP["C"]],
        COMMIT_SHA_MAP["C"]: [COMMIT_SHA_MAP["A"]],
        COMMIT_SHA_MAP["E"]: [COMMIT_SHA_MAP["C"]],
        COMMIT_SHA_MAP["F"]: [COMMIT_SHA_MAP["D"]],
        COMMIT_SHA_MAP["G"]: [COMMIT_SHA_MAP["E"]],
    }
    sha_commit_map = build_commit_graph(commit_graph)
    mock_commit_io = MockCommitIO(commit_graph)
    mocker.patch.object(CommitIO, "get", mock_commit_io.get)
    common_ancestor = CommonAncestorService(CommitIO(Path("."))).find(
        sha_commit_map.get(COMMIT_SHA_MAP["F"]),  # type: ignore
        sha_commit_map.get(COMMIT_SHA_MAP["G"]),  # type: ignore
        # sha_commit_map.get(COMMIT_SHA_MAP["D"]),
        # sha_commit_map.get(COMMIT_SHA_MAP["G"])
        # TODO: cannot find best common ancestor.
        # It should be C not A.
    )
    assert common_ancestor == sha_commit_map.get(COMMIT_SHA_MAP["C"])
