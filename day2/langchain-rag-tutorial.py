# export OPENAI_API_KEY="..."
# export LANGCHAIN_API_KEY="..."
# export LANGCHAIN_TRACING_V2="true"
# pip3 install bs4 langchain langchain-openai langchain-openai langchain_chroma langchain-text-splitters langchain_community
# phyton3 langchain-rag-tutorial.py

import bs4
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

llm = ChatOpenAI(model="gpt-4o-mini")

# prompt = hub.pull("rlm/rag-prompt")
# example_messages = prompt.invoke(
#   {
#     "context": "filler context",
#     "question": "filler question"
#   }
# ).to_messages()
# print(example_messages)

# Load, chunk and index the contents of the blog.
loader = WebBaseLoader(
  web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
  bs_kwargs=dict(
    parse_only=bs4.SoupStrainer(
      class_=("post-content", "post-title", "post-header")
    )
  ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
  {"context": retriever | format_docs, "question": RunnablePassthrough()}
  | prompt
  | llm
  | StrOutputParser()
)

example_message = rag_chain.invoke("What is Task Decomposition?")
print(example_message)
