def blob_model(params):
    model = {
        'name': params.get('name'),
        'path': params.get('path', '/nexus-data/blobs/' + params.get('name'))
    }

    return model
