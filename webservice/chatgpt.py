from openai import AzureOpenAI

from review_interface import ReviewInterface


class ChatGptService(ReviewInterface):
    def __init__(self, config):
        self.config = config
        self.client = AzureOpenAI(
            azure_endpoint=config.endpoint,
            api_version=config.api_version,
            api_key=config.key
        )

    def review(self, code_diff):
        completion = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=[self.config.system_message, {"role": "user", "content": code_diff}],
        )
        return completion.choices[0].message.content
