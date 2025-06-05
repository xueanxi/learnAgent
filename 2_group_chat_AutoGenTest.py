from autogen import AssistantAgent, GroupChat, GroupChatManager
import os
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from llm_config import config_list_qwen_turbo,config_list_qwen3_4b,config_list_qwen3_8b

# 加载配置
llm_config = {
    "config_list": config_list_qwen3_8b,
    "timeout": 120,  # 请求超时时间,
    "cache_seed": 42 # 开启缓存，同时随机种子设置为42
}

# 初始化代理
assistantAsk = AssistantAgent("assistant_ask",
                           system_message="你是好奇的小孩，总喜欢问一些奇怪，每次都会问一个有趣的问题。",
                           llm_config=llm_config)
assistantAnswer = AssistantAgent("assistant_answer",
                           system_message="你是一个专业的AI助手，擅长回答用户提出的问题。当你完成回答后，请回复‘TERMINATE’以结束对话。",
                           llm_config=llm_config)

def my_termination_checker(msg):
    # 只要Assistant回复内容包含“再见”或“TERMINATE”就终止
    return "再见" in msg.get("content", "") or "TERMINATE" in msg.get("content", "")

user_proxy = UserProxyAgent(name="user_proxy", 
                            human_input_mode="NEVER",
                             code_execution_config={"use_docker":False},
                             is_termination_msg=my_termination_checker)
# 创建一个组
group_instance = GroupChat(agents=[assistantAsk, assistantAnswer], messages=[])
# 创建一个组管理器
group_manager = GroupChatManager(groupchat=group_instance,
                                 system_message="你是一个组管理员，负责管理组内的对话。当assistant_answer回答大于等于3个问题后,结束对话",
                                 llm_config=llm_config,
                                 max_consecutive_auto_reply=4,
                                 is_termination_msg=my_termination_checker)

# 开始对话
user_proxy.initiate_chat(
    group_manager,
    message="开始你们的对话吧"
)