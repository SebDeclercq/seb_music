from typing import Any, Callable
from _pytest.config.argparsing import Parser
from _pytest.python import Function
from django.http import HttpResponse
from django.test import Client
from graphene_django.utils.testing import graphql_query
import pytest


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        '--api_call',
        action='store',
        default='on',
        help='Run the API calls along the other tests: on/off (default: on)',
    )
    parser.addoption(
        '--current',
        action='store_true',
        help='Run the tests under current development only',
    )


def pytest_runtest_setup(item: Function) -> None:
    if item.config.getoption('--current'):
        if 'current_dev' not in item.keywords:
            pytest.skip()
        else:
            _with_api_calls(item)
    else:
        _with_api_calls(item)


def _with_api_calls(item: Function) -> None:
    on_off: str = item.config.getoption('--api_call')
    if on_off.lower() == 'off':
        if 'real_api_call' in item.keywords:
            pytest.skip()


@pytest.fixture
def graphql_client(client: Client) -> Callable[..., HttpResponse]:
    def func(query: str, *args: Any, **kwargs: Any) -> HttpResponse:
        return graphql_query(query, *args, **kwargs)

    return func
