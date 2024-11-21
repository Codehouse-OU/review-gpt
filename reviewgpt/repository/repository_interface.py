class RepositoryInterface:
    """Service interface for retrieving the data from selected source"""
    def fetch_diff(self, repo_full_name, pull_number) -> str:
        """
        Fetch the diff content for a given pull request

        :param repo_full_name:
        :param pull_number:
        :return: diff content
        """
        pass

    def add_label(self, repo_full_name, pull_number, label) -> None:
        """
        Add a label to the pull request

        :param repo_full_name:
        :param pull_number:
        :param label:
        """
        pass

    def post_comment(self, repo_full_name, pull_number, comment_body) -> None:
        """
        Post a comment to the pull request regarding the diff content

        :param repo_full_name:
        :param pull_number:
        :param comment_body:
        """
        pass

    def post_review_comments(self, repo_full_name, pull_number, content, commit_sha) -> None:
        """
        Post a list of review comments to the pull request

        :param repo_full_name:
        :param pull_number:
        :param content:
        :param commit_sha:
        """
        pass

    @staticmethod
    def is_supported_payload(payload) -> bool:
        """
        Check if the payload is a supported event

        :param payload:
        :return bool:
        """
        pass

    @staticmethod
    def get_repo_name(payload) -> str:
        """
        Get the repository name from the payload

        :param payload:
        :return str:
        """
        pass

    @staticmethod
    def get_pull_number(payload) -> str:
        """
        Get the pull request number from the payload

        :param payload:
        :return str:
        """
        pass

    @staticmethod
    def get_head_commit_sha(payload) -> str:
        """
        Get the head commit SHA from the payload

        :param payload:
        :return str:
        """
        pass

    def is_valid_request(self, request_data, headers, secret: str) -> bool:
        """
        Check if the payload is valid

        :param request_data:
        :param headers:
        :param secret:
        :return bool:
        """
        pass

    def post_process(self, code_diff: str, comments) -> list:
        """
        Do post-processing after the review

        :param code_diff:
        :param comments:
        :return array:
        """
        pass
