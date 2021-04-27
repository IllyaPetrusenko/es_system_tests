import pytest


def pytest_addoption(parser):
    parser.addoption("--pmd", action="store", type=str)
    parser.addoption("--country", action="store", type=str)
    parser.addoption("--language", action="store", type=str)
    parser.addoption("--tag", action="store", type=str)
    parser.addoption("--instance", action="store", type=str)
    parser.addoption("--cassandra_username", action="store", type=str)
    parser.addoption("--cassandra_password", action="store", type=str)


# def pytest_generate_tests(metafunc):
#     # This is called for every test. Only get/set command line arguments
#     # if the argument is specified in the list of test "fixturenames".
#     option_value = metafunc.config.option.country
#     if "country" in metafunc.fixturenames and option_value is not None:
#         metafunc.parametrize("country", [option_value])
#
#     option_value = metafunc.config.option.language
#     if "language" in metafunc.fixturenames and option_value is not None:
#         metafunc.parametrize("language", [option_value])
#
#     option_value = metafunc.config.option.instance
#     if "instance" in metafunc.fixturenames and option_value is not None:
#         metafunc.parametrize("instance", [option_value])
#
#     option_value = metafunc.config.option.cassandra_username
#     if "cassandra_username" in metafunc.fixturenames and option_value is not None:
#         metafunc.parametrize("cassandra_username", [option_value])
#
#     option_value = metafunc.config.option.cassandra_password
#     if "cassandra_password" in metafunc.fixturenames and option_value is not None:
#         metafunc.parametrize("cassandra_password", [option_value])


# These another fixtures, which parse arguments into command "pytest..." and which == def pytest_generate_tests
# =============================================================================================================
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
# =============================================================================================================

@pytest.fixture(scope="session")
def pmd(request):
    """Handler for --additional_value parameter"""

    return request.config.getoption("--pmd")

@pytest.fixture(scope="session")
def tag(request):
    """Handler for --additional_value parameter"""

    return request.config.getoption("--tag")
