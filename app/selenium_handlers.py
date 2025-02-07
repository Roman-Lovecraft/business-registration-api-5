import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def fill_form_oregon(credentials, data) -> str:
    """
    Заполняет форму регистрации на сайте sos.oregon.gov с использованием Selenium.
    Возвращает application_id, полученный после успешной отправки формы.
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Запуск веб-драйвера Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://sos.oregon.gov/")

        # Нажатие на кнопку "Register a Business"
        register_business_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register a Business")))
        register_business_button.click()

        # Переключение на новое окно
        wait.until(EC.number_of_windows_to_be(2))
        windows = driver.window_handles
        driver.switch_to.window(windows[1])


        # Нажатие на кнопку "New User"
        log_in_button = wait.until(EC.element_to_be_clickable((By.ID, "loginButton")))
        log_in_button.click()

        # Авторизация
        login = wait.until(EC.presence_of_element_located((By.ID, "username")))
        login.send_keys(credentials["login"])
        password = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password.send_keys(credentials["password"])
        login_button = driver.find_element(By.NAME, "Login")
        login_button.click()

        # Проверка наличия кнопки отмены (если аккаунт новый)
        try:
            cancel_button = wait.until(EC.element_to_be_clickable((By.ID, "cancelButton")))
            cancel_button.click()
        except:
            pass  # Если кнопки нет, продолжаем

        # Клик по кнопке "Start"
        register_business_start_button = wait.until(EC.element_to_be_clickable((By.ID, "startBusinessButtonID")))
        register_business_start_button.click()

        # Выбор типа бизнеса
        wait.until(EC.number_of_windows_to_be(2))
        business_type = wait.until(EC.presence_of_element_located((By.ID, "filingType")))
        Select(business_type).select_by_value('DLLC')

        # Заполнение данных компании
        wait.until(EC.presence_of_element_located((By.ID, "busOverview_businessName"))).send_keys(data["business_name"])
        wait.until(EC.presence_of_element_located((By.ID, "busOverview_activityDescription"))).send_keys(data["activity_description"])
        wait.until(EC.presence_of_element_located((By.ID, "busOverview_duration_type_perpetual"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "busOverview_emailAddress_emailAddress"))).send_keys(data["email"])
        wait.until(EC.presence_of_element_located((By.ID, "busOverview_emailAddress_emailAddressVerification"))).send_keys(data["email"])

        # Заполнение адреса для уведомлений
        Select(wait.until(EC.presence_of_element_located((By.ID, "busOverview_principalAddr_country")))).select_by_value('USA')
        wait.until(EC.presence_of_element_located((By.ID, "busOverview_principalAddr_addressLine1"))).send_keys(data["address"])
        wait.until(EC.presence_of_element_located((By.ID, "busOverview_principalAddr_zip"))).send_keys(data["zip"])
        wait.until(EC.presence_of_element_located((By.ID, "busOverview_principalAddr_city"))).send_keys(data["city"])
        Select(wait.until(EC.presence_of_element_located((By.ID, "busOverview_principalAddr_state")))).select_by_value('OR')

        # Продолжение
        wait.until(EC.element_to_be_clickable((By.ID, "pageButton3"))).click()

        # Заполнение контактных данных
        wait.until(EC.presence_of_element_located((By.ID, "busOverview_businessContact_name"))).send_keys(data["contact_name"])
        wait.until(EC.presence_of_element_located((By.ID, "busOverview_businessContact_phone_number"))).send_keys(data["phone"])
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]"))).click()

        # Уведомления по Email
        Select(wait.until(EC.presence_of_element_located((By.ID, "eSelection")))).select_by_value("EMAIL")
        wait.until(EC.presence_of_element_located((By.ID, "contactDetail"))).send_keys(data["contact_name"])
        wait.until(EC.presence_of_element_located((By.ID, "contactEmail"))).send_keys(data["email"])
        wait.until(EC.presence_of_element_located((By.ID, "validateEmail"))).send_keys(data["email"])

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]"))).click()

        # Выбор адреса из списка
        wait.until(EC.element_to_be_clickable((By.ID, "jurisdiction_pplAddrSelectListHrefId"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'selectedOption')]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]"))).click()

        # Заполнение данных агента
        wait.until(EC.element_to_be_clickable((By.ID, "registeredAgent_indvAssocNameEntityType"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "registeredAgent_individual_firstName"))).send_keys(data["agent_first_name"])
        wait.until(EC.presence_of_element_located((By.ID, "registeredAgent_individual_lastName"))).send_keys(data["agent_last_name"])
        wait.until(EC.element_to_be_clickable((By.ID, "registeredAgent_addressSelectListHrefId"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'selectedOption')]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]"))).click()

        # Добавление организатора
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Add Organizer')]"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "organizer_individual_firstName"))).send_keys(data["organizer_first_name"])
        wait.until(EC.presence_of_element_located((By.ID, "organizer_individual_lastName"))).send_keys(data["organizer_last_name"])
        wait.until(EC.element_to_be_clickable((By.ID, "organizer_addressSelectListHrefId"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'selectedOption')]"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "organizer_saveButton"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]"))).click()

        # Завершение регистрации
        wait.until(EC.element_to_be_clickable((By.ID, "goToSignatureButton"))).click()

        return "Регистрация завершена успешно"

    finally:
        driver.quit()
