import hashlib
import re
import hmac
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
        incoming_signature = headers.get('x-hub-signature-256')
        calculated_signature = self.calculate_signature(secret, request_data_bytes)
        if not hmac.compare_digest(calculated_signature, incoming_signature):
            return False
        else:
            return True

    @staticmethod
    def calculate_signature(secret, payload_bytes) -> str:
        """
        Signature calculator
        """
        signature_bytes = bytes(secret, 'utf-8')
        digest = hmac.new(key=signature_bytes, msg=payload_bytes, digestmod=hashlib.sha256)
        signature = "sha256=" + digest.hexdigest()
        return signature
