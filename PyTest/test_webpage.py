from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest


class TestSample:
    @pytest.fixture(scope="class")
    def test_setup(self):
        # global driver
        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)

        driver.maximize_window()

        yield driver
        driver.close()
        driver.quit()
        print('Test Completed!')

    def test_getToSearch(self, test_setup):
        driver_instance = test_setup
        driver_instance.get(
            'http://127.0.0.1:8000/')
        get_started_button = WebDriverWait(driver_instance, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.mbr-section-btn .btn:not(.btn-form)'))
        )

        get_started_button.click()

    def test_searchForCar(self, test_setup):
        driver_instance = test_setup
        year_button = WebDriverWait(driver_instance, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'yearButton')
            )
        )
        year_button.click()

        select_year = WebDriverWait(driver_instance, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'year2006')
            )
        )

        select_year.click()

        make_button = WebDriverWait(driver_instance, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'makeButton')
            )
        )
        make_button.click()

        select_make = WebDriverWait(driver_instance, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'lexusCar')
            )
        )

        select_make.click()

        model_button = WebDriverWait(driver_instance, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'modelButton')
            )
        )
        model_button.click()

        select_model = WebDriverWait(driver_instance, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#modelDropdown > li:nth-child(1) > a:nth-child(1)'))
        )

        select_model.click()

        search = WebDriverWait(driver_instance, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.text-center > button:nth-child(1)'))
        )

        search.click()
