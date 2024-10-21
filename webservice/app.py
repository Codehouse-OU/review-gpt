import logging
import os
from flask import Flask, request, jsonify
from chatgpt import ChatGptService
from configuration import Configuration
from github import GitHubService

app = Flask(__name__)
config = Configuration()
github_service = GitHubService(config)
chatgpt_service = ChatGptService(config)

# Set up logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['GET'])
def bot_description():
    description = {
        "name": "GitHub Webhook Bot",
        "purpose": "This bot processes GitHub pull request webhooks, fetches the diff content, generates comments using ChatGPT, and labels the pull request as 'bot_reviewed'."
    }
    return jsonify(description), 200


@app.route('/', methods=['POST'])
def github_webhook():
    payload = request.json
    logging.debug(f'Payload received: {payload}')

    if payload.get('action') == 'opened' and 'pull_request' in payload:
        repo_full_name = payload['repository']['full_name']
        pull_number = payload['pull_request']['number']
        logging.debug(f'Repo Full Name: {repo_full_name}, Pull Request Number: {pull_number}')

        try:
            diff = github_service.fetch_diff(repo_full_name, pull_number)
            logging.debug(f'Diff fetched successfully:\n{diff}')
            message = chatgpt_service.generate_response(code_diff=diff)
            github_service.add_label(repo_full_name, pull_number, config.label)
            if message == "NO_COMMENTS":
                logging.info("No comments to add")
                return jsonify({'message': 'No comments to add'}), 200

            github_service.post_comment(repo_full_name, pull_number, message)
            return jsonify({'message': 'Diff fetched and comment posted successfully'}), 200
        except Exception as e:
            logging.error(f'Error processing pull request: {e}')
            return jsonify({'message': f'Error processing pull request: {e}'}), 500

    return jsonify({'message': 'Not a pull request opened event'}), 400


if __name__ == '__main__':
    print("{0}: {1}".format("ENDPOINT", os.environ.get("ENDPOINT")))
    print("{0}: {1}".format("MODEL_NAME", os.environ.get("MODEL_NAME")))
    print("{0}: {1}".format("API_VERSION", os.environ.get("API_VERSION")))
    app.run(host='0.0.0.0', port=5000)
