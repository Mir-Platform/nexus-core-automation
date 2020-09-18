from requests.exceptions import HTTPError
from .models.maven_model import maven_model_proxy, maven_model_hosted, maven_model_group
from .models.docker_model import docker_model_proxy, docker_model_group, docker_model_hosted
from .models.npm_model import npm_model_group, npm_model_hosted, npm_model_proxy
from .models.yum_model import yum_model_hosted
from .models.raw_model import raw_model_group, raw_model_proxy, raw_model_hosted


class Repo:

    def __init__(self, session):
        self.session = session
        self.api_location = '/beta/repositories'

    def list(self):
        repo_dict = {}

        try:
            response = self.session.get(self.api_location)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR REPO LIST HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR REPO LIST OTHER: {err}')
        else:
            print(f'REPO LISTED: {str(response.status_code)}')

        for repo in response.json():
            repo_dict[repo['name']] = repo

        return repo_dict

    def create(self, **kwargs):

        if kwargs['repoType'] == 'yum':

            if kwargs['locationType'] == "hosted":
                scheme = yum_model_hosted(kwargs)
            else:
                raise NameError(f'ERROR locationType for YUM not supported. Use hosted')

        elif kwargs['repoType'] == 'npm':

            if kwargs['locationType'] == "hosted":
                scheme = npm_model_hosted(kwargs)
            elif kwargs['locationType'] == "proxy":
                scheme = npm_model_proxy(kwargs)
            elif kwargs['locationType'] == 'group':  # array
                scheme = npm_model_group(kwargs)

            else:
                raise NameError(f'ERROR locationType for NPM not supported. Use hosted/proxy/group')

        elif kwargs['repoType'] == 'maven':

            if kwargs['locationType'] == "hosted":
                scheme = maven_model_hosted(kwargs)
            elif kwargs['locationType'] == "proxy":
                scheme = maven_model_proxy(kwargs)
            elif kwargs['locationType'] == 'group':
                # TODO: not ready backend nexus 3.22.0-02  # array
                scheme = maven_model_proxy(kwargs)

            else:
                raise NameError(f'ERROR locationType for MAVEN not supported. Use hosted/proxy')

        elif kwargs['repoType'] == 'docker':

            if kwargs['locationType'] == "hosted":
                scheme = docker_model_hosted(kwargs)
            elif kwargs['locationType'] == 'proxy':
                scheme = docker_model_proxy(kwargs)
            elif kwargs['locationType'] == 'group':
                scheme = docker_model_group(kwargs)

            else:
                raise NameError(f'ERROR locationType for DOCKER not supported. Use hosted/proxy/group')

        elif kwargs['repoType'] == 'raw':

            if kwargs['locationType'] == "hosted":
                scheme = raw_model_hosted(kwargs)
            elif kwargs['locationType'] == 'proxy':
                scheme = raw_model_proxy(kwargs)
            elif kwargs['locationType'] == 'group':
                scheme = raw_model_group(kwargs)

            else:
                raise NameError(f'ERROR locationType for RAW not supported. Use hosted/proxy/group')

        else:
            raise NameError(f'ERROR repoType for {kwargs["repoType"]} UPDATE not supported. Use maven/docker/npm/yum/raw')

        try:
            response = self.session.post(f"{self.api_location}/{kwargs['repoType']}/{kwargs['locationType']}",
                                         json=scheme)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f"ERROR repo {kwargs['name']} CREATE HTTP: {http_err}")
        except Exception as err:
            print(f"ERROR repo {kwargs['name']} CREATE OTHER: {err}")
        else:
            print(f"REPO CREATED: {str(response.status_code)} {kwargs['name']} {kwargs['repoType']}")

    def update(self, **kwargs):

        if kwargs['repoType'] == 'yum':

            if kwargs['locationType'] == "hosted":
                scheme = yum_model_hosted(kwargs)

            else:
                raise NameError(f'ERROR locationType for YUM not supported. Use hosted')

        elif kwargs['repoType'] == 'npm':

            if kwargs['locationType'] == "hosted":
                scheme = npm_model_hosted(kwargs)
            elif kwargs['locationType'] == "proxy":
                scheme = npm_model_proxy(kwargs)
            elif kwargs['locationType'] == 'group':  # array
                scheme = npm_model_group(kwargs)

            else:
                raise NameError(f'ERROR locationType for NPM not supported. Use hosted/proxy/group')

        elif kwargs['repoType'] == 'maven':

            if kwargs['locationType'] == "hosted":
                scheme = maven_model_hosted(kwargs)
            elif kwargs['locationType'] == "proxy":
                scheme = maven_model_proxy(kwargs)
            elif kwargs['locationType'] == 'group':
                scheme = maven_model_proxy(kwargs)

            else:
                raise NameError(f'ERROR locationType for MAVEN not supported. Use hosted/proxy')

        elif kwargs['repoType'] == 'docker':

            if kwargs['locationType'] == "hosted":
                scheme = docker_model_hosted(kwargs)
            elif kwargs['locationType'] == 'proxy':
                scheme = docker_model_proxy(kwargs)
            elif kwargs['locationType'] == 'group':
                scheme = docker_model_group(kwargs)

            else:
                raise NameError(f'ERROR locationType for DOCKER not supported. Use hosted/proxy/group')

        elif kwargs['repoType'] == 'raw':

            if kwargs['locationType'] == "hosted":
                scheme = raw_model_hosted(kwargs)
            elif kwargs['locationType'] == 'proxy':
                scheme = raw_model_proxy(kwargs)
            elif kwargs['locationType'] == 'group':
                scheme = raw_model_group(kwargs)

            else:
                raise NameError(f'ERROR locationType for RAW not supported. Use hosted/proxy/group')

        else:
            raise NameError(f'ERROR repoType for {kwargs["repoType"]} UPDATE not supported. Use maven/docker/npm/raw')

        try:
            response = self.session.put(f"{self.api_location}/{kwargs['repoType']}/{kwargs['locationType']}/{kwargs.get('name')}",
                                        json=scheme)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f"ERROR repo {kwargs['name']} UPDATE HTTP: {http_err}")
        except Exception as err:
            print(f"ERROR repo {kwargs['name']} UPDATE OTHER: {err}")
        else:
            print(f"REPO UPDATED: {str(response.status_code)} {kwargs['name']} {kwargs['repoType']}")

    def delete(self, name):

        try:
            response = self.session.delete(f'{self.api_location}/{name}')
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'ERROR repo {name} DELETE HTTP: {http_err}')
        except Exception as err:
            print(f'ERROR repo {name} DELETE OTHER: {err}')
        else:
            print(f'REPO DELETED: {str(response.status_code)} {name}')
