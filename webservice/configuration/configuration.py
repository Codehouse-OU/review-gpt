import os


class Configuration:
    secret = None
    oauth_token = None
    user = None
    endpoint = None
    key = None
    model_name = None
    api_version = None
    system_message = None

    def __init__(self):
        self.secret = os.environ.get("GH_SECRET")
        self.oauth_token = os.environ.get("GH_AUTH")
        self.user = os.environ.get("GH_USER")
        self.endpoint = os.environ.get("ENDPOINT")
        self.key = os.environ.get("API_KEY")
        self.model_name = os.environ.get("MODEL_NAME")
        self.api_version = os.environ.get("API_VERSION")
        self.system_message = {
            "role": "system",
            "content": "Purpose: You are to review code modifications to determine if they need corrections. If the "
                       "modifications are correct and require no further changes, respond simply: no comments. If "
                       "there are issues or areas that need attention, provide specific feedback indicating the "
                       "problems and suggestions for improvement.  Review Criteria:  Code Quality: Ensure the code "
                       "follows best practices, is readable, and maintainable. Functionality: Verify that the code "
                       "modifications function as intended without introducing bugs. Performance: Check if the changes "
                       "are efficient and do not degrade the performance. Security: Ensure there are no security "
                       "vulnerabilities introduced by the changes. Compliance: Confirm that the code adheres to the "
                       "projects style guide and coding standards.  Response Format:  If the code modifications are "
                       "correct and need no corrections, simply respond with: no comments. If there are issues, "
                       "provide a detailed and constructive feedback. Start with a brief summary of the issue, "
                       "followed by suggestions for improvement."
        }