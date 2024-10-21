import logging
import requests
from flask import Flask, request, jsonify
from chatgpt import ChatGptService
from configuration import Configuration

app = Flask(__name__)
config = Configuration()

# Set up logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['POST'])
def github_webhook():
    payload = request.json
    logging.debug(f'Payload received: {payload}')

    if payload.get('action') == 'opened' and 'pull_request' in payload:
        repo_full_name = payload['repository']['full_name']
        pull_number = payload['pull_request']['number']
        logging.debug(f'Repo Full Name: {repo_full_name}, Pull Request Number: {pull_number}')

        try:
            diff = fetch_diff_from_github(repo_full_name, pull_number)
            logging.debug(f'Diff fetched successfully:\n{diff}')
            chat_gpt = ChatGptService()
            message = chat_gpt.generate_response(code_diff=diff)
            add_label_to_pull_request(repo_full_name, pull_number, "bot_reviewed")
            if message == "NO_COMMENTS":
                    logging.info("No comments to add")
                    return jsonify({'message': 'No comments to add'}), 200

            post_comment_to_pull_request(repo_full_name, pull_number, message)
            return jsonify({'message': 'Diff fetched and comment posted successfully'}), 200
        except Exception as e:
            logging.error(f'Error processing pull request: {e}')
            return jsonify({'message': f'Error processing pull request: {e}'}), 500

    return jsonify({'message': 'Not a pull request opened event'}), 400


def add_label_to_pull_request(repo_full_name, pull_number, label):
    github_api_request(
        f'{config.github_api_url}/repos/{repo_full_name}/issues/{pull_number}/labels',
        method='POST',
        json={'labels': [label]}
    )
    logging.debug('Label added successfully')


def fetch_diff_from_github(repo_full_name, pull_number):
    return github_api_request(
        f'{config.github_api_url}/repos/{repo_full_name}/pulls/{pull_number}',
        headers={'Accept': 'application/vnd.github.v3.diff'}
    )


def post_comment_to_pull_request(repo_full_name, pull_number, comment_body):
    github_api_request(
        f'{config.github_api_url}/repos/{repo_full_name}/issues/{pull_number}/comments',
        method='POST',
        json={'body': comment_body}
    )
    logging.debug('Comment posted successfully')


def github_api_request(url, method='GET', headers=None, json=None):
    headers = headers or {}
    headers['Authorization'] = f'token {config.oauth_token}'
    response = requests.request(method, url, headers=headers, json=json)

    if response.status_code in {200, 201}:
        return response.text if method == 'GET' else None
    else:
        response.raise_for_status()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)