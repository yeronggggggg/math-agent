from langchain_core.tools import tool
import sympy as sp
from typing import Optional

@tool
def limit_calculator(expression:str,variable:str,point:str,direction:str,assumptions: Optional[dict[str, str]] = None):
    """
    对给定的函数表达式、变量求极限。

    参数：
        expression:函数表达式，如:"x**2+2x",
        variable:函数变量，如"x",
        point:趋近点，如"0","+oo","-oo",
        direction:趋近方向，"+-"表示双侧，"+"表示右侧，"-"表示左侧。
        assumptions:其他参数的假设，例如 {"x": "positive"}
    
    返回：
        求极限结果或返回错误信息
    """

    allowed_assumptions=[ "positive",
        "negative",
        "nonnegative",
        "nonpositive",
        "nonzero",
        "real",
        "integer"]
    
    try:
        symbols_map={}
        for name, assumption in (assumptions or {}).items():
            if assumption not in allowed_assumptions:
                return f"不支持的符号假设：{assumption}"
            symbols_map[name] = sp.Symbol(
                name,
                **{assumption: True},
            )
        if variable not in symbols_map:
            symbols_map[variable] = sp.Symbol(variable)

        var = symbols_map[variable]

        expr = sp.sympify(
            expression,
            locals=symbols_map,
        )
        if point == "oo":
            limit_point = sp.oo
        elif point == "-oo":
            limit_point = -sp.oo
        else:
            limit_point = sp.sympify(point,locals=symbols_map)
        result = sp.limit(
            expr,
            var,
            limit_point,
            dir=direction
        )
        return result

    except Exception as e:
        return f"求极限失败：{e}" 