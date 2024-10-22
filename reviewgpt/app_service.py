import logging
import json

from reviewgpt.configuration import Configuration
from reviewgpt.repository.repository_interface import RepositoryInterface
from reviewgpt.review.review_interface import ReviewInterface


class AppService:
    """
    Application Service responsible for coordinating the review process
    """
    def __init__(self, config: Configuration, repository_interface: RepositoryInterface, review_interface: ReviewInterface):
        self._config = config
        self._repository_service = repository_interface
        self._review_service = review_interface

    def is_valid_request(self, request) -> bool:
        """
        Validate incoming request
        :param request:
        :return bool:
        """
        return self._repository_service.is_valid_request(request.data, request.headers, self._config.webhook_secret)

    def execute(self, payload) -> int:
        """
        Main method to execute the review process
        :param payload:
        :return int:
        """
        try:
            if self._repository_service.is_supported_payload(payload):
                repo_full_name = self._repository_service.get_repo_name(payload)
                pull_number = self._repository_service.get_pull_number(payload)
                code_diff = self._repository_service.fetch_diff(repo_full_name, pull_number)
                message = self._review_service.review(code_diff)
                self._repository_service.add_label(repo_full_name, pull_number, self._config.repository_label)

                if message == "NO_COMMENTS":
                    self._repository_service.post_comment(repo_full_name, pull_number, self._config.good_job_message)
                    return 0

                comments_array = json.loads(message)
                self._repository_service.post_review_comments(repo_full_name, pull_number, comments_array, self._repository_service.get_head_commit_sha(payload))
                return 1
        except Exception as e:
            logging.error(f'Error during execution: {str(e)}')
            return -1
        return -2
