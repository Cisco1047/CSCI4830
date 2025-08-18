from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selectVehicle.models import Vehicle, Make, CarModel, CarConfiguration

class AddVehicleSeleniumTests(LiveServerTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.make = Make.objects.create(name="Ford")
        self.model = CarModel.objects.create(name="F-150", make=self.make)
        self.config = CarConfiguration.objects.create(make=self.make, model=self.model, year=2022)

    def tearDown(self):
        self.driver.quit()

    def test_add_new_vehicle_form_submission(self):
        self.driver.get(f'{self.live_server_url}/vehicles/add/')

        vin_input = self.driver.find_element(By.ID, 'id_vin')
        make_input = self.driver.find_element(By.ID, 'id_make')
        model_input = self.driver.find_element(By.ID, 'id_model')
        year_input = self.driver.find_element(By.ID, 'id_year')
        submit_button = self.driver.find_element(By.CLASS_NAME, 'button')

        vin_input.send_keys('1FTFW1RF7MFA00000')
        make_input.send_keys('Ford')
        model_input.send_keys('F-150')
        year_input.send_keys('2022')

        submit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/vehicles/add/')
        )
        
        self.assertEqual(Vehicle.objects.count(), 1)
        vehicle = Vehicle.objects.first()
        self.assertEqual(vehicle.vin, '1FTFW1RF7MFA00000')
        self.assertEqual(vehicle.configuration.year, 2022)