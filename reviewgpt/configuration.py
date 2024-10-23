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
    skip_validation = None
    review_implementation = None
    repository_implementation = None

    good_job_message = None

    def __init__(self):
        self.repository_api_url = os.environ.get("REPOSITORY_API", "https://api.github.com")
        self.repository_oauth_token = os.environ.get("REPOSITORY_OAUTH_TOKEN")
        self.webhook_secret = os.environ.get("WEBHOOK_SECRET", "")
        self.repository_label = os.environ.get("REPOSITORY_LABEL", "bot_reviewed")
        self.skip_validation = os.environ.get("DANGER_SKIP_VALIDATION", '0')

        self.llm_endpoint = os.environ.get("LLM_ENDPOINT")
        self.llm_api_key = os.environ.get("LLM_API_KEY")
        self.llm_model_name = os.environ.get("LLM_MODEL_NAME")
        self.llm_api_version = os.environ.get("LLM_API_VERSION")
        self.review_implementation = os.environ.get("REVIEW_IMPLEMENTATION", "DUMMY")
        self.repository_implementation = os.environ.get("REPOSITORY_IMPLEMENTATION", "DUMMY")
        self.good_job_message = os.environ.get("GOOD_JOB_MSG", "All good, keep up the awesome work!")

        self.system_message = {
            "role": "system",
            "content": os.environ.get("LLM_PROMPT",
                                      "You are an AI code reviewer. Your task is to review code that is presented as a GIT diff. If you do not find anything noteworthy or requiring comments, you should return the string \"NO_COMMENTS\". If there are noteworthy comments or improvements, you should format your response as a JSON array adhering to the GitHub standard for creating review comments on a pull request. The position value equals the number of lines down from the first \"@@\" hunk header in the file you want to add a comment. The line just below the \"@@\" line is position 1, the next line is position 2, and so on. The position in the diff continues to increase through lines of whitespace and additional hunks until the beginning of a new file. If no comments are necessary, simply return: \"NO_COMMENTS\". Each JSON object in the array should include: - `body`: The comment or improvement suggestion. - `commit_id`: The string \"COMMIT_SHA_STUB\". - `path`: The file path from the GIT diff. **Example JSON Response (raw parseable json without any markdown):** [ { \"body\": \"file1 comment or improvements here\", \"commit_id\": \"COMMIT_SHA_STUB\", \"path\": \"file1.txt\", \"position\":1 }, { \"body\": \"file2 comment or improvements here\", \"commit_id\": \"COMMIT_SHA_STUB\", \"path\": \"file2.txt\", \"position\":2 } ]")
        }
