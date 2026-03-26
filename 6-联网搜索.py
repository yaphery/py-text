#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from openai import OpenAI
# 从环境变量中，获取 DASHSCOPE_API_KEY
api_key = os.environ.get('DASHSCOPE_API_KEY')

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=api_key, 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
)
content=input('请输入问题：')
# 中国队在巴黎奥运会获得了多少枚金牌？
completion = client.chat.completions.create(
    model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': content}
    ],
    extra_body={
        "enable_search": True
    }
    )


# print(completion)               # 看全部
# print(completion.choices)       # 看候选回答
# print(completion.choices[0].message)  # 看消息
print(completion.choices[0].message.content)  # 看最终文本
# print(type(completion))         # 看类型，OpenAIResponse对象

print(completion.model_dump_json())

"""
 <class 'openai.types.chat.chat_completion.ChatCompletion'>
 OpenAI 官方返回的对象= 不能用 ["key"]= 必须用.点语法= 取内容用：completion.choices[0].message.content

 os.environ.get('DASHSCOPE_API_KEY')
 os.getenv('DASHSCOPE_API_KEY')
 这两种方式都可以获取环境变量的值，如果环境变量不存在，则返回None。两者的区别在于，os.getenv是一个函数，而os.environ是一个字典对象。使用os.getenv可以直接获取环境变量的值，而使用os.environ需要通过键来访问对应的值。

 
 extra_body={
    "enable_search": True 阿里云开启联网搜索，这是阿里云自己定义的功能，不是 OpenAI 的 ，必须放在 extra_body 里才能传给阿里云，因为 OpenAI 官方没有这个参数，所以用 extra_body 作为透传通道。
 }
 这个是开启模型的联网搜索能力，但是只有用client.chat.completions.create()这个接口才行，如果用client.responses.create()这个新接口，就算加了extra_body={"enable_search": True}，也不起作用，模型依然无法联网搜索。
"""



