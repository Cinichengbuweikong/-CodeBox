import os

from constants import CodesType


def deleteCodeFile(path: str) -> None:
    """
    删除指定类型的代码文件
    path: str  要被删除的文件的路径 带有后缀名
    本函数是同步函数 需要在 aysncio 的 run_in_executor 中运行
    本函数有可能抛出异常
    """

    if not os.path.exists(path):
        raise Exception("path not exits")

    try:
        os.remove(path)
    except Exception as e:
        raise e
    
    return 

