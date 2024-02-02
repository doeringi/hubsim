## This script is for validation purposes of the evaluation agent. 
## It takes just 3 conversations per name and evaluates them.

from components.experiment.BaseExperiment import BaseExperiment

# from components.common.variant_testing_helper import single_factor_variants_renter_name
import autogen
import json
import os
import shutil
import time
import openai
import subprocess
from datetime import datetime
import re

# define the config_lists for both models
mistral_config_list = [
    {
        "model": "mistral-7b-instruct-v0.1",
        "base_url": "http://localhost:8000/v1",
        "api_key": "NULL",  # if not needed add NULL as placeholder
    }
]

bagel_config_list = [
    {
        "model": "bagel-9b-v0.1",
        "base_url": "http://localhost:8001/v1",
        "api_key": "NULL",  # if not needed add NULL as placeholder
    }
]


# set temperature for sampling
mistral_llm_config = {
    "config_list": mistral_config_list,
    "cache_seed": 42,
    "temperature": 0.6,
    #               "timeout": 30,
    #               "max_retries": 5
}


bagel_llm_config = {
    "config_list": bagel_config_list,
    "cache_seed": 42,
    "temperature": 0.6,
    #               "timeout": 30,
    #               "max_retries": 5
}

experiment_helper = BaseExperiment()

base_path = "single-factor-experiments"
experiment_path = "Yi-34B-Chat-name-origin-city-in-start-Mannheim-20240109"
evaluation_folder = "single-factor-controlled-evaluation-results-validation"

full_path = os.path.join(base_path, experiment_path)
print("Full path:", full_path)
print("Current Working Directory:", os.getcwd())

# ToDo:
# Folder Structure: new experiment path: landlord-model-[renter_name]-model-city-timestamp
# extract model from folder name and include config in agent based on the extracted model
# evaluation agent is always mixtral

if os.path.isdir(full_path):
    for name in os.listdir(full_path):
        experimental_path = full_path.split(os.path.sep)[1] # extract the experiment path
        model_renter = re.search('landlord-(.+?)-[renter_name]', experimental_path) # extract the llm used for the renter
        model_landlord = re.search('-[renter_name](.+?)-city-timestamp', experimental_path) # extract the llm used for the landlord
        name_path = os.path.join(full_path, name)
        for experiment_id in os.listdir(name_path)[0:2]: # should work (hopefully)
            experiment_id_path = os.path.join(name_path, experiment_id)
            for file in os.listdir(experiment_id_path):
                file_path = os.path.join(experiment_id_path, file)
                print("File path:", file_path)
                if os.path.isfile(file_path):
                    print("File found:", file_path)
                    path_parts = file_path.split(os.path.sep)
                    eval_result_sub_path = os.path.join(path_parts[1:])

                    conversation_history = json.load(open(file_path))
                    evaluator = autogen.AssistantAgent(
                        name="Evaluator",
                        system_message="Hello, my name is Evaluator. I will evaluate the conversation.",
                        llm_config=mistral_config_list, # we discussed to always use Mixtral here
                    )
                    
                    # define with which model the renter should answer (the same as in the experiment)
                    if model_renter == mistral_config_list["model"]:
                        config_renter = mistral_config_list,
                    elif model_renter == bagel_config_list["model"]:
                        config_renter = bagel_config_list

                    renter = autogen.AssistantAgent(
                        name="Renter Name",
                        system_message="Hello, my name is Renter Name. I will be interviewed.",
                        llm_config= config_renter
                    )
                    
                    # define with which model the landlord should answer (the same as in the experiment)
                    if model_landlord == mistral_config_list["model"]:
                        config_landlord = mistral_config_list,
                    elif model_landlord == bagel_config_list["model"]:
                        config_landlord = bagel_config_list
                        
                    landlord = autogen.AssistantAgent(
                        name="Landlord Name",
                        system_message="Hello, my name is Landlord Name. I will be interviewed.",
                        llm_config= config_landlord
                    )

                    evaluator_renter_chat = autogen.GroupChat(
                        agents=[evaluator, renter],
                        messages=conversation_history,
                        max_round=10,
                        speaker_selection_method="round_robin",
                        allow_repeat_speaker=False,
                    )

                    evaluator_landlord_chat = autogen.GroupChat(
                        agents=[evaluator, landlord],
                        messages=conversation_history,
                        max_round=10,
                        speaker_selection_method="round_robin",
                        allow_repeat_speaker=False,
                    )

                    evaluator_renter_manager = autogen.GroupChatManager(
                        groupchat=evaluator_renter_chat, llm_config=mistral_config_list # should this also be mixtral
                    )

                    evaluator.initiate_chat(
                        evaluator_renter_manager, message="init_chat_message"
                    )

                    experiment_helper.save_conversation(
                        groupchat=evaluator_renter_chat,
                        path=os.join(evaluation_folder, eval_result_sub_path),
                    )

                    evaluator_landlord_manager = autogen.GroupChatManager(
                        groupchat=evaluator_landlord_chat, llm_config=mistral_config_list # should this also be mixtral
                    )

                    evaluator.initiate_chat(
                        evaluator_landlord_manager, message="init_chat_message"
                    )

                    experiment_helper.save_conversation(
                        groupchat=evaluator_landlord_chat,
                        path=os.join(evaluation_folder, eval_result_sub_path),
                    )

                else:
                    print("File not found:", file_path)
else:
    print("Directory not found:", full_path)
