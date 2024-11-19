# export OPENAI_API_KEY="..."
# export LANGCHAIN_API_KEY="..."
# export LANGCHAIN_TRACING_V2="true"
# pip3 install bs4 langchain langchain-openai langchain-openai langchain_chroma langchain-text-splitters langchain_community
# phyton3 langchain-rag-chain.py

import bs4
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o")

loader = WebBaseLoader(
  web_paths=(
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
  ),
  bs_kwargs=dict(
    parse_only=bs4.SoupStrainer(
      class_=("post-content", "post-title", "post-header")
    )
  ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1000,
  chunk_overlap=200
)
splits = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(
  model="text-embedding-3-large"
)

vectorstore = Chroma.from_documents(
  documents=splits,
  embedding=embeddings
)
# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever(
  search_type="similarity",
  search_kwargs={"k": 6}
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

parser = JsonOutputParser()
query = "agent memory"
retrieved = retriever.invoke(query)
retrieved_text = ""
for chunk in retrieved:
    retrieved_text += chunk.page_content

# 4번
prompt1 = PromptTemplate(
  template="Answer the user query.\n{format_instructions}\n{query}\n",
  input_variables=["query"],
  partial_variables={"format_instructions": parser.get_format_instructions()}
)
chain1 = prompt1 | llm | parser
result1 = chain1.invoke({"query": query})
print(result1)

# 5번
prompt2 = PromptTemplate(
  template="""You are a system that receives a query from a user and provides a final answer.
However, after looking at the retrieval result, you will refer only to the retrieved chunks that have relevance and provide a final answer.

If the retrieved chunks are relevant, output them in JSON format in the form of relevance: yes for each chunk number, or relevance: no if they are not relevant.

Below is information about the user query and retrieved chunk.

query: {query}
retrieved chunks: {retrieved_docs}
""",
  input_variables=["query", "retrieved_docs"],
  partial_variables={"format_instructions": parser.get_format_instructions()}
)
chain2 = prompt2 | llm | parser
result2 = chain2.invoke({
  "query": query,
  "retrieved_docs": retrieved_text
})
print(result2)

# 8번~
prompt3 = PromptTemplate(
  template="""You are a system that receives a query from a user and provides a final answer.
However, after looking at the retrieval result, you will refer only to the retrieved chunks that have relevance and provide a final answer.
After performing the steps below, print out the final answer.

The answers are printed in detail for each step.
Step1) Look at the retrieved chunks and if they are relevant, output them in JSON format in the form of relevance: yes for each chunk number and relevance: no if they are not relevant.
Step2) If one or more chunks have relevance: yes, generate an answer by referring only to those chunks.
Step3) Evaluate whether there was a hallucination in the final answer, and if there was, output hallucination: yes. If not, output hallucination: no.
Step4) If hallucination: no, go back to Step3 and generate an answer again. This process is only performed once to prevent an infinite loop.
Step5) Create a final answer by synthesizing the information so far

Below is information about the user query and retrieved chunk.

query: {query}
retrieved chunks: {retrieved_docs}
""",
  input_variables=["query", "retrieved_docs"]
)
chain3 = prompt3 | llm | StrOutputParser()
result3 = chain3.invoke({
  "query": query,
  "retrieved_docs": retrieved_text
})
print(result3)
