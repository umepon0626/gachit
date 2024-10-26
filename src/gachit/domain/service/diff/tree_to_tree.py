from gachit.domain.entity import BlobDiff, Tree, TreeDiff, TreeLeaf


class TreeDiffService:
    def __init__(self, before: Tree, after: Tree) -> None:
        self.diff = TreeDiff(before, after)

    def compare(self) -> None:
        self.__compare_tree(self.diff.before, self.diff.after)

    def __compare_tree(self, before: Tree, after: Tree) -> None:
        self.collect_deleted_entries(before, after)
        self.collect_added_entries(before, after)

    def collect_deleted_entries(self, before: Tree, after: Tree) -> None:
        for name, before_entry in before.entries.items():
            same_after_entry = after.entries.get(name, None)
            if same_after_entry is None:
                self.add_entry(before_entry, is_deleted=True)
            else:
                if isinstance(before_entry, Tree) and isinstance(
                    same_after_entry, Tree
                ):
                    self.__compare_tree(before_entry, same_after_entry)

                elif isinstance(before_entry, TreeLeaf) and isinstance(
                    same_after_entry, TreeLeaf
                ):
                    if before_entry.sha != same_after_entry.sha:
                        self.diff.blob_diffs[before_entry.path] = BlobDiff(
                            before_entry.path, before_entry.sha, same_after_entry.sha
                        )
                else:
                    self.add_entry(before_entry, is_deleted=True)
                    # This means that the types of two entries are different.
                    # ex) before_entry is Tree and same_after_entry is TreeLeaf and both
                    # have the same path.

                    # In this case, we have to add before_entry as a deleted entry
                    # and after entry as an added entry.

    def collect_added_entries(self, before: Tree, after: Tree) -> None:
        for name, after_entry in after.entries.items():
            same_before_entry = before.entries.get(name, None)

            if same_before_entry is None:
                self.add_entry(after_entry, is_deleted=False)
            else:
                if isinstance(after_entry, Tree) and isinstance(
                    same_before_entry, Tree
                ):
                    self.__compare_tree(same_before_entry, after_entry)
                elif isinstance(after_entry, TreeLeaf) and isinstance(
                    same_before_entry, TreeLeaf
                ):
                    # This case is already handled in collect_deleted_entries.
                    pass
                else:
                    self.add_entry(after_entry, is_deleted=False)
                    # This means that the types of two entries are different.
                    # ex) after_entry is Tree and same_before_entry is TreeLeaf and both
                    # have the same path.

                    # In this case, we have to add before_entry as a deleted entry
                    # and after entry as an added entry.

    def add_entry(self, entry: Tree | TreeLeaf, is_deleted: bool) -> None:
        if isinstance(entry, Tree):
            for child in entry.entries.values():
                if isinstance(child, Tree):
                    self.add_entry(child, is_deleted=is_deleted)
                else:
                    if is_deleted:
                        self.diff.blob_diffs[child.path] = BlobDiff(
                            child.path, child.sha, None
                        )
                    else:
                        self.diff.blob_diffs[child.path] = BlobDiff(
                            child.path, None, child.sha
                        )
        else:
            if is_deleted:
                self.diff.blob_diffs[entry.path] = BlobDiff(entry.path, entry.sha, None)
            else:
                self.diff.blob_diffs[entry.path] = BlobDiff(entry.path, None, entry.sha)
