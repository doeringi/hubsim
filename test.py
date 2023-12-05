from components.experiment.BaseExperiment import BaseExperiment
import time

experiment = BaseExperiment()

model_path = "../models/mistralai/Mistral-7B-Instruct-v0.1"

experiment.start_fastchat(model_path)

print("Timeout")

time.sleep(60)

experiment.stop_fastchat()