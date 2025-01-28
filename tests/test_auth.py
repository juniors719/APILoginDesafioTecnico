new_user = {
    "name": "Usuário teste",
    "email": "teste@example.com",
    "password": "senha1234567890",
    "access_token": "",
    "refresh_token": ""
}


def test_register_user(client):
    response = client.post('/auth/register', json=new_user)
    assert response.status_code == 201


def test_register_user_duplicate_email(client):
    response = client.post('/auth/register', json=new_user)
    assert response.status_code == 409  # Supondo que 409 é usado para conflito
    data = response.get_json()
    assert data['error'] == 'Email already registered'


def test_login(client):
    login = {
        "email": new_user['email'],
        "password": new_user['password']
    }
    response = client.post('/auth/login', json=login)
    assert response.status_code == 200
    data = response.get_json()
    new_user['access_token'] = data['tokens']['access_token']
    new_user['refresh_token'] = data['tokens']['refresh_token']
    assert data['message'] == 'Login successful'
    assert "access_token" in data['tokens']
    assert "refresh_token" in data['tokens']


def test_login_invalid_email(client):
    login = {
        "email": "invalid",
        "password": new_user['password']
    }
    response = client.post('/auth/login', json=login)
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Invalid credentials'


def test_login_invalid_password(client):
    login = {
        "email": new_user['email'],
        "password": "invalid"
    }
    response = client.post('/auth/login', json=login)
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Invalid credentials'


def test_login_without_credentials(client):
    response = client.post('/auth/login')
    assert response.status_code == 415


def test_whoami(client):
    response = client.get('/auth/whoami', headers={'Authorization': f'Bearer {new_user["access_token"]}'})
    assert response.status_code == 200


def test_whoami_with_invalid_token(client):
    response = client.get('/auth/whoami', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'invalid_token'


def test_logout(client):
    response = client.post('/auth/logout', headers={'Authorization': f'Bearer {new_user["access_token"]}'})


def test_whoami_without_token(client):
    response = client.get('/auth/whoami')
    assert response.status_code == 401
