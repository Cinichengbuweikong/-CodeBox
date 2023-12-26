export default function(
    vuexStore: any,
    vueRouter: any,
    targetProjectUid: string
): void {
    // 检测项目所属用户是否是当前登录用户
    // 是的话不做任何事 不是的话重定向到上一级路由

    if (
        vuexStore.state.userinfo === null
        || vuexStore.state.userinfo.uid !== targetProjectUid
    ) {
        vueRouter.go(-1);
    }
}
