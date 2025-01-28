from uuid import uuid4

admin_credentials = {
    "email": "admin@example.com",
    "password": "admin123",
    "access_token": "",
    "refresh_token": ""
}

users = []


def test_login_admin(client, init_database_with_admin):
    admin = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    response = client.post('/auth/login', json=admin)
    assert response.status_code == 200
    data = response.get_json()
    admin_credentials['access_token'] = data['tokens']['access_token']


def test_get_all_users(client, init_database_with_admin):
    response = client.get('/users/', headers={'Authorization': f'Bearer {admin_credentials["access_token"]}'})
    assert response.status_code == 200
    data = response.get_json()
    users.append(data)


def test_get_user_by_id(client, init_database_with_admin):
    user_id = str(users[0]['users'][0]['id'])
    response = client.get(f'/users/{user_id}', headers={'Authorization': f'Bearer {admin_credentials["access_token"]}'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == user_id


def test_get_user_by_id_invalid(client, init_database_with_admin):
    user_id = str(uuid4())
    response = client.get(f'/users/{user_id}', headers={'Authorization': f'Bearer {admin_credentials["access_token"]}'})
    assert response.status_code == 404

def test_update_user(client, init_database_with_admin):
    user_id = str(users[0]['users'][0]['id'])
    json = {
        "name": "José Bezerra",
        "is_admin": True
    }
    response = client.put(f'/users/{user_id}', json=json, headers={'Authorization': f'Bearer {admin_credentials["access_token"]}'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == json['name']
    assert data['is_admin'] == json['is_admin']
    assert data['id'] == user_id

def test_delete_user(client, init_database_with_admin):
    user_id = str(users[0]['users'][0]['id'])
    response = client.delete(f'/users/{user_id}', headers={'Authorization': f'Bearer {admin_credentials["access_token"]}'})
    assert response.status_code == 204