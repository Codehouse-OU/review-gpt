import pytest
from unittest.mock import Mock
from reviewgpt.app_service import AppService
from reviewgpt.configuration import Configuration
from reviewgpt.repository.repository_interface import RepositoryInterface
from reviewgpt.review.review_interface import ReviewInterface


@pytest.fixture
def app_service():
    config = Configuration()
    repository_interface = Mock(spec=RepositoryInterface)
    review_interface = Mock(spec=ReviewInterface)
    return AppService(config, repository_interface, review_interface)


def test_is_valid_request(app_service):
    request = Mock()
    request.data = "data"
    request.headers = {"header": "value"}
    app_service._repository_service.is_valid_request.return_value = True
    assert app_service.is_valid_request(request) == True


def test_execute_valid_payload(app_service):
    payload = {"some": "payload"}
    app_service._repository_service.is_supported_payload.return_value = True
    app_service._repository_service.get_repo_name.return_value = "repo/name"
    app_service._repository_service.get_pull_number.return_value = 1
    app_service._repository_service.fetch_diff.return_value = "diff"
    app_service._review_service.review.return_value = "NO_COMMENTS"
    app_service._repository_service.add_label.return_value = None

    assert app_service.execute(payload) == 0


def test_execute_invalid_payload(app_service):
    payload = {"some": "payload"}
    app_service._repository_service.is_supported_payload.return_value = False

    assert app_service.execute(payload) == -2
