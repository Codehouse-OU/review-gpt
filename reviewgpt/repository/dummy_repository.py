import logging

from reviewgpt.repository.repository_interface import RepositoryInterface
# Set up logging
logging.basicConfig(level=logging.DEBUG)


class DummyRepository(RepositoryInterface):
    """
    Dummy repository for testing purposes
    """
    def __init__(self, config):
        self.config = config

    def fetch_diff(self, repo_full_name, pull_number):
        # return a GIT diff content where a mistake is made, where a method should return a string but returns an integer
        return """
        diff --git a/README.md b/README.md
index 9ce5b09..935d0e8 100644
--- a/README.md
+++ b/README.md
@@ -2,7 +2,7 @@
 
 ## Project Overview
 
-This project is a bot designed to perform code reviews when GitHub sends a `pull_request` opened webhook. The bot fetches the code differences from the pull request, analyzes them using an OpenAI model, and posts comments on the pull request with feedback or simply states "no comments" if no issues are found.
+This project is a bot designed to perform code reviews when repository sends a `pull_request` *opened* webhook. The bot fetches the code differences from the pull request, analyzes them using an LLM model, and posts comments on the pull request with feedback or simply states "no comments" if no issues are found. When the bot has finished its review, a bot_reviewed label is added to the pull request.
 
 ## How to Run
 
@@ -10,48 +10,37 @@ To run the project, you can use Docker Compose. Below are the required and optio
 
 ### Required Environment Variables
 
-- `GH_AUTH`: OAuth token for GitHub.
-- `ENDPOINT`: Azure OpenAI endpoint.
-- `API_KEY`: Azure OpenAI API key.
-- `MODEL_NAME`: The model name, such as `gpt4`.
-- `API_VERSION`: Azure OpenAI API version.
+- `REPOSITORY_OAUTH_TOKEN`: OAuth token for repository.
+- `LLM_ENDPOINT`: LLM model endpoint.
+- `LLM_API_KEY`: LLM model API key.
+- `LLM_MODEL_NAME`: The LLM model name, such as `gpt4`.
+- `LLM_API_VERSION`: LLM API version.
 
 ### Optional Environment Variables
 
-- `GH_API`: To change the GitHub API (useful for on-premise GitHub instances).
-- `PROMPT`: To adjust the system prompt that the OpenAI model receives.
-- `LABEL`: To override the label `bot_reviewed` that the bot puts on the pull request.
+- `REPOSITORY_API`: To change the Repository API (useful for on-premise repository instances).
+- `LLM_PROMPT`: To adjust the system prompt that the LLM model receives.
+- `REPOSITORY_LABEL`: To override the label `bot_reviewed` that the bot puts on the pull request.
+- `WEBHOOK_SECRET`: When applicable, the secret token for the Repository webhook. Leave empty if not needed.
 
 ### Docker Compose Configuration
 
 Here is an example of how to configure the `docker-compose.yml` file:
 
 ```yaml
-version: '3.8'
-
 services:
   review-gpt:
-    image: codehouseou/review-gpt:latest
-    environment:
-      - GH_AUTH=${GH_AUTH}
-      - ENDPOINT=${ENDPOINT}
-      - API_KEY=${API_KEY}
-      - MODEL_NAME=${MODEL_NAME}
-      - API_VERSION=${API_VERSION}
-      # Optional: override GitHub label that the bot puts to the pull request
-      #      - LABEL=${LABEL}
-      # Optional: define GitHub instance API url
-      #      - GH_API=${GH_API}
-      # Optional: define the system prompt for the LLM model
-    #      - PROMPT=${PROMPT}
+    image: codehouseou/review-gpt:1.1.0
+    env_file:
+      - configuration.env
     ports:
       - "8080:5000"
 ```
-
+Rename the `configuration.env.sample` file to `configuration.env` and fill in the required environment variables.
 To run the project, execute the following command:
 
 ```sh
-docker-compose up
+docker compose up
 ```
 
-This will start the bot and it will be ready to process pull request opened webhooks from GitHub.
+This will start the bot, and it will be ready to process pull request opened webhooks from repository on root path.
diff --git a/configuration.env.sample b/configuration.env.sample
new file mode 100644
index 0000000..bcf11ab
--- /dev/null
+++ b/configuration.env.sample
@@ -0,0 +1,6 @@
+REPOSITORY_OAUTH_TOKEN=
+WEBHOOK_SECRET=
+LLM_ENDPOINT=
+LLM_API_KEY=
+LLM_MODEL_NAME=
+LLM_API_VERSION=
diff --git a/docker-compose.yml b/docker-compose.yml
index 08bbf12..0a4bc19 100644
--- a/docker-compose.yml
+++ b/docker-compose.yml
@@ -2,18 +2,8 @@ version: '3.8'
 
 services:
   review-gpt:
-    image: codehouseou/review-gpt:1.0.11
-    environment:
-      - GH_AUTH=${GH_AUTH}
-      - ENDPOINT=${ENDPOINT}
-      - API_KEY=${API_KEY}
-      - MODEL_NAME=${MODEL_NAME}
-      - API_VERSION=${API_VERSION}
-      # Optional: override GitHub label that the bot puts to the pull request
-#      - LABEL=${LABEL}
-      # Optional: define GitHub instance API url
-#      - GH_API=${GH_API}
-      # Optional: define the system prompt for the LLM model
-#      - PROMPT=${PROMPT}
+    image: codehouseou/review-gpt:1.1.0
+    env_file:
+      - configuration.env
     ports:
       - "8080:5000"
diff --git a/webservice/app.py b/webservice/app.py
index 945c227..1c72288 100644
--- a/webservice/app.py
+++ b/webservice/app.py
@@ -3,8 +3,9 @@
 from flask import Flask, request, jsonify
 from chatgpt import ChatGptService
 from configuration import Configuration
+from app_service import AppService
+from dummy_repository import DummyRepository
 from github import GitHubService
-from webservice.app_service import AppService
 
 app = Flask(__name__)
 config = Configuration()
@@ -26,15 +27,21 @@ def bot_description():
 def bot_webhook():
     payload = request.json
     logging.debug(f'Payload received: {payload}')
+
+    if not app_service.is_valid_request(request):
+        logging.error('Invalid request')
+        return jsonify({'message': 'Invalid request'}), 400
     result = app_service.execute(payload)
     if result >= 0:
+        logging.debug(f'PR reviewed successfully with code: {result}')
         return jsonify({'message': 'PR reviewed'}), 200
     else:
+        logging.error(f'Error processing PR with code: {result}')
         return jsonify({'message': 'Error processing PR'}), 400
 
 
 if __name__ == '__main__':
-    logging.debug("{0}: {1}".format("ENDPOINT", os.environ.get("ENDPOINT")))
-    logging.debug("{0}: {1}".format("MODEL_NAME", os.environ.get("MODEL_NAME")))
-    logging.debug("{0}: {1}".format("API_VERSION", os.environ.get("API_VERSION")))
+    logging.debug("{0}: {1}".format("LLM_ENDPOINT", os.environ.get("LLM_ENDPOINT")))
+    logging.debug("{0}: {1}".format("LLM_MODEL_NAME", os.environ.get("LLM_MODEL_NAME")))
+    logging.debug("{0}: {1}".format("LLM_API_VERSION", os.environ.get("LLM_API_VERSION")))
     app.run(host='0.0.0.0', port=5000)
diff --git a/webservice/app_service.py b/webservice/app_service.py
index f2c0939..88970b2 100644
--- a/webservice/app_service.py
+++ b/webservice/app_service.py
@@ -1,6 +1,6 @@
-from webservice.configuration import Configuration
-from webservice.repository_interface import RepositoryInterface
-from webservice.review_interface import ReviewInterface
+from configuration import Configuration
+from repository_interface import RepositoryInterface
+from review_interface import ReviewInterface
"""

    def add_label(self, repo_full_name, pull_number, label):
        logging.debug(f"Adding label {label} to pull request {pull_number} in repository {repo_full_name}")
        pass

    def post_comment(self, repo_full_name, pull_number, comment_body):
        logging.debug(f"Posting comment to pull request {pull_number} in repository {repo_full_name}: {comment_body}")
        pass

    def post_review_comments(self, repo_full_name, pull_number, comments, commit_sha):
        logging.debug(f"Posting review comments to pull request {pull_number} in repository {repo_full_name}: {comments}")
        pass

    def is_valid_request(self, request_data_bytes: bytes, headers, secret: str) -> bool:
        logging.debug("Validating request")
        return True

    @staticmethod
    def is_supported_payload(payload) -> bool:
        logging.debug("Checking if payload is supported")
        return True

    @staticmethod
    def get_repo_name(payload) -> str:
        logging.debug("Getting repository name from payload")
        return 'test/test'

    @staticmethod
    def get_pull_number(payload) -> str:
        logging.debug("Getting pull request number from payload")
        return '1'

    @staticmethod
    def get_head_commit_sha(payload):
        logging.debug("Getting head commit SHA from payload")
        return "1234567890"

    def post_process(self, code_diff, message):
        logging.debug(f"Processing review comments: {message}")
        return [{'body': 'Comment', 'path': 'README.md', 'position': 1}]
