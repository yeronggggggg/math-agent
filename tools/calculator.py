from langchain_core.tools import tool
import sympy as sp

@tool
def calculator(expression:str):
    """
    进行数学运算

    参数：
        expression: 数学表达式字符串，例如 "3 + 5 * (2 - 8)"

    返回：
        计算结果；输入无效时返回错误信息。
    """
    try:
        if not expression:
            return "输入为空，请提供一个数学表达式。"
        acc_result = sp.sympify(expression)
        if acc_result in (sp.zoo, sp.nan):
            return "计算错误：表达式未定义，可能存在除以零。"
        app_result = sp.N(acc_result)
        return f"精确结果为 {acc_result}，近似结果为 {app_result}"
    except Exception as e:
        return f"计算错误：{str(e)}"

