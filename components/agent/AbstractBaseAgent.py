from abc import ABC, abstractmethod
import uuid
from typing import Optional


class AbstractBaseAgent(ABC):
    id = uuid.UUID

    def __init__(
        self
    ):
        self.id = uuid.uuid4()


    @property
    def id(self):
        return self.id

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @abstractmethod
    def run_agent_to_agent_conversation(self) -> list:
        raise NotImplementedError(
            'Abstract method "init_agent_to_agent_conversation" must be implemented'
        )

    @abstractmethod
    def run_agent_to_user_conversation(self) -> list:
        raise NotImplementedError(
            'Abstract method "init_agent_to_user_conversation" must be implemented'
        )

    # @abstractmethod
    # def run_single_factor_experiment(self):
    #     raise NotImplementedError(
    #         'Abstract method "run_single_factor_experiment" must be implemented'
    #     )

    @abstractmethod
    def save_conversation(self):
        raise NotImplementedError(
            'Abstract method "save_conversation" must be implemented'
        )
