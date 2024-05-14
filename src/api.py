import uuid

from dataset import random_terminal_data

mil_auth_api_version = '1.0.0'


def get_terminal_registry_access_token(client, tr_token_client_id, tr_token_client_secret):
    headers = {
        'RequestId': str(uuid.uuid4()),
        'Version': mil_auth_api_version
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': tr_token_client_id,
        'client_secret': tr_token_client_secret
    }
    response = client.post('/mil-auth/token', headers=headers, data=data)
    return response.json().get('access_token')


def get_paginated_terminals(client, access_token_tr, page):
    headers = {
        'Authorization': f"Bearer {access_token_tr}",
        'RequestId': str(uuid.uuid4())
    }
    params = {
        'page': page,
        'size': 10
    }

    response = client.get('/mil-terminal-registry/terminals', headers=headers, params=params, name='GET /terminals')
    return response


def post_new_random_terminal(client, access_token_tr):
    headers = {
        'Authorization': f"Bearer {access_token_tr}",
        'RequestId': str(uuid.uuid4())
    }
    data = random_terminal_data()
    response = client.post('/mil-terminal-registry/terminals', headers=headers, json=data, name='POST /terminals')
    return response


def patch_terminal(client, access_token_tr, target_terminal_uuid):
    headers = {
        'Authorization': f"Bearer {access_token_tr}",
        'RequestId': str(uuid.uuid4())
    }
    data = random_terminal_data()
    response = client.patch(f'/mil-terminal-registry/terminals/{target_terminal_uuid}', headers=headers,
                            json=data, name='PATCH /terminals/{terminalUUID}')
    return response


def delete_terminal(client, access_token_tr, target_terminal_uuid):
    headers = {
        'Authorization': f"Bearer {access_token_tr}",
        'RequestId': str(uuid.uuid4())
    }
    response = client.delete(f'/mil-terminal-registry/terminals/{target_terminal_uuid}', headers=headers,
                             name='DELETE /terminals/{terminalUUID}')
    return response
