import getUserInfo from "../getUserInfo";

import { UserInfo } from "@/types";


export default async function(
    vueRouter: any
): Promise<UserInfo | void> {
    // 方法检查用户是否已登录
    // 登录则返回用户登录信息 否则直接导航到上一级路由

    const userInfo = await getUserInfo();

    if (userInfo == null) {
        vueRouter.go(-1);
    }

    return (userInfo as UserInfo);
}
