def user_model(params):
    # TODO: this is example model, we use LDAP users

    model = {
        'userId': params.get('userId'),
        'firstName': params.get('firstName', params.get('userId')),
        'lastName': params.get('lastName', params.get('userId')),
        'emailAddress': params.get('emailAddress', params.get('userId') + '@test.ru'),
        'password': params.get('password', 'pa$$w0rd'),
        'status': params.get('status', 'ACTIVE'),
        'source': params.get('source', None),
        'roles': params.get('roles', ['nx-anonymous'])
    }

    return model
