from gachit.domain.entity import Commit, Sha, User


class CommitSerializer:
    @classmethod
    def serialize(cls, commit: Commit) -> bytes:
        data = f"tree {commit.tree}\n"
        for parent in commit.parents:
            data += f"parent {parent}\n"
        data += f"author {commit.author}\n"
        data += f"committer {commit.committer}\n"
        data += f"\n{commit.message}"
        return data.encode("ascii")

    @classmethod
    def deserialize(cls, data: bytes) -> Commit:
        lines = data.decode("ascii").splitlines()
        parents: list[Sha] = []
        tree: Sha | None = None
        author: User | None = None
        committer: User | None = None
        message: str = ""
        for line in lines:
            if line.startswith("tree "):
                tree = Sha(line[5:])
            elif line.startswith("parent "):
                parents.append(Sha(line[7:]))
            elif line.startswith("author "):
                author = User.from_commit_information(line[7:])
            elif line.startswith("committer "):
                committer = User.from_commit_information(line[10:])
            elif len(line) > 0:  # TODO: deal with GPG signature, multiline message.
                message = line
        if (
            tree is not None
            and author is not None
            and committer is not None
            and len(message) > 0
        ):
            return Commit(tree, parents, author, committer, message)
        raise InvalidCommitDataError(f"Invalid commit data: {data.decode('ascii')}")


class InvalidCommitDataError(Exception):
    pass
