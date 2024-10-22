import logging

from configuration import Configuration
from dummy_repository import DummyRepository
from github import GitHubService
from repository_interface import RepositoryInterface
# Set up logging
logging.basicConfig(level=logging.DEBUG)


class RepositoryFactory:
    def __init__(self, config: Configuration):
        self.config = config

    def get_repository_service(self) -> RepositoryInterface:
        implementation_name = self.config.repository_implementation.upper()
        if implementation_name == 'DUMMY':
            logging.debug("Using DummyRepository")
            return DummyRepository(self.config)
        elif implementation_name == 'GITHUB':
            logging.debug("Using GitHubService")
            return GitHubService(self.config)
        # Add a new implementation for other repos if needed
        else:
            raise ValueError(f"Unknown repository implementation: {implementation_name}")
