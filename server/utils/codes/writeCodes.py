def writeCodeFile(path: str, content: str) -> None:
    """
    写入代码文件内容 方法清空原有文件中的内容并重新写入新内容
    path: str  要被写入的代码文件的路径
    content: str  要被写入的内容
    方法需要放在 run_in_executor 中运行
    方法可能抛出异常
    """

    try:
        with open(path, "a") as file:
            file.seek(0)
            file.truncate()
            file.write(content)
        
    except Exception as e:
        raise e
