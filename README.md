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
