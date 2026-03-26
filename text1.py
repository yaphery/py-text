"""
text1 -

Author:yaphery
Date:2026/3/24
"""
import os
from dashscope import Generation
print('os.environ.get("DASHSCOPE_API_KEY")',os.environ.get('DASHSCOPE_API_KEY'))
# 初始化请求参数
messages = [{"role": "user", "content": "你是谁？"}]
completion = Generation.call(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    model="deepseek-v3.2",
    messages=messages,
    result_format="message",  # 设置结果格式为 message
    enable_thinking=True,
    stream=True,              # 开启流式输出
    incremental_output=True,  # 开启增量输出
)

reasoning_content = ""  # 完整思考过程
answer_content = ""     # 完整回复
is_answering = False    # 是否进入回复阶段

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
print('completion',completion)

for chunk in completion:
    print('chunk', chunk)

    message = chunk.output.choices[0].message
    # 只收集思考内容
    if "reasoning_content" in message:
        if not is_answering:
            print(message.reasoning_content, end="", flush=True)
        reasoning_content += message.reasoning_content

    # 收到 content，开始进行回复
    if message.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(message.content, end="", flush=True)
        answer_content += message.content

print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
print(chunk.usage)