from openai import AzureOpenAI
from webservice.configuration.configuration import Configuration
config = Configuration()

class ChatGptService(object):
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=config.endpoint,
            api_version=config.api_version,
            api_key=config.key
        )

    def generate_response(self, code_diff):
        completion = self.client.chat.completions.create(
            model=config.model_name,
            messages=[config.system_message, {"role": "user", "content": code_diff}],
        )
        return completion.choices[0].message.content
