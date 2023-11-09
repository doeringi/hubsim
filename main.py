from components.llm.HuggingFaceLLM import HuggingFaceLLM
import autogen
import json

llm = HuggingFaceLLM()

llm.download_llm()

config_list = [
    {
        "model": "Mistral-7B-Instruct-v0.1",
        "api_base": "http://localhost:8000/v1",
        "api_type": "open_ai",
        "api_key": "NULL",  # just a placeholder
    }
]

llm_config = {"config_list": config_list, "seed": 42}

conversations = {}

# autogen.ChatCompletion.start_logging(conversations)

renter = autogen.AssistantAgent(
    name="Max Müller",
    system_message="You are Max Müller. You are interested in renting Harald Heines' apartment. The negotiation takes place in the apartment of interest. Negotiate with Harald Heines' about a price you can both agree on.",
    llm_config=llm_config,
)

landlord = autogen.AssistantAgent(
    name="Harald Heine",
    system_message="You are Harald Heine and you own an apartment that you want to rent out. Your apartment is a furnished apartment. It has two rooms and a bathroom without windows. It is located on the second floor in the city center with loud neighbors. The apartment is also close to public transportation. A student called Max Müller wants to rent the apartment from you. Negotiate with Max Müller about a price you can both agree on.",
    llm_config=llm_config,
)

# Negotiation
groupchat = autogen.GroupChat(agents=[renter, landlord], messages=[], max_round=10)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

renter.initiate_chat(manager, message="Hello Mister Heine, how are you?")

# Interview

max = autogen.AssistantAgent(
    name="Max Müller",
    system_message="You are Max Müller. You had a conversation with Harald Heine about an apartment and you are interviewed about this conversation.",
    llm_config=llm_config,
)

user = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    llm_config=llm_config,
    system_message="I am an interviewer.",
)

user_renter_groupchat = autogen.GroupChat(
    agents=[user, max], messages=groupchat.messages, max_round=14
)

user_renter_manager = autogen.GroupChatManager(
    groupchat=user_renter_groupchat, llm_config=llm_config
)

user.initiate_chat(user_renter_manager, message="Hello, what is your name?")

print(groupchat.messages)
with open("conversation.json", "w") as file:
    json.dump(groupchat.messages, file)

with open("user_renter_conversation.json", "w") as file:
    json.dump(user_renter_groupchat.messages, file)
