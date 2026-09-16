from langchain_core.tools import tool
@tool
def calculate(a, b, operation):
    """
    对两个数字进行四则运算。

    参数：
        a: 第一个数字
        b: 第二个数字
        operation: 运算符，支持 +、-、*、/

    返回：
        计算结果；输入无效时返回错误信息。
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return "输入的数字无效，请输入有效的数字。"

    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        if b == 0:
            return "除数不能为零。"
        return a / b
    else:
        return "无效的运算符，请输入 +、-、* 或 /。"


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