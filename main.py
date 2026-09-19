from agent import Agent
from tools import calculator, solve_equation, differentiate, integrate_function, matrix_calculator
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
# model = ChatOpenAI(
#     model="deepseek-flash",
#     base_url="https://api.deepseek.com",
#     api_key=os.getenv("DEEPSEEK_API_KEY")
# )

model = ChatOpenAI(
    model="deepseek-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
    extra_body={
        "thinking": {
            "type": "disabled"
        }
    }
)


prompt=""""你是一个非常聪明的数学助手，使用工具来解决数学问题。\
你可以进行多次调用\
只能在确定工具的时候进行使用\
请根据用户的输入选择合适的工具进行计算，并提供详细的解释。
"""
tools = [calculator, solve_equation, differentiate, integrate_function, matrix_calculator]
#tools={tool.name: tool for tool in cal_tools}
abot=Agent(model,tools,system=prompt)

# while True:
#     question = input("请输入数学问题（例如 'sin(pi / 2)的值'，'x + y = 5, x - y = 1'，'对 x 求导 x**2 + 3*x + 2'），退出请输入'exit'：")
#     if question.lower() == 'exit':
#         break
#     print(ask_math_question(question))

# from IPython.display import Image
# image=Image(abot.graph.get_graph().draw_png())

# from PIL import Image
# from io import BytesIO
# png_data = abot.graph.get_graph().draw_mermaid_png()
# Image.open(BytesIO(png_data)).show()

while True:
    question=input(f"请输入数学问题，退出请输入'exit'： ")
    if question.lower() == 'exit':
        break
    messages = [HumanMessage(content=question)]
    result = abot.graph.invoke({"messages": messages},config={"recursion_limit":20})
    #print(f"最终回答 \n {result['messages'][-1].content}")

    for event in abot.graph.stream({"messages": messages},config={"recursion_limit":20}, stream_mode="updates"):
        node_name = next(iter(event))
        print("经过节点：", node_name)
        #print(event)
