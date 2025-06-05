import os
from autogen import AssistantAgent, UserProxyAgent,register_function
from llm_config import config_list_local_qwen3_deepseek_8b,config_list_local_qwen3_32b
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

# 定义工具函数
def write_to_file(file_path: str, content: str) -> str:
    print(f'write_to_file# 被调用 file_path:{file_path}')
    try:
        with open(file_path, 'w',encoding='utf-8') as f:
            f.write(content)
        return f"内容已成功写入 {file_path}"
    except Exception as e:
        return f"写入文件失败: {str(e)}"

# 初始化代理
assistant = AssistantAgent("assistant",
                           system_message="""
                           你是一个专业的小说作者，总能根据用户的用户核心设定，快速编写游戏大纲。
                           
                           创建故事骨架：
                           1. 三幕式结构（开端/发展/高潮各3个关键事件）
                           2. 设计主角成长弧线
                           3. 规划3个分卷内容

                           大纲写完后，调用工具，把大纲写入工作目录，命名为'title2.txt'
                           """,
                           llm_config=llm_config)



user_proxy = UserProxyAgent(name="user_proxy", 
                            human_input_mode="NEVER",
                            max_consecutive_auto_reply=1,
                            function_map={"write_to_file": write_to_file},
                             code_execution_config={"use_docker":False})

register_function(f=write_to_file,
                  caller=assistant,
                  executor=user_proxy,
                  name="write_to_file",
                  description="""将内容写入指定路径的文件
                  参数:
                  - file_path: 文件路径 (例如: 'report.txt')
                  - content: 要写入的内容 (字符串)""")

# 开始对话
user_proxy.initiate_chat(
    assistant,
    message="赛博修仙"
)
