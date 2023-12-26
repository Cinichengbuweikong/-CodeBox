def readCodeFile(path: str) -> str:
    """
    读取代码文件内容 并返回读取到的代码文件内容
    path: str  要被读取的代码文件的路径
    方法需要放在 run_in_executor 中运行
    方法可能抛出异常
    """

    try:
        with open(path, "r") as file:
            content = file.read()
            
            return content
    except Exception as e:
        raise e
