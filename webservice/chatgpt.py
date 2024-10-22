from openai import AzureOpenAI

from review_interface import ReviewInterface


class ChatGptService(ReviewInterface):
    def __init__(self, config):
        self.config = config
        self.client = AzureOpenAI(
            azure_endpoint=config.llm_endpoint,
            api_version=config.llm_api_version,
            api_key=config.llm_api_key
        )

    def review(self, code_diff):
        completion = self.client.chat.completions.create(
            model=self.config.llm_model_name,
            messages=[self.config.system_message, {"role": "user", "content": code_diff}],
        )
        return completion.choices[0].message.content
