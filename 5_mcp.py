'''
暂时还没有跑通 FileManagerAgent 的逻辑
'''

import os
from autogen import AssistantAgent, UserProxyAgent,register_function
from llm_config import config_list_local_qwen3_deepseek_8b,config_list_local_qwen3_32b
from autogen.agentchat.contrib.file_manager_agent import FileManagerAgent



# 确保目录存在
if not os.path.exists("output"):
    os.makedirs("output")


# 加载配置
llm_config = {
    "config_list": {"model":"qwen/qwq-32b",
                    "base_url": "http://127.0.0.1:8888/v1",
                    "api_key": "lm-studio",
                    "extra_body": {
                        "enable_thinking": False  # 添加此参数
                    }},
    "timeout": 120,  # 请求超时时间
    "temperature": 0.7,  # 温度值
    "max_tokens": 3000,  # 最大生成长度
    "cache_seed": None,  # 禁用缓存
}


file_manager = FileManagerAgent(
    name="file_manager",
    root_dir="output",  # 文件操作的根目录
    human_input_mode="NEVER"
)

# 初始化代理
assistant = AssistantAgent(name="WriterAgent",
                           llm_config=llm_config,
                           system_message=(
        "你是一个专业的小说作者，总能根据用户的核心设定，快速编写游戏大纲。"
        "大纲写完后，请将内容通过文件管理器代理保存为'output/title.txt'。"
        "你可以直接向 file_manager 发送写文件请求，格式如下："
        "请将以下内容写入 output/title.txt 文件：<内容>"
    ))



user_proxy = UserProxyAgent(name="user_proxy", 
                            human_input_mode="NEVER",
                            max_consecutive_auto_reply=1,
                            code_execution_config={"use_docker":False})


# 开始对话
user_proxy.initiate_chat(
    assistant,
    message="请根据'赛博修仙'写一个大纲"
)
