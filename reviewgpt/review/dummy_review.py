from reviewgpt.review.review_interface import ReviewInterface


class DummyReview(ReviewInterface):
    """
    Dummy review for testing purposes
    """
    def __init__(self, config):
        self.config = config

    def execute(self, code_diff):
        return "NO_COMMENTS"
