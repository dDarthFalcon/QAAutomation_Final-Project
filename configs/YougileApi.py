import requests

# Спецификация: https://ru.yougile.com/api-v2?ysclid=lyyr1pb18o308827731#/

class YougileApi:
    # Инициализация 
    def __init__(self, url) -> None:
        self.url = url

    # Получить список компаний   
    def get_company_id_by_name(self, user, company_name=''):
        body = {
            "login": user["login"],
            "password": user["password"],
        }
        if company_name:
            body["name"] = company_name

        response = requests.post(self.url + '/auth/companies', json=body)
        company_list = response.json()

        if company_name:
            return company_list['content'][0]['id']
        else:
            company_ids = [company['id'] for company in company_list['content']]
            return company_ids

    def get_key_list(self, user, company_id):
        body = {
            "login": user["login"],
            "password": user["password"],
            "companyId": company_id
        }
        response = requests.post(self.url + '/auth/keys/get', json=body)
        user_keys_list = response.json()
        return user_keys_list

    def get_key(self, user, company_id):
        body = {
            "login": user["login"],
            "password": user["password"],
            "companyId": company_id
        }
        response = requests.post(self.url + '/auth/keys', json=body)
        new_key = response.json()['key']
        return new_key

    def delete_key(self, key):
        requests.delete(self.url + '/auth/keys/' + str(key))

    def invite_into_company(self, key, user, isAdmin=False):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        body = {
            'email': user["login"],
            'isAdmin': isAdmin
        }
        response = requests.post(self.url + '/users', json=body, headers=req_headers)
        return response

    def get_users_in_company(self, key):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(self.url + '/users', headers=req_headers)
        return response.json()['content']

    def get_user_info_by_id(self, key, user_id):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(self.url + '/users/' + str(user_id), headers=req_headers)
        return response.json()

    def set_isAdmin(self, key, user_id, isAdmin=True):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        body = {
            'isAdmin': isAdmin
        }
        response = requests.put(self.url + '/users/' + str(user_id), json=body, headers=req_headers)
        return response

    def delete_from_company(self, key, user_id):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        requests.delete(self.url + '/users/' + str(user_id), headers=req_headers)

    def get_projects_list(self, key):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        req_params = {
            'includeDeleted': False
        }
        response = requests.get(self.url + '/projects', params=req_params, headers=req_headers)
        return response.json()['content']

    def create_project(self, key, project_name, users=''):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        body = {
            'title': project_name,
        }
        if users:
            body["users"] = users
        response = requests.post(self.url + '/projects', json=body, headers=req_headers)
        return response.json()['id']

    def get_project_info(self, key, project_id):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(self.url + '/projects/' + str(project_id), headers=req_headers)
        return response.json()

    def edit_project(self, key, project_id, project_name='', deleted=False, users=''):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        body = {
            'deleted': deleted
        }
        if project_name:
            body['title'] = project_name
        if users:
            body['users'] = users
        response = requests.put(self.url + '/projects/' + str(project_id), json=body, headers=req_headers)
        return response.json()['id']

    def edit_project2(self, key, project_id, project_name='', deleted=False, users=''):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        body = {
            'deleted': deleted
        }
        if project_name:
            body['title'] = project_name
        if users:
            body['users'] = users
        response = requests.put(self.url + '/projects/' + str(project_id), json=body, headers=req_headers)
        return response

    def create_board(self, key, project_id, board_info):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        body = {
            'title': board_info['title'],  # обязательный параметр
            'projectId': project_id,  # обязательынй параметр
        }
        # Проверка наличия необязательного параметра
        if 'stickers' in board_info:
            body['stickers'] = board_info['stickers']

        response = requests.post(self.url + '/boards', json=body, headers=req_headers)
        return response.json()['id']

    def get_board_info(self, key, board_id):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(self.url + '/boards/' + str(board_id), headers=req_headers)
        return response.json()

    def edit_boards(self, key, project_id, board_id, board_info):
        req_headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        body = {
            'title': board_info['title'],  # обязательный параметр
            'projectId': project_id,  # обязательынй параметр
        }
        # Проверка наличия необязательного параметра
        if 'deleted' in board_info:
            body['deleted'] = board_info['deleted']

        # Проверка наличия необязательного параметра
        if 'stickers' in board_info:
            body['stickers'] = board_info['stickers']

        response = requests.put(self.url + '/boards/' + str(board_id), json=body, headers=req_headers)
        return response.json()['id']

    def delete_users_from_company(self, key):
        all_users = self.get_users_in_company(key)
        all_users_id = [user['id'] for user in all_users if not user['isAdmin']]
        for user_id in all_users_id:
            self.delete_from_company(key, user_id)
