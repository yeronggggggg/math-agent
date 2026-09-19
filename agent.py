from langchain_core.messages import SystemMessage, ToolMessage
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
model_with_tools = model.bind_tools(tools)

# def ask_math_question(question:str):
#     max_steps = 10
#     message=[
#         SystemMessage(content="你是一个数学专家，擅长使用计算器、方程求解器、求导、求积分和矩阵运算工具。请根据用户的输入选择合适的工具进行计算，并提供详细的解释。"),
#         HumanMessage(content=question),
#     ]
#     response = model_with_tools.invoke(message)
#     if not response.tool_calls:
#         return response.content
#     message.append(response)
#     while response.tool_calls != [] :
#         max_steps -= 1
#         last_error=None
#         if max_steps <= 0:
#             if last_error is not None:
#                 return last_error
#             else:
#                 return "调用次数过多，可能存在无限循环情况，请重新输入。"
#         for tool_call in response.tool_calls:
#             tool_name = tool_call['name']
#             if tool_name in tool_map:
#                 try:
#                     select_tool = tool_map.get(tool_name)
#                     tool_message = select_tool.invoke(tool_call)
                    
#                 except Exception as e:
#                     tool_message=ToolMessage(
#                     content=f"工具 {tool_name} 执行失败:{e}",
#                     tool_call_id=tool_call["id"],
#                     name=tool_name
#                 )
#                     last_error=(f"工具 {tool_name} 执行失败:{e}")
            
#             else:
#                 tool_message=ToolMessage(
#                     content=f"工具 {tool_name} 未找到。",
#                     tool_call_id=tool_call["id"],
#                     name=tool_name
#                 )
#                 last_error=(f"工具 {tool_name} 未找到。")
#             message.append(tool_message)
#         mid_response = model_with_tools.invoke(message)
#         message.append(mid_response)
#         response = mid_response

#     return response.content



from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class Agent:

    def __init__(self,model,tools,system=""):
        self.system =system
        graph=StateGraph(AgentState)
        graph.add_node("llm",self.call_openai)
        graph.add_node("action",self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exist_action,
            {True:"action",False:END}
        )
        graph.add_edge("action","llm")
        graph.set_entry_point("llm")
        self.graph=graph.compile()
        self.tools={t.name: t for t in tools}
        self.model=model.bind_tools(tools)

    def call_openai(self,state:AgentState):
        messages=state["messages"]
        if self.system:
            messages=[SystemMessage(content=self.system)]+messages
        message=self.model.invoke(messages)
        return{'messages':[message]}

    def take_action(self,state:AgentState):
        tool_calls=state["messages"][-1].tool_calls
        results=[]
        for t in tool_calls:
            print(f"Calling:{t}")
            if not t['name'] in self.tools:
                print("工具不存在")
                result="工具不存在"
            else:
                result=self.tools[t["name"]].invoke(t["args"])
            results.append (ToolMessage(tool_call_id=t["id"],name=t["name"],content=str(result)))
        print("返回模型")
        return {'messages':results}

    def exist_action(self,state:AgentState):
        result = state["messages"][-1]
        return len(result.tool_calls)>0

