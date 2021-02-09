import pytest


def pytest_addoption(parser):
    """PyTest method for adding custom console parameters"""

    parser.addoption("--additional_value", action="store", type=str)


@pytest.fixture(scope="session")
def additional_value(request):

    """Handler for --additional_value parameter"""

    return request.config.getoption("--additional_value")


