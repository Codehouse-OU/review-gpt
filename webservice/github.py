import requests
import hashlib
import hmac

from webservice.repository_interface import RepositoryInterface


class GitHubService(RepositoryInterface):
    """
    Service class for interacting with GitHub API
    """
    def __init__(self, config):
        self.config = config

    def fetch_diff(self, repo_full_name, pull_number):
        return self._github_api_request(
            f'{self.config.github_api_url}/repos/{repo_full_name}/pulls/{pull_number}',
            headers={'Accept': 'application/vnd.github.v3.diff'}
        )

    def add_label(self, repo_full_name, pull_number, label):
        self._github_api_request(
            f'{self.config.github_api_url}/repos/{repo_full_name}/issues/{pull_number}/labels',
            method='POST',
            json={'labels': [label]}
        )

    def post_comment(self, repo_full_name, pull_number, comment_body):
        self._github_api_request(
            f'{self.config.github_api_url}/repos/{repo_full_name}/issues/{pull_number}/comments',
            method='POST',
            json={'body': comment_body}
        )

    def _github_api_request(self, url, method='GET', headers=None, json=None):
        headers = headers or {}
        headers['Authorization'] = f'token {self.config.oauth_token}'
        response = requests.request(method, url, headers=headers, json=json)

        if response.status_code in {200, 201}:
            return response.text if method == 'GET' else None
        else:
            response.raise_for_status()

    def is_valid_request(self, request_data, headers, secret_token) -> bool:
        """
        Verify that the payload was sent from GitHub by validating SHA256.
        @see: https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
        Returns false if there is a problem with validation. Validation can be skipped when secret_token is not provided.

        Args:
            request_data: original request body to verify (request.body())
            headers: headers received from GitHub (including x-hub-signature-256)
            secret_token: GitHub app webhook token (WEBHOOK_SECRET)
            :return bool:
        """
        signature_header = headers.get('X-Hub-Signature-256')
        if not secret_token or secret_token == "":
            if signature_header:
                return False

        if not signature_header or not signature_header.startswith('sha256='):
            return False
        hash_object = hmac.new(secret_token.encode('utf-8'), msg=request_data, digestmod=hashlib.sha256)
        expected_signature = "sha256=" + hash_object.hexdigest()
        if not hmac.compare_digest(expected_signature, signature_header):
            return False
        return True

    @staticmethod
    def is_supported_payload(payload):
        return payload.get('action') == 'opened' and 'pull_request' in payload
    
    @staticmethod
    def get_repo_name(payload):
        return payload['repository']['full_name']
    
    @staticmethod
    def get_pull_number(payload):
        return payload['pull_request']['number']
