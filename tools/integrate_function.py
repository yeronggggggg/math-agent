from langchain_core.tools import tool
import sympy as sp

@tool
def integrate_function(expression:str, variable:str, lower_limit:str | None=None, upper_limit:str | None=None):
    """
    对给定的数学表达式进行积分。
    
    参数：
        expression: 数学表达式字符串，例如 "x**2 + 3*x + 2"
        variable: 对哪个变量积分，例如 "x"
        lower_limit: 积分下限（可选）
        upper_limit: 积分上限（可选）
    返回：
        积分结果；输入无效时返回错误信息。
    """
    try:
        if not expression or not variable:
            return "输入为空，请提供一个数学表达式和变量。"
        var = sp.symbols(variable)
        expr = sp.sympify(expression)
        if lower_limit is not None and upper_limit is not None:
            lower = sp.sympify(lower_limit)
            upper = sp.sympify(upper_limit)
            integral = sp.integrate(expr, (var, lower, upper))
            return f"定积分结果为：{integral}"
        elif lower_limit is None and upper_limit is None:
            integral = sp.integrate(expr, var)
            return f"不定积分结果为：{integral}"
        else:
            return "请提供完整的积分上下限，或者都不提供。"
    except Exception as e:
        return f"积分错误：{str(e)}"