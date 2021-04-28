import pytest


def pytest_addoption(parser):
    parser.addoption("--pmd", action="store", type=str)
    parser.addoption("--country", action="store", type=str)
    parser.addoption("--language", action="store", type=str)
    parser.addoption("--tag", action="store", type=str)
    parser.addoption("--instance", action="store", type=str)
    parser.addoption("--cassandra_username", action="store", type=str)
    parser.addoption("--cassandra_password", action="store", type=str)


@pytest.fixture(scope="session")
def country(request):
    """Handler for --additional_value parameter"""
    return request.config.getoption("--country")


@pytest.fixture(scope="session")
def language(request):
    """Handler for --additional_value parameter"""

    return request.config.getoption("--language")


@pytest.fixture(scope="session")
def instance(request):
    """Handler for --additional_value parameter"""
    return request.config.getoption("--instance")


@pytest.fixture(scope="session")
def cassandra_username(request):
    """Handler for --additional_value parameter"""
    return request.config.getoption("--cassandra_username")


@pytest.fixture(scope="session")
def cassandra_password(request):
    """Handler for --additional_value parameter"""
    return request.config.getoption("--cassandra_password")



