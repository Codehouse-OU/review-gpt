from repository_interface import RepositoryInterface


class DummyRepository(RepositoryInterface):
    """
    Dummy repository for testing purposes
    """
    def __init__(self, config):
        self.config = config

    def fetch_diff(self, repo_full_name, pull_number):
        return 'diff --git a/file1.txt b/file1.txt\nindex 0000000..1111111 100644\n--- a/file1.txt\n+++ b/file1.txt\n@@ -1,2 +1,2 @@\n-line1\n+line2\n line3\n'

    def add_label(self, repo_full_name, pull_number, label):
        pass

    def post_comment(self, repo_full_name, pull_number, comment_body):
        pass

    @staticmethod
    def is_supported_payload(payload) -> bool:
        return True

    @staticmethod
    def get_repo_name(payload) -> str:
        return 'test/test'

    @staticmethod
    def get_pull_number(payload) -> str:
        return '1'

    def is_valid_request(self, request_data_bytes: bytes, headers, secret: str) -> bool:
        return True