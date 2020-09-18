from requests.exceptions import HTTPError
from .models.blob_model import blob_model


class Blob:

    def __init__(self, session):
        self.session = session
        self.api_location = '/beta/blobstores'

    def list(self):
        response = self.session.get(self.api_location)
        blob_dict = {}
        for blob in response.json():
            blob_dict[blob['name']] = blob

        return blob_dict

    def create(self, **kwargs):
        # TODO: only files, we do not have S3
        params = blob_model(kwargs)

        try:
            response = self.session.post(f'{self.api_location}/file', json=params)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR BLOB CREATE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR BLOB CREATE OTHER: {err}')
        else:
            print(f'BLOB CREATED: {str(response.status_code)} {params["name"]} {params["path"]}')

    def update(self, **kwargs):
        params = blob_model(kwargs)

        try:
            response = self.session.put(f'{self.api_location}/file/{params["name"]}', json=params)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR BLOB UPDATE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR BLOB UPDATE OTHER: {err}')
        else:
            print(f'BLOB UPDATED: {str(response.status_code)} {params["name"]} {params["path"]}')

    def delete(self, **kwargs):

        name = kwargs.get('name')

        try:
            response = self.session.delete(f'{self.api_location}/{name}')

            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR BLOB DELETE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR BLOB DELETE OTHER: {err}')
        else:
            print(f'BLOB DELETED: {str(response.status_code)} {name}')
