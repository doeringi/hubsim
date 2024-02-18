from components.experiment.BaseExperiment import BaseExperiment
from components.common.variant_testing_helper import single_factor_variants_renter_name
import autogen
import os
import shutil
from datetime import datetime

mistral_config_list = [
    {
        "model": "Yi-34B-Chat",
        "base_url": "http://localhost:8000/v1",
        "api_key": "NULL",  # if not needed add NULL as placeholder
    }
]

mistral_llm_config = {
    "config_list": mistral_config_list,
    "cache_seed": 42,
    "temperature": 0.6,
    #               "timeout": 30,
    #               "max_retries": 5
}

bagel_config_list = [
    {
        "model": "bagel-dpo-34b-v0.2",
        "base_url": "http://localhost:8001/v1",
        "api_key": "NULL",  # if not needed add NULL as placeholder
    }
]

bagel_llm_config = {
    "config_list": bagel_config_list,
    "cache_seed": 42,
    "temperature": 0.6,
    #               "timeout": 30,
    #               "max_retries": 5
}

# model(s) to use
# models = ["mistralai/Mixtral-8x7B-Instruct-v0.1", "jondurbin/bagel-34b-v0.2"]
landlord_model = "bagel-dpo-34b-v0.2"
renter_model = "bagel-dpo-34b-v0.2"

# city and timestamp metadata
city_list = ["Duisburg", "Magdeburg", "München"]
city = city_list[0]  # the city that is used in the experiment (choose from city_list)
timestamp = datetime.now()
timestamp = timestamp.strftime("%Y%m%d")

# run configurations
number_of_experiments = (
    25  # number of experiments (one experiment = conversations) to run
)
max_rounds = (
    12  # maximum rounds in a conversation, where one round is one utterance of an agent
)
is_termination_msg = lambda x: True if "TERMINATE" in x.get("content") else False

# generate all variants
variants = single_factor_variants_renter_name()
variants = variants

for variant in variants:
    variant_folder = (
        "single-factor-experiments/"
        + "landlord"
        + "-"
        + landlord_model
        + "-"
        + variant[0][1]["name_id"]
        + "-"
        + renter_model
        + "-"
        + city
        + "-"
        + timestamp
        + "/"
    )  # create a folder with experiment metadata

    if not os.path.exists(variant_folder):
        os.makedirs(variant_folder)
        print(f"Folder '{variant_folder} created.")
    print("Starting experiment...")
    for experiment in range(0, number_of_experiments):
        try:
            experiment_helper = BaseExperiment()
            initial_chat_message = f"Hello Mister Schmidt, my name is {variant[0][1]['name_id']}. Thanks for inviting me to see the apartment in {city}. Let's talk about the rental price."
            renter = autogen.AssistantAgent(
                name=variant[0][1]["name_id"],
                system_message=variant[0][1]["renter_system_message"],
                llm_config=bagel_llm_config,
                is_termination_msg=is_termination_msg,
            )
            landlord = autogen.AssistantAgent(
                name=variant[0][0]["name_id"],
                system_message=variant[0][0]["landlord_system_message"],
                llm_config=bagel_llm_config,
                is_termination_msg=is_termination_msg,
            )

            print(f"Running experiment: {str(experiment_helper.id)}")

            # Note: The conversation is set to round_robin, therefore first speaker is set in agents
            conversation = experiment_helper.run_agent_to_agent_conversation(
                agents=[renter, landlord],
                max_round=max_rounds,
                llm_config=bagel_llm_config,
                init_chat_message=initial_chat_message,
            )
            experiment_helper.save_conversation(
                groupchat=conversation,
                path=variant_folder + "/" + str(experiment_helper.id),
            )

            if os.path.exists(".cache"):
                shutil.rmtree(".cache")

            print(f"Experiment with the id {experiment_helper.id} succeeded.")
        except Exception as e:
            print(f"An error occured: {e}. Trying again.")

            if os.path.exists(".cache"):
                shutil.rmtree(".cache")
