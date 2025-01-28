import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def test_app_is_created(app):
    assert app.name == "apilogin.app"


def test_config_is_loaded(config):
    assert config['DEBUG'] is True


def test_request_returns_404(client):
    assert client.get('/url_que_nao_existe').status_code == 404
