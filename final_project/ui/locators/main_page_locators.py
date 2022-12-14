from selenium.webdriver.common.by import By


class MainPageLocators:
    HOME_BUTTON_BUG = (By.CSS_SELECTOR, 'a.uk-navbar-brand')
    HOME_BUTTON = (By.XPATH, '//a[contains(text(), "HOME")]')
    PYTHON_BUTTON = (By.XPATH, '//a[text()="Python"]')
    PYTHON_HISTORY_BUTTON = (By.XPATH, '//a[text()="Python history"]')
    ABOUT_FLASK_BUTTON = (By.XPATH, '//a[contains(text(), "About Flask")]')
    LINUX_BUTTON = (By.XPATH, '//a[text()="Linux"]')
    CENTOS_DOWNLOAD_BUTTON = (By.XPATH, '//a[contains(text(), "Download Centos")]')
    NETWORK_BUTTON = (By.XPATH, '//a[text()="Network"]')
    NETWORK_NEWS_BUTTON = (By.XPATH, '//a[text()="News"]')
    NETWORK_DOWNLOAD_BUTTON = (By.XPATH, '//a[text()="Download"]')
    NETWORK_EXAMPLES_BUTTON = (By.XPATH, '//a[contains(text(), "Examples")]')
    LOGGED_AS_TEXT = (By.XPATH, '//li[contains(text(), "Logged")]')
    USER_TEXT = (By.XPATH, '//li[contains(text(), "User")]')
    VK_ID = (By.XPATH, '//li[contains(text(), "VK ID")]')
    API_BUTTON = (By.XPATH, '//img[@src="/static/images/laptop.png"]')
    WWW_BUTTON = (By.XPATH, '//img[@src="/static/images/loupe.png"]')
    SMTP_BUTTON = (By.XPATH, '//img[@src="/static/images/analytics.png"]')
    FOOTER_TEXT = (By.CSS_SELECTOR, 'footer div > p')
