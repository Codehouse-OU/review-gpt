class ReviewInterface:
    def review(self, diff: str) -> str:
        """
        Review the diff content and generate a response. When there are no comments to be made, return "NO_COMMENTS".
        When there are modifications, the system should respond with an array of comments:
        [
            {
                "path": "path/to/file",
                "commit_id": "...",
                "body": "comment message"
            }
        ]

        :param diff:
        :return: response
        """
        pass
