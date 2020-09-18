from requests.exceptions import HTTPError
from .models.role_model import role_model


class Role:

    def __init__(self, session):
        self.session = session
        self.api_location = '/beta/security/roles'

    def list(self):
        response = self.session.get(self.api_location)
        role_dict = {}
        for role in response.json():
            if role['source'] != 'LDAP':
                role_dict[role['name']] = role

        return role_dict

    def create(self, **kwargs):
        # TODO: only files, we do not have S3
        params = role_model(kwargs)
        try:
            response = self.session.post(f'{self.api_location}', json=params)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR ROLE CREATE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR ROLE CREATE OTHER: {err}')
        else:
            print(f'ROLE CREATED: {str(response.status_code)} {params["name"]}')

    def update(self, **kwargs):
        params = role_model(kwargs)

        try:
            response = self.session.put(f'{self.api_location}/{params["name"]}', json=params)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR ROLE UPDATE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR ROLE UPDATE OTHER: {err}')
        else:
            print(f'ROLE UPDATED: {str(response.status_code)} {params["name"]}')

    def delete(self, **kwargs):

        name = kwargs.get('name')

        try:
            response = self.session.delete(f'{self.api_location}/{name}')

            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR ROLE DELETE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR ROLE DELETE OTHER: {err}')
        else:
            print(f'ROLE DELETED: {str(response.status_code)} {name}')
