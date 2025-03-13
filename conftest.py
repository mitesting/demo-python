import os
import pytest
from selenium import webdriver


@pytest.fixture
def sauce_driver(request):
    username = os.environ["SAUCE_USERNAME"]
    access_key = os.environ["SAUCE_ACCESS_KEY"]
    build_tag = os.environ.get("BUILD_ID", "local-build")

    sauce_url = f"https://{username}:{access_key}@ondemand.eu-central-1.saucelabs.com/wd/hub"

    # You can customize these capabilities as needed
    capabilities = {
        "browserName": "chrome",
        "platformName": "Windows 10",
        "browserVersion": "latest",
        "sauce:options": {
            "build": build_tag,
            "name": request.node.name
        }
    }

    driver = webdriver.Remote(command_executor=sauce_url,
                              options=webdriver.ChromeOptions().set_capability('sauce:options', capabilities))

    # Report pass/fail back to Sauce Labs
    def fin():
        driver.execute_script("sauce:job-result={}".format("passed" if request.node.rep_call.passed else "failed"))
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)