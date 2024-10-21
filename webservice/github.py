import requests

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

    @staticmethod
    def is_supported_payload(payload):
        return payload.get('action') == 'opened' and 'pull_request' in payload
    
    @staticmethod
    def get_repo_name(payload):
        return payload['repository']['full_name']
    
    @staticmethod
    def get_pull_number(payload):
        return payload['pull_request']['number']
