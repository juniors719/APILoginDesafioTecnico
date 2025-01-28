import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def test_app_is_created(app):
    assert app.name == "apilogin.app"


def test_index(client):
    response = client.get("/hello")
    assert response.data == b"hello world"
