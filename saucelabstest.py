from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Set up browser options
options = ChromeOptions()
options.browser_version = 'latest'
options.platform_name = 'Windows 11'

# Sauce Labs capabilities
sauce_options = {
    'username': 'oauth-stefano.loi-d4a95',
    'accessKey': '6d8cae05-8c01-402d-a337-ba67273b5023',
    'build': '123',
    'name': 'test1',
}

options.set_capability('sauce:options', sauce_options)

# Define Sauce Labs remote URL
url = "https://ondemand.eu-central-1.saucelabs.com:443/wd/hub"

# Start WebDriver session
driver = webdriver.Remote(command_executor=url, options=options)

# Run test
driver.get("https://www.saucedemo.com")
title = driver.title
title_is_correct = "Swag Labs" in title
job_status = "passed" if title_is_correct else "failed"

# Report test status to Sauce Labs
driver.execute_script("sauce:job-result=" + job_status)

# End session
driver.quit()
