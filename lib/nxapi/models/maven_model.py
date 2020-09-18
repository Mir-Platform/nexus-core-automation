def maven_model_hosted(params):
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
        'maven': {
            'versionPolicy': params.get('versionPolicy', 'MIXED'),
            'layoutPolicy': params.get('layoutPolicy', 'PERMISSIVE')
        }
    }

    return model


def maven_model_proxy(params):
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
            'enabled': False,
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
        'maven': {
            'versionPolicy': params.get('versionPolicy', 'MIXED'),
            'layoutPolicy': params.get('layoutPolicy', 'PERMISSIVE')
        }
    }

    return model


def maven_model_group(params):
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
