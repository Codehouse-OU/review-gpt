import logging
import os
from flask import Flask, request, jsonify
from chatgpt import ChatGptService
from configuration import Configuration
from webservice.app_service import AppService
from webservice.github import GitHubService

app = Flask(__name__)
config = Configuration()
app_service = AppService(config, GitHubService(config), ChatGptService(config))
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
def bot_webhook():
    payload = request.json
    logging.debug(f'Payload received: {payload}')
    if not app_service.is_valid_request(request):
        logging.error('Invalid request')
        return jsonify({'message': 'Invalid request'}), 400
    result = app_service.execute(payload)
    if result >= 0:
        logging.debug(f'PR reviewed successfully with code: {result}')
        return jsonify({'message': 'PR reviewed'}), 200
    else:
        logging.error(f'Error processing PR with code: {result}')
        return jsonify({'message': 'Error processing PR'}), 400


if __name__ == '__main__':
    logging.debug("{0}: {1}".format("ENDPOINT", os.environ.get("ENDPOINT")))
    logging.debug("{0}: {1}".format("MODEL_NAME", os.environ.get("MODEL_NAME")))
    logging.debug("{0}: {1}".format("API_VERSION", os.environ.get("API_VERSION")))
    app.run(host='0.0.0.0', port=5000)
