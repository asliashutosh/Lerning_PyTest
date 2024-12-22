import pytest
from selenium import webdriver


@pytest.fixture(scope="module")
def setup_module():
    print("\nSetup: Initializing module resources")
    yield # This yield control back the test
    print("\nTeardown: Cleaning up module resources")


@pytest.fixture(scope="function")
def setup_browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
