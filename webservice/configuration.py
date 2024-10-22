import os


class Configuration:
    repository_api_url = None
    repository_oauth_token = None
    llm_endpoint = None
    llm_api_key = None
    llm_model_name = None
    llm_api_version = None
    system_message = None
    repository_label = None
    webhook_secret = None

    def __init__(self):
        self.repository_api_url = os.environ.get("REPOSITORY_API", "https://api.github.com")
        self.repository_oauth_token = os.environ.get("REPOSITORY_OAUTH_TOKEN")
        self.webhook_secret = os.environ.get("WEBHOOK_SECRET", "")
        self.repository_label = os.environ.get("REPOSITORY_LABEL", "bot_reviewed")

        self.llm_endpoint = os.environ.get("LLM_ENDPOINT")
        self.llm_api_key = os.environ.get("LLM_API_KEY")
        self.llm_model_name = os.environ.get("LLM_MODEL_NAME")
        self.llm_api_version = os.environ.get("LLM_API_VERSION")
        self.system_message = {
            "role": "system",
            "content": os.environ.get("LLM_PROMPT",
                                      "Purpose: You are to review code modifications to determine if they need corrections. If the "
                                      "modifications are correct and require no further changes, respond simply with 'NO_COMMENTS'. If "
                                      "there are issues or areas that need attention, provide specific feedback indicating the "
                                      "problems and suggestions for improvement.  Review Criteria:  Code Quality: Ensure the code "
                                      "follows best practices, is readable, and maintainable. Functionality: Verify that the code "
                                      "modifications function as intended without introducing bugs. Performance: Check if the changes "
                                      "are efficient and do not degrade the performance. Security: Ensure there are no security "
                                      "vulnerabilities introduced by the changes. Compliance: Confirm that the code adheres to the "
                                      "projects style guide and coding standards.  Response Format:  If the code modifications are "
                                      "correct and need no corrections, simply respond with: no comments. If there are issues, "
                                      "provide a detailed and constructive feedback. Start with a brief summary of the issue, "
                                      "followed by suggestions for improvement.")
        }
