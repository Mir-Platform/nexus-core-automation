def raw_model_hosted(params):
    model = {
        'name': params.get('name'),
        'online': params.get('online', True),
        'storage': {
            'blobStoreName': params.get('blobStoreName', params['name']),
            'strictContentTypeValidation': params.get('strictContentTypeValidation', True),
            'writePolicy': params.get('writePolicy', 'ALLOW')
        },
        'cleanup': {
            'policyNames': params.get('policyNames', [])
        },
        'raw': {
            'contentDisposition': params.get('contentDisposition', 'ATTACHMENT')
        }
    }

    return model


def raw_model_proxy(params):
    model = {
        'name': params.get('name'),
        'online': params.get('online', True),
        'storage': {
            'blobStoreName': params.get('blobStoreName', params['name']),
            'strictContentTypeValidation': params.get('strictContentTypeValidation', True)
        },
        'cleanup': {
            'policyNames': params.get('policyNames', [])
        },
        'proxy': {
            'remoteUrl': params.get('remoteUrl'),
            'contentMaxAge': 1440,
            'metadataMaxAge': 1440
        },
        'negativeCache': {
            'enabled': True,
            'timeToLive': 1440
        },
        'httpClient': {
            'blocked': False,
            'autoBlock': False,
            'connection': {
                'retries': 0,
                'userAgentSuffix': params.get('userAgentSuffix', 'curl'),
                'timeout': 60,
                'enableCircularRedirects': False,
                'enableCookies': False
            }
            # ,
            # 'authentication': {
            #     'type': 'username',
            #     'username': username,
            #     'password': password,
            #     'ntlmHost': ntlmHost,
            #     'ntlmDomain': ntlmDomain
        },
        'routingRule': params.get('routingRule', ''),
        'raw': {
            'contentDisposition': params.get('contentDisposition', 'ATTACHMENT')
        }
    }

    return model


def raw_model_group(params):
    model = {
        'name': params.get('name'),
        'online': params.get('online', True),
        'storage': {
            'blobStoreName': params.get('blobStoreName'),
            'strictContentTypeValidation': params.get('strictContentTypeValidation', True)
        },
        'group': {
            'memberNames': params.get('memberNames'),
        },
        'raw': {
            'contentDisposition': params.get('contentDisposition', 'ATTACHMENT')
        }
    }

    return model
