from components.experiment.BaseExperiment import BaseExperiment
from components.common.variant_testing_helper import single_factor_variants_renter_name
import autogen
import json
import os
import shutil
import time
import openai
import subprocess

config_list = [
    {
        "model": "Yi-6B-Chat-8bits",
        "api_base": "http://localhost:8000/v1",
        "api_type": "open_ai",
        "api_key": "NULL",  # just a placeholder
        "timeout": 400,
        "max_retries": 100
    }
]

llm_config = {"config_list": config_list, "seed": 42}
autogen.ChatCompletion.start_logging()

def save_log_history(content, id):
    with open(f"single-factor-experiments/logs/experiment-log-{id}.json", "w") as file:
        json.dump(content, file)

variants = single_factor_variants_renter_name()
variants = variants

# run configurations
number_of_experiments = 50
initial_chat_message = "Hello Mister Heine, thanks for inviting me to see the apartment. Let's talk about the rental price."
max_rounds = 6
model_paths= ["../models/mistralai/Mistral-7B-Instruct-v0.1", "meta-llama/Llama-2-13b-chat-hf", "01-ai/Yi-6B-Chat-8bits"]
model_path =  "meta-llama/Llama-2-13b-chat-hf"

# start fastchat once
helper = BaseExperiment()
helper.start_fastchat(model_path=model_path)

for variant in variants:
    variant_folder = "single-factor-experiments/" + variant[0][1]["name_id"] # create a folder for renter name
    
    if not os.path.exists(variant_folder):
            os.makedirs(variant_folder)
            print(f"Folder '{variant_folder} created.")
    print("Starting experiment...")
    for experiment in range(0, number_of_experiments):
        
        max_retries = 10
        retry_delay = 4
        attempt = 0
        while attempt < max_retries:
            try:
                
                experiment_helper = BaseExperiment()
                
                renter = autogen.AssistantAgent(name=variant[0][1]["name_id"], system_message=variant[0][1]["renter_system_message"], llm_config=llm_config)
                landlord = autogen.AssistantAgent(name=variant[0][0]["name_id"], system_message=variant[0][0]["landlord_system_message"], llm_config=llm_config)
                
                print(f"Running experiment: {str(experiment_helper.id)}")
                conversation = experiment_helper.run_agent_to_agent_conversation(agents=[renter, landlord], max_round=max_rounds, llm_config=llm_config, init_chat_message=initial_chat_message)
                experiment_helper.save_conversation(groupchat=conversation, path=variant_folder + "/" + str(experiment_helper.id))
                
                if os.path.exists(".cache"):
                    shutil.rmtree(".cache")
                    
                print(f"Experiment with the id {experiment_helper.id} succeeded.")
                break
            except openai.error.Timeout as e:
                print("Timeout Error. Trying again...")
                attempt += 1
                
                if os.path.exists(".cache"):
                    shutil.rmtree(".cache")
                    
                if attempt >= 3:
                    experiment_helper.stop_fastchat()
                    experiment_helper.start_fastchat(model_path)
                        
                
                print(f"Try Counter: {attempt}")
                time.sleep(retry_delay)
            except Exception as e:
                print(f"An error occured: {e}. Trying again.")
                attempt += 1
                
                if os.path.exists(".cache"):
                    shutil.rmtree(".cache")
                
                if attempt >= 3:
                    experiment_helper.stop_fastchat()
                    experiment_helper.start_fastchat(model_path)
                
                print(f"Try Counter: {attempt}")
                time.sleep(retry_delay)


        
            