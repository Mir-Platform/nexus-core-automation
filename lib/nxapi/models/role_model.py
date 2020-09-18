def role_model(params):
    model = {
        'id': params.get('id', params.get('name')),
        'name': params.get('name'),
        'description': params.get('id', params.get('name')),
        'privileges': params.get('privileges', []),
        'roles': params.get('roles', [])
    }

    return model
