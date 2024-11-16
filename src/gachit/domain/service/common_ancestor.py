from collections import defaultdict
from queue import Queue
from typing import DefaultDict

from gachit.domain.entity import Commit, Sha
from gachit.io.database.commit import CommitIO


class CommonAncestorService:
    def __init__(self, commit_io: CommitIO):
        self.commit_io = commit_io
        self.commit_queue: Queue[Commit] = Queue()

    def find(self, one: Commit, other: Commit) -> Commit:
        seen: DefaultDict[Sha, int] = defaultdict(int)
        # seen.value means the number of traversed commits
        # value=0 means not traversed yet
        # value=1 means traversed once
        # value=2 means traversed twice
        seen[one.tree] = 1
        seen[other.tree] = 1

        self.commit_queue.put(one)
        self.commit_queue.put(other)

        while not self.commit_queue.empty():
            commit = self.commit_queue.get()
            parent_commits = self.__get_parent_commits(commit)
            for parent_commit_sha, parent_commit in parent_commits:
                if seen[parent_commit_sha] == 1:
                    return parent_commit
                seen[parent_commit_sha] += 1
                self.commit_queue.put(parent_commit)
        return parent_commit

    def __get_parent_commits(self, commit: Commit) -> list[tuple[Sha, Commit]]:
        parent_commits: list[tuple[Sha, Commit]] = []
        for parent_sha in commit.parents:
            parent_commit = self.commit_io.get(parent_sha)
            parent_commits.append((parent_sha, parent_commit))
        return parent_commits
