# QAAutomation Final Project

<details>
<summary>Блок 1. Yougile API Autotest</summary>

## Описание

Проект предназначен для автоматизации тестирования API сервиса Yougile. Тесты охватывают различные аспекты работы с API, такие как авторизация, управление пользователями и проектами.

## Структура проекта

- `configs/`: Директория, содержащая файлы `YougileApi` и `config.py`.
  - `YougileApi.py` — модуль, содержащий класс `YougileApi` для взаимодействия с API Yougile.
  - `config.py` — файл конфигурации, содержащий данные для тестов (учетные данные пользователей).
- `pages/`: Директория, содержащая файл `loginPage.py`.
  - `loginPage.py` — модуль, содержащий класс `LoginPage` для взаимодействия с UI Yougile и используемый в рамках api-тестов.
- `requirements.txt`: Файл с зависимостями проекта.
- `test_api.py`: Файл с тестами для проверки API Yougile.
- - `README.md`: Документация проекта

## Установка

1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/dDarthFalcon/QAAutomation_Final-Project.git
    ```

2. Перейдите в директорию проекта:

    ```sh
    cd QAAutomation_Final-Project
    ```

3. Установите необходимые зависимости:

    ```sh
    pip install -r requirements.txt
    ```

## Настройка

Для работы с API необходимы учетные данные, которые можно указать в файле `config.py`.


## Запуск тестов

Для запуска тестов с генерацией отчета Allure выполните следующие шаги:

1. Запустите тесты с использованием `pytest` и сохраните результаты в формате, понятном для Allure:

    ```sh
    pytest test_api.py --alluredir=allure-results
    ```

2. Сгенерируйте отчет Allure:

    ```sh
    allure generate allure-results --clean -o allure-report
    ```

3. Откройте отчет в браузере:

    ```sh
    allure open allure-report
    ```

## Примеры тестов

Все автоматизированные API тесты находятся в файле `test_api.py`. Вот несколько примеров того, как выглядят тесты:

- `test_invite_to_company.py` — тест для приглашения пользователей в компанию.
- `test_create_project.py` — тест по созданию проектов.
- `test_switch_to_admin.py` — тест для изменения статуса пользователей на администратора.



</details>


<details>
<summary>Блок 2. "Самокат" UI Autotest</summary>

## Описание

Этот проект направлен на автоматизацию UI-тестирования сайта Самокат с использованием Selenium WebDriver и Pytest. Тесты охватывают различные функции, такие как поиск товаров, установка адреса доставки, очистка поля поиска и проверка общей стоимости корзины.

Тест-план по ручному тестированию проекта [тут](https://large-macrame-686.notion.site/8e68417cc71a44e5a293ba863823c29d?pvs=4).

## Структура проекта

- `pages/`: Директория, содержащая файл `main.py`.
  - `main.py` — Модель страницы (Page Object Model) для главной страницы.
- `requirements.txt`: Файл с зависимостями проекта.
- `test_ui.py`: UI-тесты с использованием pytest.
- `README.md`: Документация проекта

## Установка

1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/dDarthFalcon/QAAutomation_Final-Project.git
    ```

2. Перейдите в директорию проекта:

    ```sh
    cd QAAutomation_Final-Project
    ```

3. Установите необходимые зависимости:

    ```sh
    pip install -r requirements.txt
    ```

## Запуск тестов

Для запуска тестов с генерацией отчета Allure выполните следующие шаги:

1. Запустите тесты с использованием `pytest` и сохраните результаты в формате, понятном для Allure:

    ```sh
    pytest test_ui.py --alluredir=allure-results
    ```

2. Сгенерируйте отчет Allure:

    ```sh
    allure generate allure-results --clean -o allure-report
    ```

3. Откройте отчет в браузере:

    ```sh
    allure open allure-report
    ```

## Описание тестов

Все автоматизированные UI тесты находятся в файле `test_ui.py`:

- `test_invite_to_company.py` — тест для приглашения пользователей в компанию.
- `test_search`: Тестирует поиск товаров с использованием различных типов ввода (кириллица, латиница, другие алфавиты, цифры, специальные символы, пробелы и запросы из двух слов).
- `test_clear_search`: Тестирует очистку поля поиска после выполнения поиска.
- `test_input_valid_address`: Тестирует установку валидного адреса для доставки.
- `test_input_invalid_street`: Тестирует установку недопустимого адреса улицы, по которому доставка невозможна.
- `test_input_invalid_city`: Тестирует установку недопустимого города, в котором нет доставки.
- `test_total_price_in_cart`: Тестирует добавление товаров в корзину и проверку общей стоимости, соответствующей сумме отдельных товаров.

</details>

<details>

<summary>Используемые маркеры pytest</summary>
  
Поддерживается запуск тестов с маркерами pytest:

1. Все тесты:

    ```sh
    pytest
    ```

2. Только позитивные тесты:

    ```sh
    pytest -m positive_test
    ```

3. Только негативные тесты:

    ```sh
    pytest -m negative_test
    ```

4. Только api тесты:

    ```sh
    pytest -m ui_test
    ```

5. Только ui тесты:

    ```sh
    pytest -m api_test
    ```

Возможно сочетание с командой по генерации отчетов Allure

</details>
