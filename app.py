import logging
import os
from flask import Flask, request, jsonify
from reviewgpt.configuration import Configuration
from reviewgpt.app_service import AppService
from reviewgpt.review.review_factory import ReviewFactory
from reviewgpt.repository.repository_factory import RepositoryFactory

app = Flask(__name__)
config = Configuration()
configured_review = ReviewFactory(config).get_review_service()
configured_repository = RepositoryFactory(config).get_repository_service()

app_service = AppService(config, configured_repository, configured_review)
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
        return jsonify({'message': 'Invalid request'}), 401
    result = app_service.execute(payload)
    if result >= 0:
        logging.debug(f'PR reviewed successfully with code: {result}')
        return jsonify({'message': 'PR reviewed'}), 200
    else:
        logging.error(f'Error processing PR with code: {result}')
        return jsonify({'message': f'Error processing PR with code: {result}'}), 400


if __name__ == '__main__':
    logging.debug("{0}: {1}".format("LLM_ENDPOINT", os.environ.get("LLM_ENDPOINT")))
    logging.debug("{0}: {1}".format("LLM_MODEL_NAME", os.environ.get("LLM_MODEL_NAME")))
    logging.debug("{0}: {1}".format("LLM_API_VERSION", os.environ.get("LLM_API_VERSION")))
    app.run(host='0.0.0.0', port=5000)
