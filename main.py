from components.llm.HuggingFaceLLM import HuggingFaceLLM
import autogen

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


renter = autogen.AssistantAgent(
    name="Max Müller",
    system_message="You are interested in Harald Heines' apartment. The negotiation takes place in the apartment of interest. Negotiate with Harald Heines' about a price you can both agree on.",
    llm_config=llm_config,
)

landlord = autogen.AssistantAgent(
    name="Harald Heine",
    system_message="You are Harald Heine and you own an apartment. A student called Max Müller wants to rent the apartment from you. Negotiate with Max Müller about a price you can both agree on.",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[renter, landlord], messages=[], max_round=12)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

renter.initiate_chat(manager, message="Hello Mister Heine, how are you?")
