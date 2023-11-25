from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import LlamaCppEmbeddings
from langchain.llms import LlamaCpp
from langchain import PromptTemplate
from langchain.chains import LLMChain
import time

model = 'llama-7b.ggmlv3.q4_0.bin'

embeddings = LlamaCppEmbeddings(model_path = 'path to' + model)
llm = LlamaCpp(model_path = 'path to' + model, n_gpu_layers=28, n_threads=6, n_ctx=4096, n_batch=512,  max_tokens = 5000, verbose=True)     # n_ctx=4096
prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
Answer:"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
loader = TextLoader('raw.txt')

docs = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)

texts = text_splitter.split_documents(docs)
print (texts)
db = Chroma.from_documents(texts, embeddings)

while True:
    start_time = time.time()
    query = input("I am ready for your questions : ")

    similar_doc = db.similarity_search(query, k=5)
    for t in range(len(similar_doc)):
        context = '' + similar_doc[t].page_content

    query_llm = LLMChain(llm=llm, prompt=prompt)
    response = query_llm.run({"context": context, "question" : query})

    print (context)
    print ("Response : ", response)
    print (time.time() - start_time)

# What was Harvey Dent's role in the Joker's plan

