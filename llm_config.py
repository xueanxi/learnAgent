


config_list_qwen3_8b = [
    {
        "model": "qwen3-8b",  # 支持的模型：qwen-plus, qwen-turbo, qwen-max 等
        "api_key": "sk-40da8cec14d54379bae3306c7b40d4d9",  # 替换为你的 DashScope API Key
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",  # 重要！使用兼容OpenAI的代理接口
        "api_type": "openai",  # 自定义标签（可选）
        "extra_body": {
            "enable_thinking": False  # 添加此参数
        }
    },
]


config_list_qwen3_4b = [
    {
        "model": "qwen3-4b",
        "api_key": "sk-40da8cec14d54379bae3306c7b40d4d9",  # 替换为你的 DashScope API Key
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",  # 重要！使用兼容OpenAI的代理接口
        "api_type": "openai",  # 自定义标签（可选）
        "extra_body": {
            "enable_thinking": False  # 添加此参数
        }
    },
]



config_list_qwen_turbo = [
    {
        "model": "qwen-turbo",  # 支持的模型：qwen-plus, qwen-turbo, qwen-max 等
        "api_key": "sk-40da8cec14d54379bae3306c7b40d4d9",  # 替换为你的 DashScope API Key
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",  # 重要！使用兼容OpenAI的代理接口
        "api_type": "openai",  # 自定义标签（可选）
    }
]


config_list_local_qwen3_32b = [
    {
        "model": "qwen/qwq-32b",  # 与 LM Studio 中选择的模型名相同
        "base_url": "http://127.0.0.1:8888/v1",  # LM Studio 默认地址
        "api_key": "lm-studio",  # 任意值即可，因为本地无需验证
        "extra_body": {
            "enable_thinking": False  # 添加此参数
        }
    }
]

config_list_local_qwen3_deepseek_8b = [
    {
        "model": "lmstudio-community/deepseek-r1-0528-qwen3-8b",  # 与 LM Studio 中选择的模型名相同
        "base_url": "http://localhost:8888/v1",  # LM Studio 默认地址
        "api_key": "lm-studio",  # 任意值即可，因为本地无需验证
        "extra_body": {
            "enable_thinking": False  # 添加此参数
        }
    }
]



