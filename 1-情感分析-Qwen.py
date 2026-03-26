#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import json #注销掉没用到的引入
import os
import dashscope
# from dashscope.api_entities.dashscope_response import Role #注销掉没用到的引入

# 从环境变量中，获取 DASHSCOPE_API_KEY
# api_key = os.environ.get('DASHSCOPE_API_KEY')
api_key = os.getenv('DASHSCOPE_API_KEY')
#  os.getenv用法跟 os.environ.get一样，都是获取环境变量的值，如果环境变量不存在，则返回None。两者的区别在于，os.getenv是一个函数，而os.environ是一个字典对象。使用os.getenv可以直接获取环境变量的值，而使用os.environ需要通过键来访问对应的值。

# dashscope.api_key = api_key # 也可以直接设置dashscope的api_key属性，这样在调用dashscope的函数时就不需要每次都传入api_key参数了。
# 封装模型响应函数
def get_response(messages):
    response = dashscope.Generation.call(
        model='deepseek-v3',
        messages=messages,
        api_key=api_key,
        result_format='message'  # 将输出设置为message形式
    )
    return response
    
# review = '这款音效特别好 给你意想不到的音质。'
review =input('这款音响怎么样：')
messages=[
    {"role": "system", "content": "你是一名舆情分析师，帮我判断产品口碑的正负向，回复请用一个词语：正向 或者 负向"},
    {"role": "user", "content": review}
  ]

response = get_response(messages)
print(response.output.choices[0].message.content)

print(response)

