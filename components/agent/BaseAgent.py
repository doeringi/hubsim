import uuid
from typing import Optional
from components.agent.AbstractBaseAgent import AbstractBaseAgent
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import json
import os


class BaseAgent(AbstractBaseAgent):
    id = uuid.UUID

    def __init__(
        self
    ):
        self.id = uuid.uuid4()
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def observe(self) -> str:
        pass

    def plan_day(self):
        pass

    def set_daily_goals(self):
        pass

    def react(self):
        pass

    def update_plan(self):
        pass

    def run_agent_to_agent_conversation(
        self, agents: list, max_round: int, llm_config, init_chat_message: str
    ):
        groupchat = GroupChat(agents=agents, messages=[], max_round=max_round)

        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
        
        agents[0].initiate_chat(manager, message=init_chat_message)

        return groupchat

    def run_agent_to_user_conversation(
        self, agents: list, max_round: int, message_history: list, llm_config, init_chat_message: str
    ):
        groupchat = GroupChat(
            agents=agents, messages=message_history, max_round=max_round
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
        
        agents[0].initiate_chat(manager, message=init_chat_message)

        return groupchat

    # def run_single_factor_experiment(
    #     self,
    #     agents: list,
    #     init_chat_agent: int,
    #     manager: GroupChatManager,
    #     init_chat_message: str,
    # ):
    #     agents[init_chat_agent].initiate_chat(manager, message=init_chat_message)

    def save_conversation(self, groupchat: GroupChat, path: str):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Folder '{path}' created.")
            
        file_path = os.path.join(path, "conversation.json")
        
        with open(file_path, "w") as file:
            json.dump(groupchat.messages, file)
            
        print("Saved conversation successfully.")
