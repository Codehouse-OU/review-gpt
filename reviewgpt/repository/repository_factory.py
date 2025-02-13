import logging

from reviewgpt.repository.dummy_repository import DummyRepository
from reviewgpt.repository.gitea import GiteaService
from reviewgpt.repository.github import GitHubService
from reviewgpt.repository.repository_interface import RepositoryInterface
# Set up logging
logging.basicConfig(level=logging.DEBUG)


class RepositoryFactory:
    def __init__(self, config):
        self.config = config

    def get_repository_service(self) -> RepositoryInterface:
        implementation_name = self.config.repository_implementation.upper()
        if implementation_name == 'DUMMY':
            logging.debug("Using DummyRepository")
            return DummyRepository(self.config)
        elif implementation_name == 'GITHUB':
            logging.debug("Using GitHubService")
            return GitHubService(self.config)
        elif implementation_name == 'GITEA':
            logging.debug("Using GiteaService")
            return GiteaService(self.config)
        # Add a new implementation for other repos if needed
        else:
            raise ValueError(f"Unknown repository implementation: {implementation_name}")
