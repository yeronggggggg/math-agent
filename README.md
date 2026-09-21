# Math Agent

A tool-using AI agent for solving and verifying mathematical problems.


## 测试结果

已完成 6 道示例题测试，最终答案均正确，涵盖方程求解、求导、计算、积分、矩阵求逆和除零输入。

测试中发现计算器会把 `7/0` 返回为 `zoo`；修复后，直接调用计算器工具会返回“表达式未定义”的错误信息。详细记录见 `tests/evaluation.md`。