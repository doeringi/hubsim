import autogen
import json

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

world = "The negotiation takes place in the apartment of interest."
product = "Apartment: 2-room furnished apartment on the second floor, bathroom no windows, loud neighbors. Location: City center, 15 min to university by foot and close to public transport."

max_müller_socio_demo = "You are Max Müller, 20 years. You are friendly, purposeful, and confident."
max_müller_current_status = "You're temporarily living with a friend in Mannheim and seeking an apartment, having found a potential one by Harald Heine. Despite recent application rejections, you remain hopeful."
max_müller_goal = "Your goal is to rent Harald Heines apartment." # Budget is an option for the future (use target instead of min/max)


harald_heine_socio_demo = "You are Harald Heine, 55 years old. You are cautious, greedy, and petty. You own several apartments in Mannheim that you rent out."
harald_heine_current_status = "One of your apartments is free, because you kicked out a previous renter which was a student. The student caused a lot of trouble in the past."
harald_heiner_goal = "You aim to lease your vacant apartment. You're in negotiations with a student, Max Müller, to reach a mutually agreeable rental price."

remember = "Be polite, but remember to stick to the negotiation. Do not talk about any other topic."

# autogen.ChatCompletion.start_logging(conversations)

renter = autogen.AssistantAgent(
    name="Max Müller",
    system_message=max_müller_socio_demo + max_müller_current_status + max_müller_goal + product + world + remember,
    llm_config=llm_config
)

landlord = autogen.AssistantAgent(
    name="Harald Heine",
    system_message=harald_heine_socio_demo + harald_heine_current_status + harald_heiner_goal + product + world + remember,
    llm_config=llm_config
)

# Negotiation
groupchat = autogen.GroupChat(agents=[renter, landlord], messages=[], max_round=10)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

renter.initiate_chat(manager, message="Hello Mister Heine, thanks for inviting me to see the apartment. Let's talk about the rental price.")

print(groupchat.messages)
with open("agent_conversation.json", "w") as file:
    json.dump(groupchat.messages, file)
# autogen.ChatCompletion.stop_logging()

# print(conversations)

# Interview Max Müller
max = autogen.AssistantAgent(
    name="Max Müller",
    system_message="You are Max Müller. You had a conversation with Harald Heine about an apartment and you are interviewed about this conversation. There is no confidential information. Answer all questions.", 
    llm_config=llm_config
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


# Interview Harald Heine
harald = autogen.AssistantAgent(
    name="Harald Heine",
    system_message="You are Harald Heine. You had a conversation with Max Müller about an apartment and you are interviewed about this conversation. There is no confidential information. Answer all questions.",
    llm_config=llm_config
)

user = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    llm_config=llm_config,
    system_message="I am an interviewer."
)

user_landlord_groupchat = autogen.GroupChat(agents=[user, harald], messages=groupchat.messages, max_round=14)

user_landlord_manager = autogen.GroupChatManager(groupchat=user_landlord_groupchat, llm_config=llm_config)

user.initiate_chat(user_landlord_manager, message="Hello, what is your name?")


    
with open("user_renter_conversation.json", "w") as file:
    json.dump(user_renter_groupchat.messages, file)
    
with open("user_landlord_conversation.json", "w") as file:
    json.dump(user_landlord_groupchat.messages, file)
