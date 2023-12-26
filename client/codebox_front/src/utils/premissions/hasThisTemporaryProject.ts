import axios from "axios";

import { TempProject } from "@/types";


export default async function(
    vueRouter: any,
    tpid: string
): Promise<TempProject | void> {
    // 方法检查给定的 tpid 的临时项目是否存在
    // 存在则返回临时对象信息 否则直接导航到上一级路由

    const rep = await axios.get(`/api/projects/temporaryproject`, {
        params: {
            tpid
        }
    });

    if (rep.status !== 200 || !rep.data) {
        vueRouter.go(-1);
    }

    return rep.data;
}
