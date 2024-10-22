import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_bot_description(client):
    rv = client.get('/')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data['name'] == "GitHub Webhook Bot"


def test_bot_webhook_invalid_request(client, monkeypatch):
    def mock_is_valid_request(self, request):
        return False

    monkeypatch.setattr('reviewgpt.app_service.AppService.is_valid_request', mock_is_valid_request)
    rv = client.post('/', json={})
    json_data = rv.get_json()
    assert rv.status_code == 400
    assert json_data['message'] == 'Invalid request'


def test_bot_webhook_valid_request(client, monkeypatch):
    rv = client.post('/', json={})
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data['message'] == 'PR reviewed'
