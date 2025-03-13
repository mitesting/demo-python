def test_sauce_website(sauce_driver):
    sauce_driver.get("https://www.saucelabs.com")
    assert "Sauce Labs" in sauce_driver.title


