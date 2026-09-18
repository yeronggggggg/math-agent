from agent import ask_math_question

while True:
    question = input("请输入数学问题（例如 'sin(pi / 2)的值'，'x + y = 5, x - y = 1'，'对 x 求导 x**2 + 3*x + 2'），退出请输入'exit'：")
    if question.lower() == 'exit':
        break
    print(ask_math_question(question))
