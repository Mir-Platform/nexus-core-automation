def docker_model_hosted(params):
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
        'docker': {
            'v1Enabled': params.get('v1Enabled', True),
            'forceBasicAuth': params.get('forceBasicAuth', True),  # anonymous docker pull
            'httpPort': params.get('httpPort', None),
            'httpsPort': params.get('httpsPort', None)
        }
    }

    return model


def docker_model_proxy(params):
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
            'remoteUrl': params['remoteUrl'],
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
                'userAgentSuffix': params.get('userAgentSuffix', None),
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
        },
        # 'routingRule': 'string',
        'docker': {
            'v1Enabled': params.get('v1Enabled', True),
            'forceBasicAuth': params.get('forceBasicAuth', True),
            'httpPort': params.get('httpPort', None),
            'httpsPort': params.get('httpsPort', None)
        },
        'dockerProxy': {
            'indexType': 'HUB',
            'indexUrl': params.get('indexUrl', None)
        }
    }

    return model


def docker_model_group(params):
    model = {
        'name': params.get('name'),
        'online': params.get('online', True),
        'storage': {
            'blobStoreName': params.get('blobStoreName', params['name']),
            'strictContentTypeValidation': params.get('strictContentTypeValidation', True)
        },
        'group': {
            'memberNames': params.get('memberNames'),
        },
        'docker': {
            'v1Enabled': params.get('v1Enabled', True),
            'forceBasicAuth': params.get('forceBasicAuth', True),
            'httpPort': params.get('httpPort', None),
            'httpsPort': params.get('httpsPort', None)
        }
    }

    return model
