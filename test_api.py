import pytest
import allure
from configs.YougileApi import YougileApi
from configs.config import user1, user2, user3
from pages.loginPage import LoginPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from faker import Faker


api = YougileApi("https://yougile.com/api-v2")

project_name = "Test Project"

# Генерируем случайное название компании
fake = Faker("ru_RU")
company_name = fake.company()

# Фикстура для сессии pytest-тестов
# При запуске теста, через ui создается компания со случайным именем
# и генерируется ключ api, которые будут использоваться в самих тестах
# После завершения тестов удаляется компания и ключ


@pytest.fixture(scope='session', autouse=True)
def new_test_start():
    # Создаем экземпляр браузера
    browser = webdriver.Chrome(service=ChromeService())

    page = LoginPage(browser)
    page.login(user1)
    page.add_company(company_name)

    # Узнаем текущий id компании по её названию
    company_id = api.get_company_id_by_name(user1, company_name)
    print(company_id)

    # Запрашиваем токен администратора
    admin_key = api.get_key(user1, company_id)
    print(admin_key)

    # Передаем данные в тесты
    yield admin_key, company_id

    # Удаляем компанию после завершения всех тестов
    page.delete_company(company_name)
    api.delete_key(admin_key)
    browser.quit()


@pytest.mark.positive_test
@pytest.mark.api_test
def test_invite_to_company(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Пригласить пользователя в компанию"):
        new_user = api.invite_into_company(admin_key, user2)
        new_user_id = new_user.json()['id']

    with allure.step("Получить список пользователей в компании"):
        user_list = api.get_users_in_company(admin_key)
        users_id = [item['id'] for item in user_list]

    with allure.step("Проверить, что новый пользователь есть в списке"):
        assert new_user_id in users_id

    # Удаляем добавленного пользователя
    api.delete_from_company(admin_key, new_user_id)


@pytest.mark.positive_test
@pytest.mark.api_test
def test_removes_from_company(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Пригласить пользователя в компанию"):
        new_user = api.invite_into_company(admin_key, user2)
        if new_user.status_code in (200, 201):
            new_user = new_user.json()

            with allure.step("Удалить нового пользователя из компании"):
                api.delete_from_company(admin_key, new_user['id'])

            with allure.step("Получить список пользователей в компании"):
                user_list = api.get_users_in_company(admin_key)
                users_id = [item['id'] for item in user_list]

            with allure.step("Проверка отсутствия пользователя"):
                assert new_user['id'] not in users_id
        else:
            pytest.skip("Skip: Пользователь не был добавлен в компанию")


@pytest.mark.positive_test
@pytest.mark.api_test
def test_switch_to_admin_for_user(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Пригласить пользователя в компанию"):
        new_user = api.invite_into_company(admin_key, user2)
        if new_user.status_code in (200, 201):
            new_user = new_user.json()

            with allure.step("Проверить, что пользователь не администратор"):
                user_info = api.get_user_info_by_id(admin_key, new_user['id'])
                user_admin_status = user_info['isAdmin']
                if user_admin_status is False:
                    api.set_isAdmin(admin_key, new_user['id'])

                    with allure.step("isAdmin=True?"):
                        user_info = api.get_user_info_by_id(admin_key,
                                                            new_user['id'])
                        user_admin_status = user_info['isAdmin']
                        assert user_admin_status is True

                    api.delete_from_company(admin_key, new_user['id'])
                else:
                    api.delete_from_company(admin_key, new_user['id'])
                    pytest.skip("Пользователь был администратором")
        else:
            pytest.skip("Пользователь не был добавлен в компанию")


@pytest.mark.positive_test
@pytest.mark.api_test
def test_switch_to_noAdmin_for_user(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Пригласить пользователя-администратора"):
        new_user = api.invite_into_company(admin_key, user2, isAdmin=True)
        if new_user.status_code in (200, 201):
            new_user = new_user.json()

            with allure.step("Проверить, что пользователь администратор"):
                user_info = api.get_user_info_by_id(admin_key, new_user['id'])
                user_admin_status = user_info['isAdmin']
                if user_admin_status is True:

                    with allure.step("Изменить на isAdmin=False"):
                        api.set_isAdmin(admin_key, new_user['id'],
                                        isAdmin=False)

                    with allure.step("Проверить, что isAdmin=False?"):
                        user_info = api.get_user_info_by_id(admin_key,
                                                            new_user['id'])
                        user_admin_status = user_info['isAdmin']
                        assert user_admin_status is False

                    api.delete_from_company(admin_key, new_user['id'])
                else:
                    api.delete_from_company(admin_key, new_user['id'])
                    pytest.skip("Skip: Пользователь не был администратором")
        else:
            pytest.skip("Skip: Пользователь не был добавлен в компанию")


@pytest.mark.positive_test
@pytest.mark.api_test
def test_create_project_by_admin(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Создать проект администратором"):
        new_project = api.create_project(admin_key, project_name)

    with allure.step("Получить список проектов"):
        projects_list = api.get_projects_list(admin_key)
        projects_list_id = [project['id'] for project in projects_list]

    with allure.step("Проверить, что проект создан"):
        assert new_project in projects_list_id

    with allure.step("Удалить созданный проект"):
        api.edit_project(admin_key, new_project, project_name='', deleted=True)


@pytest.mark.positive_test
@pytest.mark.api_test
def test_create_project_by_user(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Пригласить пользователя в компанию"):
        user = api.invite_into_company(admin_key, user2)
        new_user_id = user.json()['id']

    with allure.step("Получить токен пользователя"):
        user_key = api.get_key(user2, company_id)

    with allure.step("Создать проект пользователем"):
        new_project = api.create_project(user_key, project_name)

    with allure.step("Получить список проектов"):
        projects_list = api.get_projects_list(admin_key)
        projects_list_id = [project['id'] for project in projects_list]

    with allure.step("Проверить, что проект создан"):
        assert new_project in projects_list_id

    with allure.step("Удалить созданный проект"):
        api.edit_project(admin_key, new_project, project_name='', deleted=True)

    with allure.step("Удалить пользователя из компании"):
        api.delete_from_company(admin_key, new_user_id)
        api.delete_key(user_key)


@pytest.mark.positive_test
@pytest.mark.api_test
def test_delete_project_by_admin(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Создать проект администратором"):
        new_project = api.create_project(admin_key, project_name)

    with allure.step("Получить список проектов"):
        projects_list = api.get_projects_list(admin_key)
        projects_list_id = [project['id'] for project in projects_list]

    if new_project in projects_list_id:
        with allure.step("Удалить созданный проект"):
            api.edit_project(admin_key, new_project, project_name='',
                             deleted=True)

        with allure.step("Получить обновленный список проектов"):
            projects_list = api.get_projects_list(admin_key)
            projects_list_id = [project['id'] for project in projects_list]

        with allure.step("Проверить, что проект удален"):
            assert new_project not in projects_list_id
    else:
        pytest.skip("Тест пропущен: Проект не был создан")


@pytest.mark.negative_test
@pytest.mark.api_test
def test_delete_project_by_user(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Создать проект администратором"):
        new_project = api.create_project(admin_key, project_name)

    with allure.step("Пригласить пользователя в компанию"):
        user = api.invite_into_company(admin_key, user2)
        new_user_id = user.json()['id']

    with allure.step("Получить токен пользователя"):
        user_key = api.get_key(user2, company_id)

    with allure.step("Попытаться удалить проект пользователем"):
        edit_response = api.edit_project2(user_key, new_project,
                                          project_name='', deleted=True)

    with allure.step("Получить список проектов"):
        projects_list = api.get_projects_list(admin_key)
        projects_list_id = [project['id'] for project in projects_list]

    with allure.step("Проверить, что проект не удален"):
        assert edit_response.status_code not in (200, 201) or \
            edit_response.json()['id'] in projects_list_id

    with allure.step("Удалить пользователя и проект"):
        api.delete_from_company(admin_key, new_user_id)
        api.edit_project(admin_key, new_project, project_name='', deleted=True)
        api.delete_key(user_key)


@pytest.mark.negative_test
@pytest.mark.api_test
def test_invite_users_by_user(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Пригласить пользователя в компанию"):
        add_user2 = api.invite_into_company(admin_key, user2)
        user2_id = add_user2.json()['id']

    with allure.step("Получить токен пользователя"):
        user_key = api.get_key(user2, company_id)

    with allure.step("Попытаться пригласить другого пользователя"):
        add_user3 = api.invite_into_company(user_key, user3)

    with allure.step("Получить список пользователей в компании"):
        user_list = api.get_users_in_company(admin_key)
        users_id = [item['id'] for item in user_list]

    with allure.step("Проверить, что приглашение не сработало"):
        assert add_user3.status_code not in (200, 201) or \
            add_user3.json()['id'] not in users_id

    api.delete_from_company(admin_key, user2_id)
    api.delete_key(user_key)


@pytest.mark.negative_test
@pytest.mark.api_test
def test_change_isAdmin_by_user(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Пригласить пользователя в компанию"):
        add_user = api.invite_into_company(admin_key, user3)
        user_id = add_user.json()['id']

    with allure.step("Получить токен пользователя"):
        user_key = api.get_key(user3, company_id)

    with allure.step("Изменить статус пользователя на администратора"):
        resp = api.set_isAdmin(user_key, user_id, isAdmin=True)

    with allure.step("Проверить, что изменение статуса не сработало"):
        assert resp.status_code not in (200, 201)

    # Удаляем нового пользователя и ключ
    api.delete_from_company(admin_key, user_id)
    api.delete_key(user_key)


@pytest.mark.negative_test
@pytest.mark.api_test
def test_use_deleted_key(new_test_start):
    admin_key, company_id = new_test_start
    with allure.step("Получить новый токен администратора"):
        last_admin_key = api.get_key(user1, company_id)

    with allure.step("Удалить ключ"):
        api.delete_key(last_admin_key)

    with allure.step("Пригласить пользователя удаленным ключом"):
        add_user1 = api.invite_into_company(last_admin_key, user2,
                                            isAdmin=True)

    with allure.step("Проверить, что приглашение не сработало"):
        assert add_user1.status_code not in (200, 201)
