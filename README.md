# README Documentation

## Project Overview

This project is a bot designed to perform code reviews when GitHub sends a `pull_request` opened webhook. The bot fetches the code differences from the pull request, analyzes them using an OpenAI model, and posts comments on the pull request with feedback or simply states "no comments" if no issues are found.

## How to Run

To run the project, you can use Docker Compose. Below are the required and optional environment variables:

### Required Environment Variables

- `GH_AUTH`: OAuth token for GitHub.
- `ENDPOINT`: Azure OpenAI endpoint.
- `API_KEY`: Azure OpenAI API key.
- `MODEL_NAME`: The model name, such as `gpt4`.
- `API_VERSION`: Azure OpenAI API version.

### Optional Environment Variables

- `GH_API`: To change the GitHub API (useful for on-premise GitHub instances).
- `PROMPT`: To adjust the system prompt that the OpenAI model receives.

### Docker Compose Configuration

Here is an example of how to configure the `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  review-gpt:
    image: codehouseou/review-gpt:latest
    environment:
      - GH_AUTH=${GH_AUTH}
      - ENDPOINT=${ENDPOINT}
      - API_KEY=${API_KEY}
      - MODEL_NAME=${MODEL_NAME}
      - API_VERSION=${API_VERSION}
#      - GH_API=${GH_API}
#      - PROMPT=${PROMPT}
    ports:
      - "8080:5000"
```

To run the project, execute the following command:

```sh
docker-compose up
```

This will start the bot and it will be ready to process pull request opened webhooks from GitHub.