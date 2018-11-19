from selenium import webdriver
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture(scope="session")
def driver():
    print("Creating driver")
    driver = webdriver.Chrome('/Users/victoria/Downloads/chromedriver')
    driver.implicitly_wait(30)
    yield driver
    print("Closing driver")
    driver.close()

def test_open_page(driver):
    driver.get('http://127.0.0.1:5000/home.html')
    bla = driver.find_element_by_id('submit')
    assert bla.text == 'Submit'


def test_input_form1(driver):
    driver.get('http://127.0.0.1:5000/home.html')
    email = driver.find_element_by_id("inputEmail").send_keys("v.sapronova@gm.com")
    assert email is None


def test_input_form2(driver):
    driver.get('http://127.0.0.1:5000/home.html')
    date = driver.find_element_by_id("datepicker").send_keys("11/15/2018")
    assert date is None


def test_popup_form(driver):
    driver.get('http://127.0.0.1:5000/home.html')
    driver.find_element_by_id("inputEmail").send_keys("v.sapronova.gm.com")
    driver.find_element_by_id("datepicker").send_keys("11/15/2018")
    driver.find_element_by_id('submit').click()

    wait = WebDriverWait(driver, 5)
    alert = wait.until(EC.visibility_of_element_located((By.ID, "failed")))

    assert "Ooops" in alert.text


def test_empty_email():
    driver.get('http://127.0.0.1:5000/home.html')
    driver.find_element_by_id("inputEmail").send_keys(" ")

    assert alert.text == "Please enter valid email address"


def test_empty_date():
    driver.get('http://127.0.0.1:5000/home.html')
    driver.find_element_by_id("datepicker").send_keys(" ")

    assert alert.text == "Please pick a date"

