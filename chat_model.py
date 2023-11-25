from llama_cpp import Llama

llm = Llama(model_path='llama-7b.ggmlv3.q4_0.bin')

while True:
    question = input("Your question : ")
    response = llm(question, max_tokens=2000)

    print (response['choices'][0]['text'])

