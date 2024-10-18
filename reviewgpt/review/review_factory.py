import logging

from reviewgpt.review.chatgpt import ChatGptService
from reviewgpt.review.dummy_review import DummyReview
from reviewgpt.review.review_interface import ReviewInterface

# Set up logging
logging.basicConfig(level=logging.DEBUG)


class ReviewFactory:
    def __init__(self, config):
        self.config = config

    def get_review_service(self) -> ReviewInterface:
        implementation_name = self.config.review_implementation.upper()
        if implementation_name == 'DUMMY':
            logging.debug("Using DummyReview")
            return DummyReview(self.config)
        elif implementation_name == 'AZURE':
            logging.debug("Using ChatGptService")
            return ChatGptService(self.config)
        # Add a new implementation for other review services if needed
        else:
            raise ValueError(f"Unknown review implementation: {implementation_name}")
