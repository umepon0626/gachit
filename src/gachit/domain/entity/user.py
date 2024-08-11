from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """User

    Args:
        name (str): User name
        email (str): User email
        datetime (datetime): commit datetime
    """

    name: str
    email: str
    datetime: datetime

    @classmethod
    def from_commit_information(cls, commit_information: str) -> "User":
        """Create User from commit information

        Args:
            commit_information (str): Commit information
            like "test_user <test@example.com> 1423299412 +0900".

        Returns:
            User: User object

        Examples:
            >>> commit_information = "test_user <test@example.com> 1423299412 +0900"
            >>> User.from_commit_information(commit_information)
            User(name='test_user', email='test@example.com', \
            datetime=datetime.datetime(2015, 2, 7, 8, 56, 52))
        """
        email_start = commit_information.find("<")
        email_end = commit_information.find(">")
        name = commit_information[: email_start - 1]
        email = commit_information[email_start + 1 : email_end]
        timestamp = commit_information.split(" ")[-2]
        # TODO: parse timezone
        return cls(name, email, datetime.fromtimestamp(int(timestamp)))
