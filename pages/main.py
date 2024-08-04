from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get('https://samokat.ru/')
        self.driver.maximize_window()
        self.wait = WebDriverWait(driver, 5)
        self.driver.implicitly_wait(3)

    def search(self, search_text):
        search_field = self.driver.find_element(By.CSS_SELECTOR, "input")
        search_field.clear()
        search_field.send_keys(search_text)
        while True:
            try:
                self.wait.until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, "div[class*='DesktopShowcase']")
                    )
                )
                input_text = search_field.get_attribute("value")
            except TimeoutException:
                self.driver.refresh()
            return input_text

    def clear_search(self):
        clear_button = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div._clear_184dk_59")
            )
        )
        clear_button = self.driver.find_element(
            By.CSS_SELECTOR, "div._clear_184dk_59"
        )
        clear_button.click()
        search_field = self.driver.find_element(By.CSS_SELECTOR, "input")
        search_field_value = search_field.get_attribute("value")
        return search_field_value if search_field_value is not None else ""

    def set_address(self, city, address):
        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "canvas")
            )).click()

        city_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Город']")
            )
        )
        city_input.send_keys(city)

        city_suggest = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'Suggest')]"
                           " //span[not(contains(text(), 'Город'))]"
                )
            )
        )
        city_suggest.click()

        address_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Улица и дом']")
            )
        )
        address_input.send_keys(address)

        address_suggest = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//div[contains(@class, 'Suggest')]"
                           f"//span[contains(text(), '{address}')]"
                )
            )
        )
        address_suggest.click()

        try:
            confirmation_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(), 'Да, всё верно')]")
                )
            )
            confirmation_button.click()
        except:
            self.driver.find_element(
                By.XPATH, "//span[contains(text(), 'Сюда не доставляем')]"
            )
            return "Некорректный адрес"

    def add_to_cart(self):
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "div[class*='DesktopShowcase']")
                )
        )
        available_products = self.driver.find_elements(
            By.CSS_SELECTOR, "div[class*='increase']"
        )
        available_products_data = []
        for i in range(2):
            product = available_products[i]
            # Добавляем все продукты по 1 шт
            self.driver.execute_script("arguments[0].click();", product)
            # Получить родительский элемент
            parent_element = product.find_element(
                By.XPATH, "./ancestor::div[contains(@class,\
                    'ProductCardActions_root__')]"
            )
            price_element = parent_element.find_elements(
                By.CSS_SELECTOR, "span"
            )[1]
            # Получить цену продукта
            price_text = price_element.text
            # Извлечь только цифры из строки и преобразовать в число
            price_digits = ''.join(filter(str.isdigit, price_text))
            # Добавить продукт в корзину
            if price_digits:  # Проверка, что price_digits не пустой
                price = int(price_digits)
            else:
                price = 0
            available_products_data.append(price)
        return available_products_data

    def get_cart_price(self):
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".drawers"))
        )
        try:
            order_price_element = self.driver.find_element(
                By.XPATH, "//div[contains(@class, 'OrderPrice')]"
                          "//span[contains(text(), '₽')]"
            )
            order_price_text = order_price_element.text
            # Извлечь только цифры из строки и преобразовать в число
            order_price = int(''.join(filter(str.isdigit, order_price_text)))
        except NoSuchElementException:
            try:
                self.driver.refresh()
                order_price_element = self.driver.find_element(
                    By.XPATH, "//div[contains(@class, 'OrderPrice')]"
                              "//span[contains(text(), '₽')]"
                )
                order_price_text = order_price_element.text
                order_price = int(''.join
                                  (filter
                                   (str.isdigit,order_price_text)
                                )
                )
            except NoSuchElementException:
                order_price = 0
        return order_price

    def set_address_loop(self, city, address):
        while True:
            try:
                self._enter_city(city)
                try:
                    error_message = self.wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//span[contains(text(),\
                             'Сюда не доставляем')]")
                        )
                    )
                    if error_message:
                        return "Некорректный адрес"
                except TimeoutException:
                    pass

                self._enter_address(address)
                try:
                    error_message = self.wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//span[contains(text(),\
                             'Сюда не доставляем')]")
                        )
                    )
                    if error_message:
                        return "Некорректный адрес"
                except TimeoutException:
                    pass

                confirmation_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//span[contains(text(), 'Да, всё верно')]")
                    )
                )
                confirmation_button.click()
                self.wait.until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, "div[class*='Drawer_overlay']")
                    )
                )

                address_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, "div[class*='address'] span"
                )
                if address_elements:
                    current_address_parts = []
                    for element in address_elements:
                        current_address_parts.append(element.text.strip())
                    current_address = ' '.join(
                        current_address_parts
                    ).strip().replace(' ,', ',')
                    return current_address

            except TimeoutException:
                self.driver.refresh()

    def _enter_city(self, city):
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas"))
        ).click()

        city_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Город']")
            )
        )
         # Проверка значения параметра value
        current_value = city_input.get_attribute("value")
        if current_value == "Москва":
            return
        city_input.clear()
        city_input.send_keys(city)

        city_suggest = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'Suggest')]"
                           "//span[not(contains(text(), 'Город'))]")
            )
        )
        city_suggest.click()

    def _enter_address(self, address):
        address_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Улица и дом']")
            )
        )
        address_input.clear()
        address_input.send_keys(address)

        address_suggest = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//div[contains(@class, 'Suggest')]"
                           f"//span[contains(text(), '{address}')]")
            )
        )
        address_suggest.click()
