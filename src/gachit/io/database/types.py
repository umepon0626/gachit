from gachit.domain.entity import Blob, Commit, Tree

GitObjectTypes = Blob | Tree | Commit
GitObjectFormats = {Blob: Blob.format, Tree: Tree.format, Commit: Commit.format}
