from datetime import datetime

from gachit.domain.entity import Commit, Sha, User


class CommitSerializer:
    @staticmethod
    def serialize(commit: Commit) -> bytes:
        data = f"tree {commit.tree.value}\n"
        for parent in commit.parents:
            data += f"parent {parent.value}\n"
        data += f"author {commit.author.name} <{commit.author.email}> "
        data += f"{int(commit.created_at.timestamp())} +0900\n"
        data += f"committer {commit.committer.name} <{commit.committer.email}> "
        data += f"{int(commit.committed_at.timestamp())} +0900\n"
        data += f"\n{commit.message}"
        return data.encode("utf-8")

    @staticmethod
    def deserialize(data: bytes) -> Commit:
        lines = data.decode("utf-8").splitlines()  # split with newline.
        parents: list[Sha] = []
        tree: Sha | None = None
        author: User | None = None
        committer: User | None = None
        created_at: datetime | None = None
        committed_at: datetime | None = None
        message: str = ""
        for line in lines:
            if line.startswith("tree "):
                tree = Sha(line[5:])
            elif line.startswith("parent "):
                parents.append(Sha(line[7:]))
            elif line.startswith("author "):
                author, created_at = User.from_commit_information(line[7:])
            elif line.startswith("committer "):
                committer, committed_at = User.from_commit_information(line[10:])
            elif len(line) > 0:  # TODO: deal with GPG signature, multiline message.
                message = line
        if (
            tree is not None
            and author is not None
            and committer is not None
            and len(message) > 0
            and committed_at is not None
            and created_at is not None
        ):
            return Commit(
                tree, parents, author, created_at, committer, committed_at, message
            )
        raise ValueError(f"Invalid commit data: {data.decode('ascii')}")
