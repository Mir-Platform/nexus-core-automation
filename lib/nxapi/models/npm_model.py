def npm_model_hosted(params):
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
        }
    }

    return model


def npm_model_proxy(params):
    model = {
        'name': params.get('name'),
        'online': params.get('online', True),
        'storage': {
            'blobStoreName': params.get('blobStoreName', params['name']),
            'strictContentTypeValidation': params.get('strictContentTypeValidation', True),
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
            'enabled': False,
            'timeToLive': 1440
        },
        'httpClient': {
            'blocked': False,
            'autoBlock': False,
            'connection': {
                'retries': 0,
                'userAgentSuffix': params.get('userAgentSuffix'),
                'timeout': 60,
                'enableCircularRedirects': False,
                'enableCookies': False
            }
            # ,
            # 'authentication': {
            # 'type': 'username',
            # 'username': username,
            # 'ntlmHost': 'string',
            # 'ntlmDomain': 'string'
            # }
        }
        # 'routingRule': 'string',
    }

    return model


def npm_model_group(params):
    model = {
        'name': params.get('name'),
        'online': params.get('online', True),
        'storage': {
            'blobStoreName': params.get('blobStoreName'),
            'strictContentTypeValidation': params.get('strictContentTypeValidation', True)
        },
        'group': {
            'memberNames': params.get('memberNames'),
        }
    }

    return model