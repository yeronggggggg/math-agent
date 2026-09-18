from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
model = ChatOpenAI(
    model="deepseek-flash",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

from tools import calculator, solve_equation, differentiate, integrate_function, matrix_calculator

tools = [calculator, solve_equation, differentiate, integrate_function, matrix_calculator]
tool_map={tool.name: tool for tool in tools}
max_steps = 10

def ask_math_question(question:str):
    message=[
        SystemMessage(content="你是一个数学专家，擅长使用计算器、方程求解器、求导、求积分和矩阵运算工具。请根据用户的输入选择合适的工具进行计算，并提供详细的解释。"),
        HumanMessage(content=question),
    ]
    model_with_tools = model.bind_tools(tools)
    response = model_with_tools.invoke(message)
    if not response.tool_calls:
        return response.content
    message.append(response)
    while response.tool_calls != [] :
        max_steps -= 1
        if max_steps <= 0:
            return "计算步骤过多，可能存在无限循环，请检查输入。"
        for tool_call in response.tool_calls:
            tool_name = tool_call['name']
            if tool_name in tool_map:
                select_tool = tool_map.get(tool_name)
                tool_message = select_tool.invoke(tool_call)
                message.append(tool_message)
            else:
                tool_message=ToolMessage(
                    content=f"工具 {tool_name} 未找到。"
                    tool_call_id=tool_call["id"]
                    name=tool_name
                )
                return f"工具 {tool_name} 未找到。"
        mid_response = model_with_tools.invoke(message)
        message.append(mid_response)
        response = mid_response

    return response.content
