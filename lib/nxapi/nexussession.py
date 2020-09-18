from requests import Session


class NexusSession(Session):
    def __init__(self, url_base=None, auth=None, verify=False):
        super(NexusSession, self).__init__()
        self.url_base = url_base
        self.auth = auth
        self.verify = verify

    def request(self, method, url, **kwargs):
        modified_url = self.url_base + url

        return super(NexusSession, self).request(method, modified_url, **kwargs)
