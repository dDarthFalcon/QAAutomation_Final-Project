import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from pages.main import MainPage

browser = webdriver.Chrome(service=ChromeService())


@pytest.mark.positive_test
@pytest.mark.ui_test
# Тест работы поля поиска
def test_search():
    ru = 'молоко'  # ввод кириллицы
    eng = 'parmalat'  # ввод латинских символов
    other_lang = '面包'  # ввод иного алфавита
    numbers = '200'  # ввод цифр
    special_char = '!"№;%:?*()_+'  # ввод спецсимволов
    space = ' '  # пробел
    two_words = 'пластовой творог'  # 2 слова
    search_texts = [ru, eng, other_lang, numbers,
                    special_char, space, two_words]
    main_page = MainPage(browser)

    for search_text in search_texts:
        with allure.step(f"Ввод запроса в строку поиска: {search_text}"):
            # записываем в переменную текст, который отображается в поле ввода
            returned_text = main_page.search(search_text)
            # сравниваем запрос с тем, что отображено на экране
            assert returned_text == search_text


@pytest.mark.positive_test
@pytest.mark.ui_test
# Тест работы кнопки очистки поискового запроса
def test_clear_search():
    main_page = MainPage(browser)
    search_text = 'сырники'  # искомый текст в каталоге

    with allure.step("Поиск товара по каталогу"):
        # делаем поиск по каталогу
        main_page.search(search_text)

    with allure.step("Очищаем поле поиска"):
        # нажимаем на кнопку, отвечающую за очистку поля поиска
        cleared_text = main_page.clear_search()
        assert cleared_text == ''


@pytest.mark.positive_test
@pytest.mark.ui_test
# Тест ввода валидного адреса (куда возможна доставка)
def test_input_valid_address():
    # указываем город, где есть работающие дарксторы
    city = 'Москва'
    # указываем улицу, куда возможна доставка
    address = 'Театральная площадь, 1'
    main_page = MainPage(browser)

    with allure.step("Устанавливаем валидный адрес"):
        result = main_page.set_address_loop(city, address)
        assert result == address

        # очищаем куки для корректной работы следующих тестов
        browser.delete_all_cookies()
        # обновляем страницу после удаления куки
        browser.refresh()


@pytest.mark.negative_test
@pytest.mark.ui_test
# Тест ввода НЕвалидной улицы (куда НЕвозможна доставка)
def test_input_invalid_street():
    # указываем город, где есть работающие дарксторы
    city = 'Москва'
    # указываем улицу, куда заведомо невозможна доставка
    address = 'деревня Бачурино, 36'
    main_page = MainPage(browser)

    with allure.step("В качестве адреса доставки выбираем некорректную улицу"):
        result = main_page.set_address_loop(city, address)
        assert result == "Некорректный адрес"

        # очищаем куки для корректной работы следующих тестов
        browser.delete_all_cookies()
        # обновляем страницу после удаления куки
        browser.refresh()


@pytest.mark.negative_test
@pytest.mark.ui_test
# Тест ввода НЕвалидного города (куда НЕвозможна доставка)
def test_input_invalid_city():
    city = 'Клин'  # указываем город, где нет дарксторов
    address = 'Советская площадь, 21'  # указываем улицу в городе
    main_page = MainPage(browser)

    with allure.step("В качестве адреса доставки выбираем некорректный город"):
        result = main_page.set_address_loop(city, address)
        assert result == "Некорректный адрес"

        # очищаем куки для корректной работы следующих тестов
        browser.delete_all_cookies()
        # обновляем страницу после удаления куки
        browser.refresh()


@pytest.mark.positive_test
@pytest.mark.ui_test
# Тест корректного расчета стоимости корзины
def test_total_price_in_cart():
    city = 'Москва'
    address = 'Театральная площадь, 1'
    search_text = 'молоко'
    main_page = MainPage(browser)

    # указать корректный адрес доставки
    with allure.step("Указываем валидный адрес доставки"):
        main_page.set_address_loop(city, address)

    # найти что-нибудь в каталоге, для отображения возможных к покупке товаров
    with allure.step("Ищем продукты"):
        main_page.search(search_text)

    # добавить найденные товары в корзину
    with allure.step("Добавляем найденные продукты в каталог"):
        result = main_page.add_to_cart()
        # шаг 3.1: посчитать стоимость товаров, которые мы добавили в корзину
        total_product_price = sum(result)

    # узнать общую стоимость товаров в корзине
    with allure.step("Проверка стоимости корзины и добавленных товаров"):
        cart_value = main_page.get_cart_price()
        assert cart_value == total_product_price

        # очищаем куки для корректной работы следующих тестов
        browser.delete_all_cookies()
        # обновляем страницу после удаления куки
        browser.refresh()
