from autogen import AssistantAgent, UserProxyAgent
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import json

# 步骤1: 准备向量数据库（ChromaDB）
def setup_vector_db():
    # 初始化 ChromaDB 客户端
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # 创建集合（collection）并指定嵌入模型
    embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = chroma_client.get_or_create_collection(
        name="knowledge_base",
        embedding_function=embedding_function
    )
    
    # 模拟文档数据（ID、文本、元数据）
    documents = [
        "微软AutoGen支持多代理协作系统。",
        "向量数据库用于存储和检索嵌入向量。",
        "RAG结合检索和生成技术提升回答质量。",
    ]
    metadatas = [{"source": "doc1"}, {"source": "doc2"}, {"source": "doc3"}]
    ids = ["id1", "id2", "id3"]
    
    # 插入数据到向量数据库
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    return collection

# 步骤2: 定义检索函数
def retrieve_from_vector_db(query: str, collection, n_results=2):
    results = collection.query(query_texts=[query], n_results=n_results)
    return results["documents"][0]  # 返回相关文档列表

# 步骤3: 配置AutoGen代理
# 用户代理（发起问题）
user_proxy = UserProxyAgent(
    name="User_Proxy",
    human_input_mode="ALWAYS",  # 用户实时输入问题
    code_execution_config={"work_dir": "coding"}
)

# 助理代理（回答用户问题）
qa_assistant = AssistantAgent(
    name="QA_Assistant",
    system_message="你是一个问答助手，使用知识库检索和生成技术回答问题。",
    llm_config={
        "config_list": [
            {
               "model":"qwen/qwq-32b",
                    "base_url": "http://127.0.0.1:8888/v1",
                    "api_key": "lm-studio",
                    "extra_body": {
                        "enable_thinking": False  # 添加此参数
                    }
            }
        ],
        "functions": [
            {
                "name": "retrieve_from_vector_db",
                "description": "从向量数据库检索相关文档",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "用户问题"}
                    },
                    "required": ["query"],
                },
            }
        ],
    }
)

# 注册检索函数（关键步骤！）
@user_proxy.register_for_execution()
@qa_assistant.register_for_llm(description="从向量数据库检索文档")
def retrieve_docs(query: str):
    return retrieve_from_vector_db(query, vector_db_collection)

# 步骤4: 初始化向量数据库
vector_db_collection = setup_vector_db()

# 步骤5: 启动对话
def ask_question(question):
    user_proxy.initiate_chat(
        qa_assistant,
        message=question,
    )

# 示例问题
ask_question("AutoGen是什么？")