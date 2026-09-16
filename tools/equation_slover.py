import sympy as sp
from langchain_core.tools import tool
import ast

ALLOWED_NODE_TYPES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,
    ast.Name,
    ast.Load,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.UAdd,
    ast.USub,
)


def validate_expression(expression: str, allowed_variables: set[str]):
    tree = ast.parse(expression, mode="eval")

    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODE_TYPES):
            raise ValueError(
                f"表达式包含不允许的内容：{type(node).__name__}"
            )

        if isinstance(node, ast.Name):
            if node.id not in allowed_variables:
                raise ValueError(f"未声明的变量：{node.id}")

        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise ValueError("表达式中只允许数字常量")


@tool
def solve_equation(equations:list[str], variables:list[str]):
    """
    求解多元多次方程。
    
    参数：
        equation: 方程(组)字符串的列表，例如 ["2*x + 3 = 7", "x + y = 10"]
        variable: 方程(组)中的未知数，例如 ["x", "y"]
    
    返回：
        方程(组)的解；输入无效时返回错误信息。

    示例：
    >>> solve_equation(["2*x + 3 = 7","x + y = 10"], ["x","y"])
    """
    try:
        if equations==[] or variables==[]:
            return f"格式不正确，请重新输入"
        if len(variables) != len(set(variables)):
            return f"变量名不能重复。"
        variables_map={var: sp.symbols(var) for var in variables}
        #exprs= [sp.Eq(sp.sympify(eq.split('=')[0],locals=variables_map) - sp.sympify(eq.split('=')[1],locals=variables_map)) for eq in equations]
        allowed_variables = set(variables)
        exprs = []
        for eq in equations:
            if eq.count("=") != 1:
                return f"方程格式错误：{eq}。每个方程必须包含一个等号。"
            left_side, right_side = eq.split("=", 1)
            left_side = left_side.strip()
            right_side = right_side.strip()
            validate_expression(left_side, allowed_variables)
            validate_expression(right_side, allowed_variables)
            left_expr = sp.sympify(left_side, locals=variables_map)
            right_expr = sp.sympify(right_side, locals=variables_map)
            exprs.append(left_expr - right_expr)
        symbols = list(variables_map.values())
        solution = sp.nonlinsolve(exprs, symbols)

        if solution == sp.EmptySet:
            return "方程组无解。"

        return solution
        # solution = sp.solve(exprs, *variables_map.values(),dict=True)
        # if solution==[]:
        #     return "方程(组)无解。"
        # return solution
    except Exception as e:
        return f"求解错误：{str(e)}"