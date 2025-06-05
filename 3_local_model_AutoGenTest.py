import os
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json,Agent
from llm_config import config_list_local_qwen3_deepseek_8b,config_list_local_qwen3_32b
import re
from CustomAgent import FilteredUserProxyAgent
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    Iterable,
    Literal,
    Optional,
    TypeVar,
    Union,
)


# 加载配置
llm_config = {
    "config_list": config_list_local_qwen3_32b,
    "timeout": 120,  # 请求超时时间
    "temperature": 0.7,  # 温度值
    "max_tokens": 2000,  # 最大生成长度
    "cache_seed": 43,  # 禁用缓存
}


'''
这段可以用于测试模型是否可用
import requests
response = requests.get("http://127.0.0.1:8888/v1/models")
print("response:",response.json())
'''

# 初始化代理
assistant = FilteredUserProxyAgent("assistant",
                           system_message="""
                           你是一个专业的小说作者，总能根据用户的用户核心设定，快速编写游戏大纲。

                           字数要求:200字以内
                           
                           创建故事骨架：
                           1. 三幕式结构（开端/发展/高潮各3个关键事件）
                           2. 设计主角成长弧线
                           3. 规划3个分卷内容
                           """,
                           llm_config=llm_config)

def my_termination_checker(msg):
    # 只要Assistant回复内容包含“再见”或“TERMINATE”就终止
    return "再见" in msg.get("content", "") or "TERMINATE" in msg.get("content", "")

user_proxy = UserProxyAgent(name="user_proxy", 
                            human_input_mode="NEVER",
                            max_consecutive_auto_reply=1,
                             code_execution_config={"use_docker":False},
                             is_termination_msg=my_termination_checker)

# 开始对话
user_proxy.initiate_chat(
    assistant,
    message="赛博修仙"
)