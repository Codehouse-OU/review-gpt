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
