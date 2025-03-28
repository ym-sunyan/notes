from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
# from langchain_community.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import retrieval_qa
from langchain.chains.retrieval_qa.base import RetrievalQA

# 初始化嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 初始化向量数据库
vectordb = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_data"
)

# 加载文档
loader = TextLoader(r"C:\Dropbox\YAN\D\2025\zhiguol\LocalRAGFullTextSearch\rag本地模型部署.md", encoding='utf-8')
documents = loader.load()

# 分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
texts = text_splitter.split_documents(documents)

# 将文档添加到向量数据库
vectordb.add_documents(texts)

# 初始化语言模型
# llm = Ollama(model="nomic-embed-text")

# # 创建检索增强生成链
# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",
#     retriever=vectordb.as_retriever()
# )
# from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
llm = Ollama(model="llama2")
# llm = Ollama(model="deepseek-r1:1.5b")

template = "Answer the following question: {question}"
prompt = PromptTemplate(template=template, input_variables=["question"])


# qa_chain = LLMChain(llm=llm, prompt=prompt)

# 创建 RunnableSequence
qa_chain = RunnableSequence(prompt | llm)

# response = qa_chain.run(question="What is the capital of France?")
response = qa_chain.invoke({"question": "What is the capital of France?"})
print(response)

# 提问
question = "文档预处理使用的方法"
question = "Methods used for document pre-processing?"
# response = qa_chain.run(question)
response = qa_chain.invoke({"question": question})

# 打印回答
print(response)