import pytest


def pytest_addoption(parser):
    """PyTest method for adding custom console parameters"""

    parser.addoption("--pmd", action="store", type=str)
    parser.addoption("--country", action="store", type=str)
    parser.addoption("--language", action="store", type=str)
    parser.addoption("--tag", action="store", type=str)
@pytest.fixture(scope="session")
def pmd(request):

    """Handler for --additional_value parameter"""

    return request.config.getoption("--pmd")

@pytest.fixture(scope="session")
def country(request):

    """Handler for --additional_value parameter"""

    return request.config.getoption("--country")

@pytest.fixture(scope="session")
def language(request):

    """Handler for --additional_value parameter"""

    return request.config.getoption("--language")

@pytest.fixture(scope="session")
def tag(request):

    """Handler for --additional_value parameter"""

    return request.config.getoption("--tag")

