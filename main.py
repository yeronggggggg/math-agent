from tools.calculator import calculate
from tools.calculator import calculate_adv
#result = calculate.invoke({"a": 5, "b": 3, "operation": "+"})
#print(f"The result of adding 5 and 3 is: {result}")

#print("工具名称：", calculate.name)
#print("工具说明：", calculate.description)
#print("参数结构：", calculate.args)

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
model = ChatOpenAI(
    model="deepseek-flash",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

#response = model.invoke("你好，请只回复：连接成功")
#print(response.content)


#model_with_tools = model.bind_tools([calculate])
#response = model_with_tools.invoke("你好")
#print(response.tool_calls)

#tool_call = response.tool_calls[0]
#result = calculate.invoke(tool_call["args"])
#print("计算结果：", result)

#question = input("请输入计算问题：")
#response = model_with_tools.invoke(question)
#tool_message = calculate.invoke(response.tool_calls[0])
#final_response = model_with_tools.invoke([
#    ("human", question),
#    response,
#    tool_message
#])
#print(final_response.content)


# model_with_tools = model.bind_tools([calculate])
# while True:
#     question = input("请输入计算问题（或输入 'exit' 退出）：")
#     if question.lower() == 'exit':
#         break

#     response = model_with_tools.invoke(question)
#     if response.tool_calls:
#         tool_message = calculate.invoke(response.tool_calls[0])

#         final_response = model_with_tools.invoke([
#             ("human", question),
#             response,
#             tool_message
#         ])

#         print(final_response.content)
#     else:
#         print(response.content)


model_with_advtools = model.bind_tools([calculate_adv])
while True:
    question = input("请输入计算问题（或输入 'exit' 退出）：")
    if question.lower() == 'exit':
        break

    response = model_with_advtools.invoke(question)
    if response.tool_calls:
        tool_message = calculate_adv.invoke(response.tool_calls[0])

        final_response = model_with_advtools.invoke([
            ("human", question),
            response,
            tool_message
        ])

        print(final_response.content)
    else:
        print(response.content)