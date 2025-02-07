import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import tempfile




def fill_form_oregon(credentials, data) -> str:
    """
    Заполняет форму регистрации на сайте sos.oregon.gov с использованием Selenium.
    Возвращает response, полученный после успешной отправки формы.
    """
    options = Options()
    # Создаем уникальный временный каталог для каждого запуска
    temp_dir = tempfile.mkdtemp()


    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # Открытие сайта
        driver.get("https://sos.oregon.gov/")
        
        # Нажатие на кнопку "Register a Business"
        register_business_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register a Business")))
        register_business_button.click()

        # Ожидание появления нового окна и переключение на него
        wait.until(EC.number_of_windows_to_be(2))
        windows = driver.window_handles
        driver.switch_to.window(windows[1])

        # Нажатие на кнопку "New User"
        log_in_button = wait.until(EC.element_to_be_clickable((By.ID, "loginButton")))
        log_in_button.click()

        # Авторизация
        login = wait.until(EC.presence_of_element_located((By.ID, "username")))
        login.send_keys(credentials.login)
        password = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password.send_keys(credentials.password)
        login_button = driver.find_element(By.NAME, "Login")
        login_button.click()

        time.sleep(20)
        #  ВАЖНО!!! Если ранее не были созданы шаблоны с этого акка, то строки 43-47 нужно удалить
        cancel_button = wait.until(EC.element_to_be_clickable((By.ID, "cancelButton"))) 
        cancel_button.click()  




        # Клик по кнопке Start
        register_business_start_button =  wait.until(EC.element_to_be_clickable((By.ID, "startBusinessButtonID")))
        register_business_start_button.click()

        wait.until(EC.number_of_windows_to_be(2))
        register_name_button = driver.find_element(By.ID, "startBusRegBtn")
        register_name_button.click()
        wait.until(EC.number_of_windows_to_be(2))

        # Выбор типа бизнеса
        business_type = driver.find_element(By.ID, "filingType")
        business_type.click()
        dllc_option = driver.find_element(By.XPATH, "//option[@value='DLLC']")
        dllc_option.click()
        wait.until(EC.number_of_windows_to_be(2))

        # Заполнение данных компании
        business_name_textarea = driver.find_element(By.ID, "busOverview_businessName")
        business_name_textarea.send_keys("Oregon Test LLC")
        activity_description_textarea = driver.find_element(By.ID, "busOverview_activityDescription")
        activity_description_textarea.send_keys("This is a description of the business activity.")
        perpetual_radio = driver.find_element(By.ID, "busOverview_duration_type_perpetual")
        perpetual_radio.click()

        email_input = driver.find_element(By.ID, "busOverview_emailAddress_emailAddress")
        email_input.send_keys("johndoe@example.com")
        reenter_email_input = driver.find_element(By.ID, "busOverview_emailAddress_emailAddressVerification")
        reenter_email_input.send_keys("johndoe@example.com")

        # Заполнение адреса для уведомлений
        country_select = driver.find_element(By.ID, "busOverview_principalAddr_country")
        Select(country_select).select_by_value('USA')
        address_input = driver.find_element(By.ID, "busOverview_principalAddr_addressLine1")
        address_input.send_keys("1234 Main St")
        zip_input = driver.find_element(By.ID, "busOverview_principalAddr_zip")
        zip_input.send_keys("97201")
        city_input = driver.find_element(By.ID, "busOverview_principalAddr_city")
        city_input.send_keys("Portland")
        state_select = driver.find_element(By.ID, "busOverview_principalAddr_state")
        Select(state_select).select_by_value('OR')

        time.sleep(20)
        continue_button = driver.find_element(By.ID, "pageButton3")
        continue_button.click()

        # Заполнение контактных данных
        name_input = driver.find_element(By.ID, "busOverview_businessContact_name")
        name_input.send_keys("John Doe")
        phone_input = driver.find_element(By.ID, "busOverview_businessContact_phone_number")
        phone_input.send_keys("5031234567")
        continue_button = driver.find_element(By.XPATH, "//span[contains(text(),'Continue')]")
        continue_button.click()

        time.sleep(20)
        # Заполнение данных уведомлений (Email)
        notification_select = Select(wait.until(EC.presence_of_element_located((By.ID, "eSelection"))))
        notification_select.select_by_value("EMAIL")
        contact_name_input = wait.until(EC.presence_of_element_located((By.ID, "contactDetail")))
        contact_name_input.send_keys("John Doe")
        contact_email_input = wait.until(EC.presence_of_element_located((By.ID, "contactEmail")))
        contact_email_input.send_keys("johndoe@example.com")
        reenter_email_input = wait.until(EC.presence_of_element_located((By.ID, "validateEmail")))
        reenter_email_input.send_keys("johndoe@example.com")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]")))
        continue_button.click()

        time.sleep(20)
        # Выбор адреса из списка
        select_from_list_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "jurisdiction_pplAddrSelectListHrefId"))
        )
        select_from_list_button.click()
        first_address_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, \"selectedOption(cbrPageObj.addressArray[0]\")]"))
        )
        first_address_option.click()
        continue_button = driver.find_element(By.XPATH, "//span[contains(text(),'Continue')]")
        continue_button.click()

        time.sleep(20)
        # Заполнение данных для зарегистрированного агента
        individual_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "registeredAgent_indvAssocNameEntityType"))
        )
        individual_radio.click()
        first_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "registeredAgent_individual_firstName"))
        )
        first_name_input.send_keys("John")
        last_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "registeredAgent_individual_lastName"))
        )
        last_name_input.send_keys("Doe")
        select_from_list_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "registeredAgent_addressSelectListHrefId"))
        )
        select_from_list_button.click()
        first_address_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, \"selectedOption(cbrPageObj.addressOROnlyArray[0]\")]"))
        )
        first_address_option.click()
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]"))
        )
        continue_button.click()

        time.sleep(20)
        # Добавление организатора
        add_organizer_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Add Organizer')]"))
        )
        add_organizer_button.click()
        first_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "organizer_individual_firstName"))
        )
        first_name_input.send_keys("John")
        last_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "organizer_individual_lastName"))
        )
        last_name_input.send_keys("Doe")
        select_from_list_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "organizer_addressSelectListHrefId"))
        )
        select_from_list_button.click()
        first_address_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, \"selectedOption(cbrPageObj.addressArray[0]\")]"))
        )
        first_address_option.click()
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "organizer_saveButton"))
        )
        save_button.click()
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]"))
        )
        continue_button.click()

        time.sleep(20)
        # Добавление лица с прямыми знаниями
        add_individual_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "indDirectKnowledge_multiObjectAdd"))
        )
        add_individual_button.click()
        first_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "indDirectKnowledge_individual_firstName"))
        )
        first_name_input.send_keys("John")
        middle_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "indDirectKnowledge_individual_middleName"))
        )
        middle_name_input.send_keys("Michael")
        last_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "indDirectKnowledge_individual_lastName"))
        )
        last_name_input.send_keys("Doe")
        select_address_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "indDirectKnowledge_addressSelectListHrefId"))
        )
        select_address_button.click()
        select_first_address = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'selectedOption')]"))
        )
        select_first_address.click()
        time.sleep(20)
        save_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "indDirectKnowledge_saveButton"))
        )
        try:
            save_button.click()
        except Exception:
            print("Не удалось кликнуть стандартным способом, пробуем JavaScript")
            driver.execute_script("arguments[0].click();", save_button)
        time.sleep(20)
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]"))
        )
        continue_button.click()

        time.sleep(20)
        # Выбор управления участниками
        member_managed_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "management_trueType"))
        )
        member_managed_radio.click()
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue')]"))
        )
        continue_button.click()
        add_initial_memb = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "memberManager_addMemberManagersNo"))
        )
        add_initial_memb.click()
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue')]"))
        )
        continue_button.click()
        time.sleep(20)
        llcr = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "professionalServices_falseType"))
        )
        llcr.click()
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue')]"))
        )
        continue_button.click()
        time.sleep(20)
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue')]"))
        )
        continue_button.click()
        time.sleep(20)
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue')]"))
        )
        continue_button.click()
        gtsb = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "goToSignatureButton"))
        )
        gtsb.click()
        time.sleep(20)
        # Выбор титула
        title_select = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "selectTitleHref0"))
        )
        title_select.click()
        organizer_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Authorized Agent')]"))
        )
        organizer_option.click()
        time.sleep(20)
        title_select = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "selectNameHref0"))
        )
        title_select.click()
        manager_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'John Doe')]"))
        )
        manager_option.click()
        time.sleep(20)
        # Подписание
        sign_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signatureCheckBox0"))
        )
        sign_checkbox.click()
        print("Галочка Sign установлена")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Submit')]"))
        )
        submit_button.click()
        ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "pageButton1"))
        )
        ok_button.click()
        

        # возвращаем JSON с подтверждением
        response = {
            "registration_completed": True,
            "message": "Registration successful"
        }

        return response

    finally:
        driver.quit()

def fill_form(state: str, credentials, data) -> str:
    """
    Выбирает обработчик заполнения формы по штату.
    В данном примере реализован только для штата Орегон (OR).
    """
    if state.upper() == "OR":
        return fill_form_oregon(credentials, data)
    else:
        raise ValueError(f"Обработка для штата {state} не реализована.")
