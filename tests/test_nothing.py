from typing import Generator
import pytest

from your_app import __version__  # replace 'your_app' with the actual package name

# to test your app, use absolute imports just like any third-party package
# import your_app.module

# use `print` to log in tests because only those will get printed out on test failure
# if you want to see logs then first - initialize logging and then run the tests
# as pytest -s


def test_version():
    assert __version__.startswith("99"), (
        "You are not testing local version 99.99; current version is %s" % __version__
    )


@pytest.fixture
def name_matters() -> Generator[int, None, None]:
    print("Entering fixture")
    yield 1
    print("Exiting fixture")


def test_nothing(name_matters: int):
    print("Entering test")
    assert name_matters == 1, "fixture should yield/return 1, got %s" % name_matters
    print("Exiting test")
