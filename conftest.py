import os
import pytest
from selenium import webdriver


@pytest.fixture(params=[
    {"browserName": "chrome", "platformName": "Windows 10"},
    {"browserName": "firefox", "platformName": "Windows 10"},
    {"browserName": "safari", "platformName": "macOS 12"}
])
def sauce_driver(request):
    username = os.environ["SAUCE_USERNAME"]
    access_key = os.environ["SAUCE_ACCESS_KEY"]
    build_tag = os.environ.get("BUILD_ID", "local-build")

    sauce_url = f"https://{username}:{access_key}@ondemand.eu-central-1.saucelabs.com/wd/hub"

    # Use request.param to get the browser configuration
    browser_config = request.param

    capabilities = {
        # Load browserName and platformName from the parameter
        "browserName": browser_config["browserName"],
        "platformName": browser_config["platformName"],
        "browserVersion": "latest",
        "sauce:options": {
            "build": build_tag,
            "name": request.node.name,
            # Add tunnel identifier if using Sauce Connect
            "tunnelIdentifier": "github-tunnel" if os.environ.get("USE_SAUCE_CONNECT") else None
        }
    }

    # Create appropriate options object based on browser
    if browser_config["browserName"] == "chrome":
        options = webdriver.ChromeOptions()
    elif browser_config["browserName"] == "firefox":
        options = webdriver.FirefoxOptions()
    elif browser_config["browserName"] == "safari":
        options = webdriver.SafariOptions()
    else:
        options = webdriver.ChromeOptions()  # Default

    # Set capabilities
    options.set_capability('sauce:options', capabilities['sauce:options'])
    for key, value in capabilities.items():
        if key != 'sauce:options':
            options.set_capability(key, value)

    driver = webdriver.Remote(command_executor=sauce_url, options=options)

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