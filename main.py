from agent import Agent
from tools import __all__
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import sys#读取启动程序时写在命令后面的内容

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

PLAN_PROMPT="""
你是一名数学解题规划器。\
请把用户的数学问题拆分成有顺序、可执行的步骤。\
每个步骤作为 steps 列表中的一个字符串。\
这里只制定计划，不要给出最终答案。

"""
SYSTEM_PROMPT=""""你是一个非常聪明的数学助手，使用工具来解决数学问题。\
你可以进行多次调用。\
只能在确定工具的时候进行使用。\
请根据给出的解题计划{content}选择合适的工具进行计算，给出答案。\
工具执行完成后，最终回答必须使用统一格式：\
结果：<最终结果>\
说明：<最多两句话的必要说明>\
"""


tools = __all__
#tools={tool.name: tool for tool in cal_tools}
abot=Agent(model,tools,system=SYSTEM_PROMPT,plan=PLAN_PROMPT)

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

# test_state = {
#     "messages": [
#         HumanMessage(content="求 f(x)=x**3-3*x 的极值"),
#         AIMessage(content="x=1 处取得极小值 2。")
#     ]
# }

# check_result = abot.verify_answer(test_state)
# print(check_result)

def solve_question(question:str):
    messages = [HumanMessage(content=question)]
    result = abot.graph.invoke({"messages": messages,"revision_count":0},config={"recursion_limit":50})#整张图运行步数上限
    #result["verification"] = {"passed": False, "reasons": "测试失败提示"}
    if result["verification"]["passed"]:
        return f"检查通过\n最终回答：\n{result['messages'][-1].content}"
    return f"检查未通过：{result['verification']['reasons']}\n本次没有已验证的答案。"



while True:
    if len(sys.argv)>1:#sys.argv[0] 是脚本名，sys.argv[1] 是传入的题目。
        question = " ".join(sys.argv[1:])
    else:
        question=input(f"请输入数学问题，退出请输入'exit'： ")
    if question.lower() == 'exit':
        break
    print(solve_question(question))

    if len(sys.argv) > 1:
        break
    

    # for event in abot.graph.stream({"messages": messages},config={"recursion_limit":50}, stream_mode="updates"):
    #     node_name = next(iter(event))
    #     print("经过节点：", node_name)
        # print(event)
