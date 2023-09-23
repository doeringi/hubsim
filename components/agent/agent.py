from uuid import UUID
from typing import Optional


class BaseAgent:
    id: UUID
    first_name: str
    last_name: str
    seed_memory: str  # initial memory specifying the agents biography
    current_action: str
    action_emojie: str
    inner_voice: str  # user commands
    memories: dict
    reflections: dict
    plans: dict

    def __init__(
        self,
        id: UUID,
        first_name: str,
        last_name: str,
        bio: str,
        current_action: str,
        action_emojie: str,
        memories: dict,
        reflections: dict,
        plans: dict,
        inner_voice: Optional[str] = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.seed_memory = bio
        self.current_action = current_action
        self.action_emojie = action_emojie
        self.inner_voice = inner_voice
        self.memories = memories
        self.reflections = reflections
        self.plans = plans
