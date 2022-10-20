from selenium.webdriver.common.by import By


class BasePageLocators:
    CAMPAIGNS_BUTTON = (By.XPATH, '//a[@href="/dashboard"]')
    SEGMENTS_BUTTON = (By.XPATH, '//a[@href="/segments"]')
    BALANCE_BUTTON = (By.XPATH, '//a[@href="/billing" and contains(@class, "center")]')


class MainPageLocators:  # Main page - page for logi
    HEADER_LOGIN_BUTTON = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")
    EMAIL_FIELD = (By.NAME, 'email')
    PASSWORD_FIELD = (By.NAME, 'password')
    WRAP_LOGIN_BUTTON = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')


class DashboardPageLocators(BasePageLocators):
    CREATE_CAMPAIGN_BUTTON = (By.XPATH, '//div[contains(@class, "createButton")]/div/div')


class NewCampaignPageLocators(BasePageLocators):
    COVERAGE_CAMPAIGN = (By.XPATH, '//div[text()="Охват"]')
    LINK_TO_PRODUCT = (By.XPATH, '//input[contains(@class, "searchInput")]')
    CAMPAIGN_NAME = (By.XPATH, '//div[contains(@class, "input_campaign-name")]/div/input')
    BUDGET_LEFT_BAR = (By.XPATH, '//li[contains(@data-scroll-to, "budget_setting")]/div')
    DAY_BUDGET_FIELD = (By.XPATH, '//div[contains(@class, "budget-setting-daily")]/div/div/input')
    TOTAL_BUDGET_FIELD = (By.XPATH, '//div[contains(@class, "budget-setting-total")]/div/div/input')
    SUPERVIDEO = (By.XPATH, '//div[contains(@id, "supervideo")]')
    ICON_INPUT_BUTTON = (By.XPATH, '//div[contains(@class, "roles")]/div/input[contains(@accept, ".png")]')
    VIDEO_INPUT_BUTTON = (By.XPATH, '//div[contains(@class, "roles")]/div/input[contains(@accept, ".mp4")]')
    VIDEO_PREVIEW = (By.XPATH, '//video[contains(@class, "videoPreview")]')
    CAMPAIGN_HEADER_FIELD = (By.XPATH, '//input[@data-name="title_25"]')
    AD_TEXT = (By.XPATH, '//textarea[@data-name="text_40"]')
    SAVE_AD_BUTTON = (By.XPATH, '//div[@data-test="submit_banner_button"]/div')
    SAVE_CAMPAIGN_BUTTON = (By.XPATH, '//div[contains(@class, "footer__button")]/button')


class SegmentsPageLocators(BasePageLocators):
    CREATE_SEGMENT = (By.XPATH, '//button[@data-class-name="Submit"]')
    DELETE_SEGMENT = (By.XPATH, '//button[contains(@class, "confirm-remove")]')
    SEGMENTS_LIST = (By.XPATH, '//a[@href="/segments/segments_list"]')
    MASS_ACTION = (By.XPATH, '//div[contains(@class, "massAction")]')
    REMOVE_MASS = (By.XPATH, '//li[contains(@data-id, "remove")]')
    GROUPS_LIST = (By.XPATH, '//a[@href="/segments/groups_list"]')


class NewSegmentPageLocators(SegmentsPageLocators):
    GAMES_AND_APPS = (By.XPATH, '//div[text()="Приложения и игры в соцсетях"]')
    VK_OK = (By.XPATH, '//div[text()="Группы ОК и VK"]')
    SEGMENT_CHECKBOX = (By.XPATH, '//input[@type="checkbox"]')
    MODAL_ADD_SEGMENT_BUTTON = (By.XPATH, '//div[contains(@class, "modal")]/button[@data-class-name="Submit"]')
    NEW_SEGMENT_NAME = (By.XPATH, '//div[contains(@class, "create")]/div/input')
    FORM_ADD_SEGMENT_BUTTON = (By.XPATH, '//div[contains(@class, "form")]/button[@data-class-name="Submit"]')


class GroupsPage(SegmentsPageLocators):
    SEARCH_INPUT = (By.XPATH, '//input[contains(@class, "searchInput")]')
    SELECT_GROUPS = (By.XPATH, '//div[@data-test="select_all"]')
    ADD_GROUP = (By.XPATH, '//div[@data-test="add_selected_items_button"]')
    DELETE_GROUP = (By.XPATH, '//td[@data-id="remove"]/div/div')
    CONFIRM_REMOVE = (By.XPATH, '//button[contains(@class, "confirm-remove")]')
    TABLE = (By.XPATH, '//table')
    DELETE_MODAL = (By.XPATH, '//div[contains(@class, "modal-view__controls")]')
