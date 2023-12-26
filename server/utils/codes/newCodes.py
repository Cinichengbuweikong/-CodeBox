import uuid
import os

from constants import CodesType, VUE_DEFAULT_TEMPLATE


def newCodeFile(path: str, filetype: CodesType) -> str:
    """
    新建一个指定类型的代码文件
    方法返回新建的代码文件的名字(不带后缀名)
    path: str  要在哪个文件夹下新建文件
    filetype: CodesType  要新建的文件的类型
    本函数是同步函数 需要在 aysncio 的 run_in_executor 中运行
    本函数可能抛出异常
    """

    fileName: str = uuid.uuid1().hex
    newFileContent = ""

    if filetype == CodesType.VUE:
        targetFileName = f"{fileName}.vue"
        newFileContent = VUE_DEFAULT_TEMPLATE
    elif filetype == CodesType.JS:
        targetFileName = f"{fileName}.js"
    else:
        raise Exception(f"unknow filetype: {filetype}")
    

    try:
        with open(os.path.join(path, targetFileName), "a") as file:
            file.write(newFileContent)
    except Exception as e:
        raise e
    
    return fileName
