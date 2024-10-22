from reviewgpt.configuration import Configuration
from reviewgpt.repository.repository_interface import RepositoryInterface
from reviewgpt.review.review_interface import ReviewInterface


class AppService:
    """
    Service class for handling the application
    """
    def __init__(self, config: Configuration, repository_interface: RepositoryInterface, review_interface: ReviewInterface):
        self._config = config
        self._repository = repository_interface
        self._review = review_interface

    def is_valid_request(self, request) -> bool:
        """
        Validate the request

        :param request:
        :return bool:
        """
        return self._repository.is_valid_request(request.data, request.headers, self._config.webhook_secret)

    def execute(self, payload) -> int:
        """
        Execute the application logic

        :param payload:
        :return int:
        """
        if self._repository.is_supported_payload(payload):
            repo_full_name = self._repository.get_repo_name(payload)
            pull_number = self._repository.get_pull_number(payload)

            try:
                code_diff = self._repository.fetch_diff(repo_full_name, pull_number)
                message = self._review.execute(code_diff)
                self._repository.add_label(repo_full_name, pull_number, self._config.repository_label)
                if message == "NO_COMMENTS":
                    return 0
        
                self._repository.post_comment(repo_full_name, pull_number, message)
                return 1
            except Exception as e:
                return -1
        return -2
