from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langchain.llms import HuggingFacePipeline

model = AutoModelForSeq2SeqLM.from_pretrained("local-llm/google/flan-t5-small")

tokenizer = AutoTokenizer.from_pretrained("local-llm/google/flan-t5-small")

pipe = pipeline(task="text2text-generation", model=model, tokenizer=tokenizer)

llm = HuggingFacePipeline(pipeline=pipe)

prompt = (
    "You are John, Sara your wife asks what you want to eat for dinner. Your answer:"
)

output = llm(prompt)

print(output)
