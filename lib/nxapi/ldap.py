from requests.exceptions import HTTPError
from .models.ldap_model import ldap_model


class Ldap:

    def __init__(self, session):
        self.session = session
        self.api_location = '/beta/security/ldap'

    def list(self):
        ldap_dict = {}

        try:
            response = self.session.get(self.api_location)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR LDAP LIST HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR LDAP LIST OTHER: {err}')
        else:
            print(f'LDAP LISTED: {str(response.status_code)}')

        for ldap in response.json():
            ldap_dict[ldap['name']] = ldap

        return ldap

    def delete(self, **kwargs):
        name = kwargs.get('name')

        try:
            response = self.session.delete(f'{self.api_location}/{name}')
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR LDAP DELETE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR LDAP DELETE OTHER: {err}')
        else:
            print(f'LDAP DELETED: {str(response.status_code)} {name}')

        return response

    def create(self, **kwargs):
        params = ldap_model(kwargs)

        try:
            response = self.session.post(self.api_location, json=params)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR LDAP CREATE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR LDAP CREATE OTHER: {err}')
        else:
            print(f"LDAP CREATED: {str(response.status_code)} {params['name']}")
