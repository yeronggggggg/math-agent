from langchain_core.tools import tool
import sympy as sp

@tool
def differentiate(expression:str, variable:str):
    """
    对给定的数学表达式进行求导。
    参数：
        expression: 数学表达式字符串，例如 "x**2 + 3*x + 2"
        variable: 对哪个变量求导，例如 "x"
    返回：
        求导结果；输入无效时返回错误信息。
    """
    try:
        if not expression or not variable:
            return "输入为空，请提供一个数学表达式和变量。" 
        var = sp.symbols(variable)
        expr = sp.sympify(expression)
        derivative = sp.simplify(sp.diff(expr, var))
        return f"对 {variable} 求导的结果为：{derivative}"
    except Exception as e:  
        return f"求导错误：{str(e)}"