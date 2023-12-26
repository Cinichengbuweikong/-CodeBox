import uuid
import os
from typing import Tuple

from constants import PROJECT_BASE_DIR, TEMP_PROJECT_BASE_DIR, ProjectType, CodesType
from utils.codes.newCodes import newCodeFile


def createProject(projectType: ProjectType) -> Tuple[str, str]:
    """
    创建一个指定类型的项目 创建成功后方法返回创建好的项目文件夹的名字(一个唯一值)和 App.vue 的文件名
    本函数有可能抛出异常
    该函数是同步函数 需要放在 eventloop.run_in_executor 中运行
    """

    floderName: str = uuid.uuid1().hex

    # 要新建的项目的文件夹位置
    if projectType == ProjectType.NORMAL:
        floderPath: str = os.path.join(PROJECT_BASE_DIR, floderName)
    elif projectType == ProjectType.TEMP:
        floderPath: str = os.path.join(TEMP_PROJECT_BASE_DIR, floderName)

    try:
        # 创建项目文件夹
        os.mkdir(floderPath)
    except Exception as e:
        raise e

    try:
        # 新建 App.vue 并写入内容
        appFileName = newCodeFile(floderPath, CodesType.VUE)

    except Exception as e:
        raise e
    
    return (floderName, appFileName)
