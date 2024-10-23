import json
import time

import requests
import hashlib
import hmac

from reviewgpt.repository.repository_interface import RepositoryInterface


class GitHubService(RepositoryInterface):
    """
    Service class for interacting with GitHub API
    """
    def __init__(self, config):
        self.config = config

    def fetch_diff(self, repo_full_name, pull_number):
        return self._github_api_request(
            f'{self.config.repository_api_url}/repos/{repo_full_name}/pulls/{pull_number}',
            headers={'Accept': 'application/vnd.github.v3.diff'}
        )

    def add_label(self, repo_full_name, pull_number, label):
        self._github_api_request(
            f'{self.config.repository_api_url}/repos/{repo_full_name}/issues/{pull_number}/labels',
            method='POST',
            json={'labels': [label]}
        )

    def post_comment(self, repo_full_name, pull_number, comment_body):
        self._github_api_request(
            f'{self.config.repository_api_url}/repos/{repo_full_name}/issues/{pull_number}/comments',
            method='POST',
            json={'body': comment_body}
        )

    def post_review_comments(self, repo_full_name, pull_number, comments, commit_sha):
        for comment in comments:
            payload = {'body': comment['body'], 'commit_id': commit_sha, 'path': comment['path'], 'position': comment['position']}
            self._github_api_request(
                f'{self.config.repository_api_url}/repos/{repo_full_name}/pulls/{pull_number}/comments',
                headers={'Accept': 'application/vnd.github+json'},
                method='POST',
                json=payload
            )
            time.sleep(2)

    def _github_api_request(self, url, method='GET', headers=None, json=None):
        headers = headers or {}
        headers['Authorization'] = f'token {self.config.repository_oauth_token}'
        response = requests.request(method, url, headers=headers, json=json)

        if response.status_code in {200, 201}:
            return response.text if method == 'GET' else None
        else:
            response.raise_for_status()

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

    @staticmethod
    def is_supported_payload(payload):
        return payload.get('action') == 'opened' and 'pull_request' in payload
    
    @staticmethod
    def get_repo_name(payload):
        return payload['repository']['full_name']
    
    @staticmethod
    def get_pull_number(payload):
        return payload['pull_request']['number']

    @staticmethod
    def get_head_commit_sha(payload):
        return payload['pull_request']['head']['sha']
