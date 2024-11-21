import logging

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
        if self._config.skip_validation == '1':
            logging.warning("Skipping request validation")
            return True
        else:
            return self._repository_service.is_valid_request(request.data, request.headers, self._config.webhook_secret)

    def execute(self, payload) -> int:
        """
        Main method to execute the review process
        :param payload:
        :return int:
        """
        if not self._repository_service.is_supported_payload(payload):
            return -2
        repo_full_name = self._repository_service.get_repo_name(payload)
        pull_number = self._repository_service.get_pull_number(payload)
        code_diff = self._repository_service.fetch_diff(repo_full_name, pull_number)

        if not code_diff or not pull_number or not repo_full_name:
            return -3

        try:
            message = self._review_service.review(code_diff)
        except Exception as e:
            logging.error(f'Error while generating review: {str(e)}, repo_full_name: {repo_full_name}, pull_number: {pull_number}')
            return -4

        try:
            self._repository_service.add_label(repo_full_name, pull_number, self._config.repository_label)
            if message == "NO_COMMENTS":
                self._repository_service.post_comment(repo_full_name, pull_number, self._config.good_job_message)
                return 0
        except Exception as e:
            logging.error(f'Error during label adding: {str(e)}, repo_full_name: {repo_full_name}, pull_number: {pull_number}')
            return -5

        try:
            logging.debug(f'Parsed review comments: {message}')
            comments_array = self._repository_service.post_process(code_diff, message)
            self._repository_service.post_review_comments(repo_full_name, pull_number, comments_array, self._repository_service.get_head_commit_sha(payload))
            return 1
        except Exception as e:
            logging.error(f'Error during parsing the review response to review comments: {str(e)}, repo_full_name: {repo_full_name}, pull_number: {pull_number}')
            return -6
