from selenium.webdriver.common.by import By


class LoginPageLocators:
    DATA_BLOCK = (By.CSS_SELECTOR, 'div.uk-card')
    USERNAME_INPUT_FIELD = (By.CSS_SELECTOR, 'input#username')
    PASSWORD_INPUT_FIELD = (By.CSS_SELECTOR, 'input#password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'input#submit')
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, 'div > a')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'div#flash')
    ERROR_AUTH = (By.XPATH, "//div[contains(text(), 'This page is available')]")
