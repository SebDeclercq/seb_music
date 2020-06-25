from typing import Any
import pytest


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--api_call", action="store_true", help="Run the real API calls only",
    )
    parser.addoption(
        "--no_api_call",
        action="store_true",
        help="Do not run the real API calls along the other tests",
    )


def pytest_runtest_setup(item: Any) -> None:
    if item.config.getoption("--api_call"):
        if 'real_api_call' not in item.keywords:
            pytest.skip('')
    if item.config.getoption('--no_api_call'):
        if 'real_api_call' in item.keywords:
            pytest.skip('')
