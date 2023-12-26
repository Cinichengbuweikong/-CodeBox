import os
import shutil

from constants import ProjectType, PROJECT_BASE_DIR, TEMP_PROJECT_BASE_DIR


def removeProject(name: str, type: ProjectType) -> None:
    """
    删除指定类别和名字的项目
    本函数有可能抛出异常
    该函数是同步函数 需要放在 eventloop.run_in_executor 中运行
    """

    if type == ProjectType.NORMAL:
        floderPath = os.path.join(PROJECT_BASE_DIR, name)
    
    elif type == ProjectType.TEMP:
        floderPath = os.path.join(TEMP_PROJECT_BASE_DIR, name)
    
    else:
        raise Exception(f"not found floder: {name} in {type}")

    print(floderPath)
    
    if os.path.exists(floderPath):
        shutil.rmtree(floderPath)
