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
        app_result = sp.N(acc_result)
        return f"精确结果为 {acc_result}，近似结果为 {app_result}"
    except Exception as e:
        return f"计算错误：{str(e)}"



import ast
import operator

def _evaluate_node_(node):
    if isinstance(node, ast.BinOp):
        left = _evaluate_node_(node.left)
        right = _evaluate_node_(node.right)
        op_type = type(node.op)

        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod
        }

        if op_type in ops:
            return ops[op_type](left, right)
        else:
            raise ValueError(f"不支持的运算符：{op_type}")

    elif isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"不支持的常量类型：{type(node.value)}")
    elif isinstance(node, ast.Expression):
        return _evaluate_node_(node.body)
    else:
        raise ValueError(f"不支持的表达式类型：{type(node)}")

@tool
def calculate_adv(expression:str):
    """
    对一个数学表达式进行计算。

    参数：
        expression: 数学表达式字符串，例如 "3 + 5 * (2 - 8)"

    返回：
        计算结果；输入无效时返回错误信息。
    """
    try:
        tree=ast.parse(expression, mode='eval')
        result = _evaluate_node_(tree)
        return result
    except Exception as e:
        return f"计算错误：{str(e)}"