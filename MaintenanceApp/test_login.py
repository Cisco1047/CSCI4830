import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="class")
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    _driver = webdriver.Chrome(options=chrome_options)
    request.cls.driver = _driver
    yield _driver
    _driver.quit()

@pytest.mark.usefixtures("driver")
class TestLogin:
    def test_open_login_page(self, live_server):
        self.driver.get(f'{live_server.url}')
        assert "CarPal" in self.driver.title