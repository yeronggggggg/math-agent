from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
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
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage,AIMessage
from typing import TypedDict, Annotated
import operator
from pydantic import BaseModel,Field

class AgentState(TypedDict):
    messages:Annotated[list[AnyMessage],operator.add]
    plan:list[str]
    verification:dict
    revision_count: int

class MathPlan(BaseModel):
    steps:list[str]=Field(
        description="按照执行顺序排列的数学解题步骤"
    )

class MathVerify(BaseModel):
    passed:bool
    reasons:str

class Agent:

    def __init__(self,model,tools,system="",plan="",revision_count=0):
        self.system =system
        self.plan =plan
        self.revision_count=revision_count
        graph=StateGraph(AgentState)
        graph.add_node("plan",self.make_plan)
        graph.add_node("llm",self.call_openai)
        graph.add_node("action",self.take_action)
        graph.add_node("verify",self.verify_answer)
        graph.add_conditional_edges(
            "llm",
            self.exist_action,
            {True:"action",False:"verify"}
        )
        graph.add_conditional_edges(
            "verify",
            self.exist_change,
            {True:END,False:"llm"}
        )
        graph.add_edge("action","llm")
        graph.add_edge("plan","llm")
        graph.add_edge("verify",END)
        graph.set_entry_point("plan")
        self.graph=graph.compile()
        self.tools={t.name: t for t in tools}
        self.model=model.bind_tools(tools)
        self.planner_model=model.with_structured_output(MathPlan,method="function_calling")#deepseek要求method=
        self.verify_model=model.with_structured_output(MathVerify,method="function_calling")

    def make_plan(self, state:AgentState):
        plans=self.planner_model.invoke([
            SystemMessage(content=self.plan),
            state['messages'][-1]
        ])#state['messages']是HumanMessage的列表，即[HumanMessage()]
        print("生成的计划是：")
        for i, step in enumerate (plans.steps,start=1):
            print(f"{i},{step}")
        return {"plan":plans.steps}

    def call_openai(self,state:AgentState):
        plan_text="\n\n".join(state["plan"])
        systemmessage=SystemMessage(content=self.system.format(content=plan_text))
        messages=[systemmessage]+state["messages"]#临时保存的systemmessage
        message=self.model.invoke(messages)
        # if not message.tool_calls and not any(
        #     isinstance(msg, HumanMessage) and msg.content.startswith("检查反馈为")
        #     for msg in state["messages"]
        #     ):
        #     message = AIMessage(content="x=1 处取得极小值 2。")用于测试
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

    def verify_answer(self,state:AgentState):
        Messages=state["messages"]
        question=next(
            msg.content for msg in reversed(Messages) if isinstance(msg,HumanMessage)
        )
        final_answer=Messages[-1].content

        tool_result="\n".join(
            f"{msg.name}:{msg.content}" for msg in Messages if isinstance (msg,ToolMessage)
        )
        check=self.verify_model.invoke([
            SystemMessage(content=(
            "你是数学答案检查员。请根据原题和工具结果，"
            "检查最终答案的计算、结论以及是否回答了全部要求。"
            "发现错误时说明具体位置；不要重新编造工具结果。"
        )),
            HumanMessage(content=(
                f"原题：\n{question}\n\n"
                f"工具调用结果：\n{tool_result}\n\n"
                f"最终答案:\n{final_answer}\n\n"

            ))
        ])
        result={"verification":check.model_dump()} #model_dump把pydantic转换为python字典
        print(result)
        if not check.passed:
            self.revision_count+=1
            result["messages"]=[HumanMessage(content=f"检查反馈为{check.reasons}。请根据反馈修正答案")]
        return result

    def exist_action(self,state:AgentState):
        result = state["messages"][-1]
        return len(result.tool_calls)>0

    def exist_change(self,state:AgentState):
        if self.revision_count==5:
            print(f"检查未通过，原因是{state["verification"]["reasons"]}")
            return True
        else:
            return state["verification"]["passed"]

