from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional


class AbstractBaseAgent(ABC):
    id: UUID
    first_name: str
    last_name: str
    seed_memory: str  # initial memory specifying the agents biography
    current_action: str
    inner_voice: str  # user commands
    memories: dict
    reflections: dict
    plans: dict

    def __init__(
        self,
        id: UUID,
        first_name: str,
        last_name: str,
        seed_memory: str,
        current_action: str,
        memories: dict,
        reflections: dict,
        plans: dict,
        inner_voice: Optional[str] = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.seed_memory = seed_memory
        self.current_action = current_action
        self.inner_voice = inner_voice
        self.memories = memories
        self.reflections = reflections
        self.plans = plans

    @property
    def id(self):
        return self.id

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @abstractmethod
    def init_agent_to_agent_conversation(self) -> list:
        raise NotImplementedError(
            'Abstract method "init_agent_to_agent_conversation" must be implemented'
        )

    @abstractmethod
    def init_agent_to_user_conversation(self) -> list:
        raise NotImplementedError(
            'Abstract method "init_agent_to_user_conversation" must be implemented'
        )

    @abstractmethod
    def run_single_factor_experiment(self):
        raise NotImplementedError(
            'Abstract method "run_single_factor_experiment" must be implemented'
        )

    @abstractmethod
    def save_conversation(self):
        raise NotImplementedError(
            'Abstract method "save_conversation" must be implemented'
        )
