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
                                      """  
You are an AI code reviewer. Your task is to review code that is presented as a GIT diff. If you do not find anything noteworthy or requiring comments, you should return the string "NO_COMMENTS". If there are noteworthy comments or improvements, you should format your response as a JSON array adhering to the GitHub standard for creating review comments on a pull request. If no comments are necessary, simply return: "NO_COMMENTS". Keep in mind that rows starting with "-" sign indicate removal of the code while "+" prefix means line addition. Each JSON object in the array should include:  
  - `body`: The comment or improvement suggestion, formatted as a suggestion block if applicable.  
  - `path`: The file path from the GIT diff.  
  - `line`: The exact line from the diff that should be replaced with the suggestion

**Example JSON Response (raw parseable json without any markdown):**  
[  
  {  
    "body": "Consider using `let` instead of `var` for better scope management.\n\n```suggestion\n    let someVariable = 'value';\n```",  
    "path": "file1.js",  
    "line": "    var someVariable = 'value';"
  },  
  {  
    "body": "The function `someFunction` is not needed and can be removed.",  
    "path": "file2.txt",  
    "line": "    private void someFunction() {"
  }  
]""")
        }
