import json
import os
import requests
import dashscope
from dashscope.api_entities.dashscope_response import Role

# 从环境变量中，获取 DASHSCOPE_API_KEY
api_key = os.getenv('DASHSCOPE_API_KEY')
dashscope.api_key = api_key

amap_key = os.getenv('AMAP_KEY') or os.getenv('GAODE_KEY')
print('api_key=', api_key, 'amap_key=', amap_key)

# 编写你的天气函数
# 为了演示流程，这里指定了天气的温度，实际上可以调用 高德接口获取实时天气。
# 这里可以先用每个城市的固定天气进行返回，查看大模型的调用情况
def get_current_weather(location, unit="摄氏度"):
    """调用高德（AMap）天气接口获取指定地点的实时天气。

    需要在环境变量中设置 `AMAP_KEY`（或 `GAODE_KEY`）。
    返回 JSON 字符串（含中文字段），若出错会返回包含 `error` 字段的 JSON。
    """
    amap_key = os.environ.get('AMAP_KEY') or os.environ.get('GAODE_KEY')

    if not amap_key:
        return json.dumps({"error": "AMAP key not set. Please set environment variable AMAP_KEY or GAODE_KEY."}, ensure_ascii=False)

    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        'key': amap_key,
        'city': location,
        'extensions': 'base',  # base: 实时天气， all: 预报
        'output': 'JSON'
    }
    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        # 高德返回 status='1' 表示成功
        if str(data.get('status')) != '1':
            return json.dumps({"error": "AMap API error", "info": data.get('info')}, ensure_ascii=False)

        lives = data.get('lives') or []
        if not lives:
            return json.dumps({"location": location, "error": "no weather data returned", "raw": data}, ensure_ascii=False)

        live = lives[0]
        # live 包含: province, city, adcode, weather, temperature, winddirection, windpower, humidity, reporttime
        temp_c = None
        try:
            temp_c = float(live.get('temperature'))
        except Exception:
            temp_c = None

        if temp_c is None:
            temperature = None
            unit_out = unit
        else:
            if unit in ("摄氏度", "celsius", "C", "c", 'celsius'):
                temperature = round(temp_c, 1)
                unit_out = "摄氏度"
            else:
                temperature = round(temp_c * 9.0 / 5.0 + 32.0, 1)
                unit_out = "华氏度"

        weather_info = {
            "location": f"{live.get('province','')}{live.get('city','')}",
            "temperature": temperature,
            "unit": unit_out,
            "description": live.get('weather'),
            "winddirection": live.get('winddirection'),
            "windpower": live.get('windpower'),
            "humidity": live.get('humidity'),
            "reporttime": live.get('reporttime'),
            "raw": data
        }
        return json.dumps(weather_info, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

# 封装模型响应函数
def get_response(messages):
    try:
        response = dashscope.Generation.call(
            model='qwen-max',
            messages=messages,
            functions=functions,
            result_format='message'
        )
        return response
    except Exception as e:
        print(f"API调用出错: {str(e)}")
        return None

# 使用function call进行QA
def run_conversation(query):
    # query = "大连的天气怎样"
    messages=[{"role": "user", "content": query}]
    
    # 得到第一次响应
    response = get_response(messages)
    if not response or not response.output:
        print("获取响应失败")
        return None
        
    print('response=', response)
    
    message = response.output.choices[0].message
    messages.append(message)
    print('message=', message)
    
    # Step 2, 判断用户是否要call function
    if hasattr(message, 'function_call') and message.function_call:
        function_call = message.function_call
        tool_name = function_call['name']
        # Step 3, 执行function call
        arguments = json.loads(function_call['arguments'])
        print('arguments=', arguments)
        tool_response = get_current_weather(
            location=arguments.get('location'),
            unit=arguments.get('unit'),
        )
        tool_info = {"role": "function", "name": tool_name, "content": tool_response}
        print('tool_info=', tool_info)
        messages.append(tool_info)
        print('messages=', messages)
        
        #Step 4, 得到第二次响应
        response = get_response(messages)
        if not response or not response.output:
            print("获取第二次响应失败")
            return None
            
        print('response=', response)
        message = response.output.choices[0].message
        return message
    return message

# 这个地方的description，我先用的英文，你可以动手改成中文试试
functions =[
  {
    "name": "get_current_weather",
    "description": "Get the current weather in a given location.",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  },
  {
    "name": "get_current_time",
    "description": "Get the current time in a given city.",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "City name, e.g. Beijing"
        }
      },
      "required": ["city"]
    }
  }
]

# 入口执行函数，只要有这个，就肯定会执行
# if __name__ == "__main__":
#     result = run_conversation()
#     if result:
#         print("最终结果:", result)
#     else:
#         print("对话执行失败")



query=input('请输入你想查询的天气信息，例如：大连的天气怎样？')
result = run_conversation(query)
if result:
    print("最终结果:", result)
else:
    print("对话执行失败")



"""
functions 参数的格式：

"""