from autogen import AssistantAgent
import os
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from llm_config import config_list_qwen_turbo

# 加载配置
llm_config = {
    "config_list": config_list_qwen_turbo,
    "timeout": 120,  # 请求超时时间
}

llm_config={
        "config_list": [{"model": "gpt-4", "api_key": "YOUR_KEY"}],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "write_to_file",
                    "description": "Write content to a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string"},
                            "content": {"type": "string"}
                        },
                        "required": ["file_path", "content"],
                    },
                }
            }
        ],
    }

# 初始化代理
assistant = AssistantAgent("assistant",
                           system_message="你是一个专业的AI助手，擅长回答用户提出的问题。当你完成回答后，请回复‘TERMINATE’以结束对话。",
                           llm_config=llm_config)

def my_termination_checker(msg):
    # 只要Assistant回复内容包含“再见”或“TERMINATE”就终止
    return "再见" in msg.get("content", "") or "TERMINATE" in msg.get("content", "")

user_proxy = UserProxyAgent(name="user_proxy", 
                            human_input_mode="NEVER",
                             code_execution_config={"use_docker":False},
                             is_termination_msg=my_termination_checker)

# 开始对话
user_proxy.initiate_chat(
    assistant,
    message="简单介绍一下相对论的概念"
)