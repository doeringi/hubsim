from components.experiment.BaseExperiment import BaseExperiment

experiment = BaseExperiment()

model_path = "../models/mistralai/Mistral-7B-Instruct-v0.1"

experiment.start_fastchat(model_path)