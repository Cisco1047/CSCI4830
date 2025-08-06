from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest


class TestLogin:
    @pytest.fixture(scope="class")
    def test_setup(self):
        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.maximize_window()

        yield driver
        driver.quit()
        print("Test Completed!")

    def test_open_login_page(self, test_setup):
        driver_instance = test_setup
        driver_instance.get("http://127.0.0.1:8000/login/")
        
        WebDriverWait(driver_instance, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        assert "Login" in driver_instance.page_source

