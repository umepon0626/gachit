from pathlib import Path

from gachit.domain.entity import User


class UserIOError(Exception):
    pass


class UserIO:
    @staticmethod
    def read() -> User:
        gitconfig_path = Path.home() / ".gitconfig"

        if not gitconfig_path.exists():
            raise UserIOError("gitconfig file does not exist.")
        with gitconfig_path.open("r") as f:
            lines = f.readlines()
        name = None
        email = None
        for line in lines:
            if line.startswith("\tname"):
                name = line.split("=")[1].strip()
            if line.startswith("\temail"):
                email = line.split("=")[1].strip()

        if name is None or email is None:
            raise UserIOError("name or email is not found in gitconfig.")
        return User(name, email)
