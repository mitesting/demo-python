import os

import pytest
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

urllib3.disable_warnings()

@pytest.fixture()
def headless_driver(request):
    options = ChromeOptions()
    options.browser_version = 'latest'
    options.platform_name = 'Windows 10'
    options.headless = True

    sauce_options = {
    'username': 'oauth-stefano.loi-d4a95',
    'accessKey': '6d8cae05-8c01-402d-a337-ba67273b5023',
    'build': '123',
    'name': 'test1',
}

    options.set_capability('sauce:options', sauce_options)
    sauce_url = "https://ondemand.us-west-1.saucelabs.com/wd/hub"

    driver = webdriver.Remote(command_executor=sauce_url, options=options)

    yield driver

    if driver is not None:
        sauce_result = "failed" if request.session.testsfailed == 1 else "passed"
        driver.execute_script("sauce:job-result={}".format(sauce_result))

        driver.quit()

@pytest.fixture()
def driver(request):
    options = ChromeOptions()
    options.browser_version = 'latest'
    options.platform_name = 'Windows 10'

    sauce_options = {
    'username': 'oauth-stefano.loi-d4a95',
    'accessKey': '6d8cae05-8c01-402d-a337-ba67273b5023',
    'build': '123',
    'name': 'test1',
}

    options.set_capability('sauce:options', sauce_options)
    sauce_url = "https://ondemand.us-west-1.saucelabs.com/wd/hub"

    driver = webdriver.Remote(command_executor=sauce_url, options=options)

    yield driver

    if driver is not None:
        sauce_result = "failed" if request.session.testsfailed == 1 else "passed"
        driver.execute_script("sauce:job-result={}".format(sauce_result))

        driver.quit()
