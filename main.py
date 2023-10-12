from components.llm.LocalLLM import LLM

llm = LLM()

llm.download_llm()

llm.load_llm()

t5_small_local_llm = llm.get_llm

prompt = "You are John. Sara your wife asks what you want to eat for dinner. Your answer to Saras question:"

output = t5_small_local_llm(prompt)

print(output)
