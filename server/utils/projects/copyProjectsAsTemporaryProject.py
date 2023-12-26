import os
import shutil
import uuid

from constants import PROJECT_BASE_DIR, TEMP_PROJECT_BASE_DIR


def copyProjectsAsTemporaryProject(name: str) -> str:
    """
    将指定的工程文件夹复制为临时工程
    方法返回被复制为的临时工程的文件夹名
    src: str  源工程文件夹名
    方法需要在 run_in_executor 中运行
    方法可能抛出异常
    """

    srcProjectPath = os.path.join(PROJECT_BASE_DIR, name)

    if not os.path.exists(srcProjectPath):
        raise Exception("src path doesn't exist")
    
    newTemporaryProjectName = uuid.uuid1().hex
    
    try:
        shutil.copytree(
            srcProjectPath,
            os.path.join(TEMP_PROJECT_BASE_DIR, newTemporaryProjectName)
        )
    except Exception as e:
        raise e
    
    return newTemporaryProjectName
