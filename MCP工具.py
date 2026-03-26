import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"（不建议）,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1"
)

# MCP 工具配置
mcp_tool = {
    "type": "mcp",
    "server_protocol": "sse",
    "server_label": "amap-maps",
    "server_description": "高德地图MCP Server，提供地图、导航、路径规划、天气查询等能力。",
    "server_url": "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse",
    "headers": {
        "Authorization": "Bearer " + os.getenv("DASHSCOPE_API_KEY")
    }
}

input=input("请输入问题：")
response = client.responses.create(
    model="qwen3.5-plus",
    input=input,
    tools=[mcp_tool],
       extra_body={
        "enable_search": True
    }
)

print("[模型回复]")
print(response.output_text)
print(f"\n[Token 用量] 输入: {response.usage.input_tokens}, 输出: {response.usage.output_tokens}, 合计: {response.usage.total_tokens}")


"""
client.responses.create()方法是openAI2025新接口，只要用了这个，任何扩展的功能（联网、工具）都会失效
"""