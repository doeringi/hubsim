from components.llm.HuggingFaceLLM import HuggingFaceLLM
import time
from dotenv import load_dotenv
import os

load_dotenv()

llama2_access_token = os.environ.get("HF_LLAMA2_ACCESS_TOKEN")
model_id = "meta-llama/Llama-2-70b-chat-hf"

llm_helper = HuggingFaceLLM()

llm_helper.model_id = model_id

llm_helper.download_llm(access_token=llama2_access_token)
