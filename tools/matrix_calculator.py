from langchain_core.tools import tool
import sympy as sp

@tool
def matrix_calculator(matrix:list[list[list[float]]], operation:str):
    """
    对给定的矩阵进行计算。
    
    参数：
        matrix: 一个包括二维列表表示的矩阵的列表，例如 [[[1,2],[3,4]], [[5,6],[7,8]]] 表示两个 2x2 矩阵
        operation: 要执行的操作，例如 "det"（行列式）、"inv"（逆矩阵）、"transpose"（转置矩阵）、 "rank"（秩）、"trace"（迹）、 "eigenvalues"（特征值）、"eigenvectors"（特征向量）、 "add"（矩阵加法）、"subtract"（矩阵减法）、"multiply"（矩阵乘法）
    返回：
        计算结果；输入无效时返回错误信息。
    """
    try:
        if not matrix or not operation:
            return "输入为空，请提供一个矩阵和操作。"
        if not all(isinstance(row, list) for row in matrix):
            return "矩阵格式不正确，请提供一个二维列表。"
        # if not all(isinstance(num, (int, float)) for row in matrix for num in row):
        #     return "矩阵中只能包含数字。"

        unary_operations = {
                "det": lambda A: A.det(),
                "inv": lambda A: A.inv(),
                "transpose": lambda A: A.T,
                "rank": lambda A: A.rank(),
                "trace": lambda A: A.trace(),
                "eigenvalues": lambda A: A.eigenvals(),
                "eigenvectors": lambda A: A.eigenvects()
            }

        binary_operations = {
            "add": lambda A, B: A + B,
            "subtract": lambda A, B: A - B,
            "multiply": lambda A, B: A * B
        }

        if len(matrix) == 1:
            mat = sp.Matrix(matrix[0])
            if operation in unary_operations:
                result = unary_operations[operation](mat)
                return f"操作 {operation} 的结果为：{result}"
            elif operation in binary_operations:
                return "请提供两个矩阵进行二元操作。"
            else:
                return f"不支持的操作：{operation}"
        else:
             if operation in binary_operations:
                mat1 = sp.Matrix(matrix[0])
                mat2 = sp.Matrix(matrix[1])
                result = binary_operations[operation](mat1, mat2)
                return f"操作 {operation} 的结果为：{result}"
    except Exception as e:
        return f"计算过程中发生错误：{str(e)}"
