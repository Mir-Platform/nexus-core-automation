from requests.exceptions import HTTPError
from .models.user_model import user_model


class User:

    def __init__(self, session):
        self.session = session
        self.api_location = '/beta/security/users'

    def list(self):
        response = self.session.get(self.api_location)
        users_dict = {}
        for user in response.json():
            users_dict[user['userId']] = user

        return users_dict

    def create(self, **kwargs):
        params = user_model(kwargs)
        try:
            response = self.session.post(f'{self.api_location}', json=params)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR USER CREATE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR USER CREATE OTHER: {err}')
        else:
            print(f'USER CREATED: {str(response.status_code)} {params["userId"]} change default pass {params["password"]}')

    def delete(self, **kwargs):

        userId = kwargs.get('userId')

        try:
            response = self.session.delete(f'{self.api_location}/{userId}')

            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR USER DELETE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR USER DELETE OTHER: {err}')
        else:
            print(f'USER DELETED: {str(response.status_code)} {userId}')

    def update(self, **kwargs):
        params = user_model(kwargs)
        del params['password']
        try:
            response = self.session.put(f'{self.api_location}/{params["userId"]}', json=params)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR USER UPDATE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR USER UPDATE OTHER: {err}')
        else:
            print(f'USER UPDATED: {str(response.status_code)} {params["userId"]}')
