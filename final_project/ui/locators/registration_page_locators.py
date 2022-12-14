from selenium.webdriver.common.by import By


class RegistrationPageLocators:
    DATA_BLOCK = (By.CSS_SELECTOR, 'div.uk-flex-center')
    NAME_INPUT = (By.CSS_SELECTOR, 'input#user_name')
    SURNAME_INPUT = (By.CSS_SELECTOR, 'input#user_surname')
    MIDDLE_NAME_INPUT = (By.CSS_SELECTOR, 'input#user_middle_name')
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input#username')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input#email')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input#password')
    REPEAT_PASS_INPUT = (By.CSS_SELECTOR, 'input#confirm')
    SDET_CHECKBOX = (By.CSS_SELECTOR, 'input#term')
    REGISTER_BUTTON = (By.CSS_SELECTOR, 'input#submit')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'div > a')

    EMAIL_LENGTH_MESSAGE = (By.XPATH, "//div[contains(text(), 'Incorrect email length')]")
    DIFF_PASSWORDS_MESSAGE = (By.XPATH, "//div[contains(text(), 'Passwords must match')]")
    USER_ALREADY_EXISTS_MESSAGE = (By.XPATH, "//div[contains(text(), 'User already exist')]")
    EMAIL_ALREADY_EXISTS_MESSAGE = (By.XPATH, "//div[contains(text(), 'Internal Server Error')]")
    INVALID_EMAIL_MESSAGE = (By.XPATH, "//div[contains(text(), 'Invalid email address')]")

