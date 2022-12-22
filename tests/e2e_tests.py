import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

WAIT_SEC = 30


@pytest.fixture
def setup():
    morda_url = ''
    chrome_driver = webdriver.Chrome(ChromeDriverManager().install())
    yield dict(url=morda_url, driver=chrome_driver)


class TestDepressionMorda:

    def test_positive(self, setup):
        driver = setup['driver']
        driver.get(setup['url'])

        header = driver.find_element(By.CSS_SELECTOR, 'body > app-root > app-header > header > nav > div > a')
        assert header.text == 'Распознаватель депрессии'

        text_field = driver.find_element(By.CSS_SELECTOR, '#mat-input-0')
        text_field.clear()
        text_field.send_keys('Я такой депрессивный, я так хочу умереть. Очень надоело жить')

        birthday_field = driver.find_element(By.CSS_SELECTOR, '#mat-input-1')
        birthday_field.clear()
        birthday_field.send_keys('11.09.2001')

        button_num = 2  # male
        radio_button_choice = driver.find_element(By.CSS_SELECTOR, f'#mat-radio-{button_num}')
        radio_button_choice.click()

        submit_button = driver.find_element(By.CSS_SELECTOR,
                                            'body > app-root > div > app-home > div > form > div:nth-child(6) > button')
        submit_button.click()

        try:
            result_text = WebDriverWait(driver, WAIT_SEC).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'body > app-root > div > app-home > div > div > div > span'))
            )
            assert result_text.text == 'Депресивные признаки не обнаружены'
        except TimeoutException as e:
            assert False
