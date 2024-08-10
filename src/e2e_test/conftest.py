import os
import shutil
from typing import Generator

import pytest
from git import Repo


def pytest_configure() -> None:
    is_test_env = os.environ.get("IS_TEST_ENV", 0)
    if is_test_env != "1":
        raise ValueError("This is not test environment")
    repo = Repo()
    user_name = os.environ.get("GIT_USER_NAME", None)
    user_email = os.environ.get("GIT_USER_EMAIL", None)
    if user_name is None or user_email is None:
        raise ValueError("Please set GIT_USER_NAME and GIT_USER_EMAIL")
    with repo.config_writer() as cw:
        cw.set_value("user", "name", user_name)
        cw.set_value("user", "email", user_email)


def clean_up_after_each_tests() -> None:
    # .gitフォルダを削除
    shutil.rmtree(".git")


def clean_up_after_all_tests() -> None:
    # .gitファイルを元の場所に戻す
    shutil.copytree("test/.git", ".git", dirs_exist_ok=True)


def setup_before_all_tests() -> None:
    # .gitファイルを別の場所にコピー
    shutil.copytree(".git", "test/.git", dirs_exist_ok=True)


def setup_before_each_tests() -> None:
    # .gitファイルをもとに戻す
    shutil.copytree("test/.git", ".git", dirs_exist_ok=True)


@pytest.fixture(scope="session", autouse=True)
def secure_original_git_folder() -> Generator[None, None, None]:
    setup_before_all_tests()
    yield
    clean_up_after_all_tests()


@pytest.fixture(scope="function", autouse=True)
def reset_git_folder() -> Generator[None, None, None]:
    setup_before_each_tests()
    yield
    clean_up_after_each_tests()
