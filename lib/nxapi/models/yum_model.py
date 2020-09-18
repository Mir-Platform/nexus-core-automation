def yum_model_hosted(params):
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
        'yum': {
            'repodataDepth': params.get('repodataDepth', 5),
            'deployPolicy': params.get('deployPolicy', 'PERMISSIVE')
        }
    }

    return model
