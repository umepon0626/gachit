import os
import shutil
from pathlib import Path
from typing import Generator

import pytest
from git import Repo

playground_path = Path("/workspace/playground")


def pytest_configure() -> None:
    print("pytest_configure is called")
    is_test_env = os.environ.get("IS_TEST_ENV", 0)
    if is_test_env != "1":
        raise ValueError("This is not test environment")
    repo = Repo(playground_path)
    user_name = os.environ.get("GIT_USER_NAME", None)
    user_email = os.environ.get("GIT_USER_EMAIL", None)
    if user_name is None or user_email is None:
        raise ValueError("Please set GIT_USER_NAME and GIT_USER_EMAIL")
    with repo.config_writer() as cw:
        cw.set_value("user", "name", user_name)
        cw.set_value("user", "email", user_email)


def delete_escaped_playground() -> None:
    # 退避していたplaygroundを削除
    shutil.rmtree(playground_path.parent / "playground_escaped")


def escape_playground() -> None:
    # playgroundを退避
    shutil.copytree(
        playground_path,
        playground_path.parent / "playground_escaped",
        dirs_exist_ok=True,
    )


def recover_playground_from_escaped() -> None:
    # 退避していたplaygroundをもとに戻す
    shutil.rmtree(playground_path)
    shutil.copytree(playground_path.parent / "playground_escaped", playground_path)


@pytest.fixture(scope="session", autouse=True)
def secure_playground() -> Generator[None, None, None]:
    escape_playground()
    yield
    delete_escaped_playground()


@pytest.fixture(scope="function", autouse=True)
def reset_playground() -> Generator[None, None, None]:
    recover_playground_from_escaped()
    yield
