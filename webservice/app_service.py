from configuration import Configuration
from repository_interface import RepositoryInterface
from review_interface import ReviewInterface


class AppService:
    """
    Service class for handling the application
    """
    def __init__(self, config: Configuration, repository_interface: RepositoryInterface, review_interface: ReviewInterface):
        self._config = config
        self._repository_interface = repository_interface
        self._review_interface = review_interface

    def is_valid_request(self, request) -> bool:
        """
        Validate the request

        :param request:
        :return bool:
        """
        return self._repository_interface.is_valid_request(request.data, request.headers, self._config.secret_token)

    def execute(self, payload) -> int:
        """
        Execute the application logic

        :param payload:
        :return int:
        """
        if self._repository_interface.is_supported_payload(payload):
            repo_full_name = self._repository_interface.get_repo_name(payload)
            pull_number = self._repository_interface.get_pull_number(payload)

            try:
                code_diff = self._repository_interface.fetch_diff(repo_full_name, pull_number)
                message = self._review_interface.review(code_diff)
                self._repository_interface.add_label(repo_full_name, pull_number, self._config.label)
                if message == "NO_COMMENTS":
                    return 0
        
                self._repository_interface.post_comment(repo_full_name, pull_number, message)
                return 1
            except Exception as e:
                return -1
        return -2
