from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get('https://ru.yougile.com/team/')
        self.driver.maximize_window()
        self.wait = WebDriverWait(driver, 5)

    # Авторизация на сайте
    def login(self, user):
        # Ищем поле для ввода логина (эл почта)
        email_field = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              "[type='email']"))
                                              )
        email_field.clear()
        # Отправляем на сервер логин пользователя
        email_field.send_keys(user['login'])

        # Ищем поле для ввода пароля от аккаунта
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              "[type='password']"))
                                              )
        password_field.clear()
        # Отправляем на сервер пароль пользователя
        password_field.send_keys(user['password'])

        # Нажимаем "Войти"
        accept_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '[role="button"]'))
                                        )
        accept_button.click()

    # Создание новой компании
    def add_company(self, company_name):
        # Переходим на настройки профиля
        go_settings = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(text(), 'Мой профиль')]")))
        go_settings.click()

        # Ищем кнопку "Добавить компанию"
        add_company = self.driver.find_element(
            By.XPATH, "//div[contains(text(), 'Добавить компанию')]"
        )
        # Прокрутка страницы до кнопки "Добавить компанию"
        self.driver.execute_script("arguments[0].scrollIntoView();",
                                   add_company)
        add_company.click()

        # Вводим название компании
        input_name = self.wait.until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, "input[class='add-company__input']")))
        input_name.send_keys(company_name)

        # Нажимаем "добавить компанию"
        accept_button = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".add-company__submit")
            )
        )
        accept_button.click()

        # Ждем появления сообщения "компания успешно добавлена"
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".fa-check"))
        )
        self.driver.refresh()

    # Удаление компании по её названию
    def delete_company(self, company_name):
        # Переходим на настройки профиля
        go_settings = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), 'Мой профиль')]")
            )
        )
        go_settings.click()

        # Ищем кнопку "Удалить" для компании по указанному названию
        xpath = (
            f"//div[contains(text(), '{company_name}')] \
                /ancestor::div[contains(@class, "
            "'relative') and contains(@class, 'h-32')] \
                /descendant::div[contains(@class, "
            "'active:text-error-old')]"
        )
        del_button = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("arguments[0].scrollIntoView();",
                                   del_button)
        del_button.click()

        # Нажимаем кнопку для подтверждения удаления
        accept = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[text()='Удалить']")
            )
        )
        accept.click()

        # Ждем появления сообщения "компания успешно удалена"
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".fa-check"))
        )
