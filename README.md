# README Documentation

## Project Overview

This project is a bot designed to perform code reviews when repository sends a `pull_request` *opened* webhook. The bot fetches the code differences from the pull request, analyzes them using an LLM model, and posts comments on the pull request with feedback or simply states "no comments" if no issues are found. When the bot has finished its review, a bot_reviewed label is added to the pull request.

## How to Run

To run the project, you can use Docker Compose. Below are the required and optional environment variables:

### Required Environment Variables

- `REPOSITORY_OAUTH_TOKEN`: OAuth token for repository.
- `LLM_ENDPOINT`: LLM model endpoint.
- `LLM_API_KEY`: LLM model API key.
- `LLM_MODEL_NAME`: The LLM model name, such as `gpt4`.
- `LLM_API_VERSION`: LLM API version.
- `REVIEW_IMPLEMENTATION`: The review implementation to use (AZURE, DUMMY, etc).
- `REPOSITORY_IMPLEMENTATION`: The repository implementation to use (GITHUB, DUMMY, etc).

### Optional Environment Variables

- `REPOSITORY_API`: To change the Repository API (useful for on-premise repository instances).
- `LLM_PROMPT`: To adjust the system prompt that the LLM model receives.
- `REPOSITORY_LABEL`: To override the label `bot_reviewed` that the bot puts on the pull request.
- `WEBHOOK_SECRET`: When applicable, the secret token for the Repository webhook. Leave empty if not needed.

### Docker Compose Configuration

Here is an example of how to configure the `docker-compose.yml` file:

```yaml
services:
  review-gpt:
    image: codehouseou/review-gpt:1.1.0
    env_file:
      - configuration.env
    ports:
      - "8080:5000"
```
Rename the `configuration.env.sample` file to `configuration.env` and fill in the required environment variables.
To run the project, execute the following command:

```sh
docker compose up
```

This will start the bot, and it will be ready to process pull request opened webhooks from repository on root path.
## Development Principles

### Extending the System with New Review and Repository Classes

 > Ensure all required dependencies for the new class are installed. You can update the `requirements.txt` or provide installation instructions.

To extend the system with new review and repository classes, follow these steps:

1. **Create New Review Class**:
    - Implement the `ReviewInterface` for the new review class.
    - Add the new class to the `ReviewFactory`.

2. **Create New Repository Class**:
    - Implement the `RepositoryInterface` for the new repository class.
    - Add the new class to the `RepositoryFactory`.

### Example: Adding a New Review Class

1. **Create the new review class**:
    ```python
    class NewReviewService(ReviewInterface):
        def review(self, diff: str) -> str:
            return "Review by NewReviewService"
    ```

2. **Update `ReviewFactory`**:
    ```python
    class ReviewFactory:
        def get_review_service(self) -> ReviewInterface:
            implementation_name = self.config.review_implementation.upper()
            if implementation_name == 'DUMMY':
                return DummyReview(self.config)
            elif implementation_name == 'AZURE':
                return ChatGptService(self.config)
            elif implementation_name == 'NEW':
                return NewReviewService(self.config)
            else:
                raise ValueError(f"Unknown review implementation: {implementation_name}")
    ```

### Example: Adding a New Repository Class

1. **Create the new repository class**:
    ```python
    class NewRepositoryService(RepositoryInterface):
        def fetch_diff(self, repo_full_name, pull_number) -> str:
            return "Diff from NewRepositoryService"
        
        def add_label(self, repo_full_name, pull_number, label) -> None:
            pass
        
        def post_comment(self, repo_full_name, pull_number, comment_body) -> None:
            pass
        
        @staticmethod
        def is_supported_payload(payload) -> bool:
            return True
        
        @staticmethod
        def get_repo_name(payload) -> str:
            return "repo_name_new"
        
        @staticmethod
        def get_pull_number(payload) -> str:
            return "pull_number_new"
    ```

2. **Update `RepositoryFactory`**:
    ```python
    class RepositoryFactory:
        def get_repository_service(self) -> RepositoryInterface:
            implementation_name = self.config.repository_implementation.upper()
            if implementation_name == 'DUMMY':
                return DummyRepository(self.config)
            elif implementation_name == 'GITHUB':
                return GitHubService(self.config)
            elif implementation_name == 'NEW':
                return NewRepositoryService(self.config)
            else:
                raise ValueError(f"Unknown repository implementation: {implementation_name}")
    ```

### Configuration Parameters

To configure which implementation is used, set the following parameters in your configuration:

- `REVIEW_IMPLEMENTATION`: Specifies the review implementation to use. Possible values: `DUMMY`, `AZURE`, `NEW`, etc.
- `REPOSITORY_IMPLEMENTATION`: Specifies the repository implementation to use. Possible values: `DUMMY`, `GITHUB`, `NEW`, etc.
