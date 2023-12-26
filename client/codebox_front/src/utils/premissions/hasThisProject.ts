import axios from "axios";

import { Project } from "@/types";


export default async function(
    vueRouter: any,
    pid: string
): Promise<Project | void> {
    // 方法检查给定的 pid 的项目是否存在
    // 存在则返回项目对象信息 否则直接导航到上一级路由

    const rep = await axios.get(`/api/projects/${pid}/`);

    if (rep.status !== 200 || !rep.data || (rep.data.code && rep.data.code !== 200)) {
        console.log("请求项目数据时出错: ", rep);
        vueRouter.go(-1);
    }

    return rep.data;
}
