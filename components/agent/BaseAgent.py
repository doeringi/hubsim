from uuid import UUID
from typing import Optional
from components.agent import AbstractBaseAgent
from components.memory.observer import AbstractObserver
from components.memory.planner import AbstractPlanner
from components.memory.planner.prompts import planner_chains


class BaseAgent(AbstractBaseAgent, AbstractObserver, AbstractPlanner):
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
        action_emojie: str,
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
        self.action_emojie = action_emojie
        self.inner_voice = inner_voice
        self.memories = memories
        self.reflections = reflections
        self.plans = plans

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def observe(self) -> str:
        pass

    def plan_day(self):
        planner_chains.plan_day_chain.run()
        pass

    def set_daily_goals(self):
        pass

    def react(self):
        pass

    def update_plan(self):
        pass
