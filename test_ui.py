import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pages.main import MainPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome(service=ChromeService())

@pytest.mark.positive_test
@pytest.mark.ui_test
def test_search():
    ru = 'молоко'  # ввод кириллицы
    eng = 'parmalat'  # ввод латинских символов
    other_lang = '面包'  # ввод иного алфавита
    numbers = '200'  # ввод цифр
    special_char = '!"№;%:?*()_+'  # ввод спецсимволов
    space = ' '  # пробел
    two_words = 'пластовой творог'  # 2 слова
    search_texts = [ru, eng, other_lang, numbers, special_char, space, two_words]
    main_page = MainPage(browser)

    for search_text in search_texts:
        with allure.step(f"Ввод запроса в строку поиска: {search_text}"):
            returned_text = main_page.search(search_text)  # записываем в переменную текст, который отображается в поле ввода
            assert returned_text == search_text  # сравниваем текст, который отправлял, с тем, что был отображен на экране

@pytest.mark.positive_test
@pytest.mark.ui_test
def test_clear_search():
    main_page = MainPage(browser)
    search_text = 'сырники'  # искомый текст в каталоге

    with allure.step("Поиск товара по каталогу"):
        main_page.search(search_text)  # делаем поиск по каталогу
    
    with allure.step("Очищаем поле поиска"):
        cleared_text = main_page.clear_search()  # нажимаем на кнопку, отвечающую за очистку поля поиска
        assert cleared_text == ''

@pytest.mark.positive_test
@pytest.mark.ui_test
def test_input_valid_address():
    city = 'Москва'  # указываем город, где есть работающие дарксторы
    address = 'Театральная площадь, 1'  # указываем улицу, куда возможна доставка
    main_page = MainPage(browser)

    with allure.step("Устанавливаем валидный адрес"):
        result = main_page.set_address_loop(city, address)
        assert result == address

        browser.delete_all_cookies()  # очищаем куки для корректной работы следующих тестов
        browser.refresh()  # обновляем страницу после удаления куки

@pytest.mark.negative_test
@pytest.mark.ui_test
def test_input_invalid_street():
    city = 'Москва'  # указываем город, где есть работающие дарксторы
    address = 'деревня Бачурино, 36'  # указываем улицу, куда заведомо невозможна доставка
    main_page = MainPage(browser)

    with allure.step("В качестве адреса доставки выбираем некорректную улицу"):
        result = main_page.set_address_loop(city, address)
        assert result == "Некорректный адрес"  # т.к. main_page.set_address_loop возвращает "Некорректный адрес", если доставка невозможна по указанному адресу

        browser.delete_all_cookies()  # очищаем куки для корректной работы следующих тестов
        browser.refresh()  # обновляем страницу после удаления куки

@pytest.mark.negative_test
@pytest.mark.ui_test
def test_input_invalid_city():
    city = 'Клин'  # указываем город, где нет дарксторов
    address = 'Советская площадь, 21'  # указываем улицу в городе
    main_page = MainPage(browser)

    with allure.step("В качестве адреса доставки выбираем некорректный город"):
        result = main_page.set_address_loop(city, address)
        assert result == "Некорректный адрес"  # т.к. main_page.set_address_loop возвращает "Некорректный адрес", если доставка невозможна по указанному адресу

        browser.delete_all_cookies()  # очищаем куки для корректной работы следующих тестов
        browser.refresh()  # обновляем страницу после удаления куки

@pytest.mark.positive_test
@pytest.mark.ui_test
def test_total_price_in_cart():
    city = 'Москва'
    address = 'Театральная площадь, 1'
    search_text = 'Творог рассыпчатый 200'
    main_page = MainPage(browser)

    with allure.step("Указываем валидный адрес доставки"):
        main_page.set_address_loop(city, address)  # шаг 1: указать корректный адрес доставки

    with allure.step("Ищем продукты"):
        main_page.search(search_text)  # шаг 2: найти что-нибудь в каталоге, для отображения возможных к покупке товаров

    with allure.step("Добавляем найденные продукты в каталог"):
        result = main_page.add_to_cart()  # шаг 3: добавить найденные товары в корзину
        total_product_price = sum(result)  # шаг 3.1: посчитать стоимость товаров, которые мы добавили в корзину

    with allure.step("Проверям стоимость добавленных продуктов и величину стоимости корзины"):
        cart_value = main_page.get_cart_price()  # шаг 4: узнать общую стоимость товаров в корзине
        assert cart_value == total_product_price

        browser.delete_all_cookies()  # очищаем куки для корректной работы следующих тестов
        browser.refresh()  # обновляем страницу после удаления куки
