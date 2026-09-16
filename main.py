import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
model = ChatOpenAI(
    model="deepseek-flash",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)


from tools.calculator import calculate

#result = calculate.invoke({"a": 5, "b": 3, "operation": "+"})
#print(f"The result of adding 5 and 3 is: {result}")

#print("工具名称：", calculate.name)
#print("工具说明：", calculate.description)
#print("参数结构：", calculate.args)

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

from tools.calculator import calculate_adv

# model_with_advtools = model.bind_tools([calculate_adv])
# while True:
#     question = input("请输入计算问题（或输入 'exit' 退出）：")
#     if question.lower() == 'exit':
#         break

#     response = model_with_advtools.invoke(question)
#     if response.tool_calls:
#         tool_message = calculate_adv.invoke(response.tool_calls[0])

#         final_response = model_with_advtools.invoke([
#             ("human", question),
#             response,
#             tool_message
#         ])
#         print(final_response.content)
#     else:
#         print(response.content)


from tools.equation_slover import solve_equation
#question = input("请输入方程(组)（例如 '2*x + 3 = 7' , 'x + y = 10'），退出请输入'exit'：")
# model_with_equation_tools = model.bind_tools([solve_equation])
# response = model_with_equation_tools.invoke("x + y = 5, x - y = 1")
# print("模型响应：", response.content, "工具调用：", response.tool_calls)
# tool_call = response.tool_calls[0]
# tool_message = solve_equation.invoke(tool_call)
# print("工具响应：", tool_message)

# response = solve_equation.invoke({
#     "equations": [
#         "x + y = 5",
#         "x - y = 1"
#     ],
#     "variables": ["x", "y"]
# })
# print("模型响应：", response)
#response = model_with_equation_tools.invoke("hello")
#print("模型响应：", response.content)
#print("工具调用：", response.tool_calls)

#print("计算结果：", result)

# result = solve_equation.invoke({
#     "equations": [
#         "x + y = 1",
#         "x - y = 0",
#         "x + 2*y = 3"
#     ],
#     "variables": ["x", "y"]
# })

# print("工具直接返回：", repr(result))

# result = solve_equation.invoke({
#     "equations": ["x**2 = 1", "x + y = 0"],
#     "variables": ["x", "y"]
# })

# print(repr(result))

while True:
    question = input("请输入方程(组)（例如 '2*x + 3 = 7' , 'x + y = 10'），退出请输入'exit'：")
    if question.lower() == 'exit':
        break
    model_with_equation_tools = model.bind_tools([solve_equation])
    response = model_with_equation_tools.invoke(f"请使用方程求解工具求解：{question}")
    if not response.tool_calls:
        print(response.content)
        continue
    tool_call = response.tool_calls[0]
    tool_message = solve_equation.invoke(tool_call)
    final_response = model_with_equation_tools.invoke([
    ("human", question),
    response,
    tool_message
    ])
    print(final_response.content)