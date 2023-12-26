<template>
    <div class="projectPage">
        <el-container>
            <el-main>
                <suspense>
                    <TempRepl />
                </suspense>

                <el-row class="infoBox">
                    <div class="title">
                        <el-text>{{ projectInfo ? projectInfo.name : "Title" }}</el-text>
                    </div>
                    
                    <div class="info">
                        <el-avatar 
                            :size="50" 
                            :src="`/assets/avatars/${projectOwnerInfo? projectOwnerInfo.avatarurl : 'default.jpg'}`"
                            @click="routeToUserPage"
                        />

                        <div>
                            <el-text class="username">{{ projectOwnerInfo ? projectOwnerInfo.username : "username" }}</el-text>
                            <el-text class="description">临时项目</el-text>
                        </div>
                    </div>
                </el-row>

                <el-row class="actionBox">
                    <div
                        @click="routerToProjectSettingsPage"
                    >
                        <i class="iconfont icon-modify"></i>
                        <el-text>修改此项目</el-text>
                    </div>

                    <div
                        @click="eventSub.emit('saveChanges')"
                    >
                        <i class="iconfont icon-baocun"></i>
                        <el-text>保存修改</el-text>
                    </div>
                </el-row>
            </el-main>
            
            <PageFooter />
        </el-container>
    </div>
</template>


<script setup lang="ts">
import {
    defineOptions,
    ref,
    onMounted,
    onBeforeMount,
} from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import TempRepl from "@/components/Repl/tempRepl.vue";

import PageFooter from "@/components/Footer/pageFooter.vue";
import { UserInfo } from "@/types";
import eventSub from "@/utils/eventSub";
import { TempProject } from "@/types";
import hasUserLogin from "@/utils/premissions/hasUserLogin";
import hasThisTemporaryProject from "@/utils/premissions/hasThisTemporaryProject";
import hasUserOwnProject from "@/utils/premissions/hasUserOwnProject";


defineOptions({
    name: "projectPage"
});

const route = useRoute();
const router = useRouter();
const store = useStore();


const projectInfo = ref<TempProject | null>(null);
// 当前项目信息

const projectOwnerInfo = ref<UserInfo | null>(null);
// 当前项目拥有者的信息


(async function() {
    // 鉴权函数  检查以下权限:
    // 用户是否已登录
    // 此临时项目是否存在
    // 用户是否拥有此临时项目

    const userinfo = await hasUserLogin(router);
    projectOwnerInfo.value = (userinfo as UserInfo);

    const pInfo = await hasThisTemporaryProject(router, (route.params.tpid as string));
    projectInfo.value = (pInfo as TempProject);

    hasUserOwnProject(store, router, `${projectInfo.value.uid}`);
})();


function routerToProjectSettingsPage(): void {
    // 当 "修改此项目按钮" 点击时 跳转到项目设置页
    router.push({
        path: `/projects/temp/${route.params.tpid}/settings`
    });
}

function routeToUserPage() {
    // 当用户点击头像后 我们需要重定向至用户信息页

    router.push(`/user/${projectOwnerInfo.value?.uid}`);
}


onBeforeMount(() => {
    console.clear = () => {};
});

onMounted(async () => {
    try{
        // 从网络获取数据 判断当前项目是否是用户自己的

        // 获取项目信息
        const rep = await axios.get(`/api/projects/temporaryproject`, {
            params: {
                tpid: route.params.tpid,
            }
        });

        if (rep.status !== 200 || !rep.data) {
            throw rep;
        }

        projectInfo.value = rep.data;
        
        
        // 获取项目所有者信息
        const projOwnerRep = await axios.get("/api/user/", {
            params: {
                uid: projectInfo.value!.uid
            }
        });

        if (projOwnerRep.status !== 200 || !projOwnerRep.data) {
            throw projOwnerRep;
        }

        projectOwnerInfo.value = projOwnerRep.data;
    } catch(e) {
        console.log("获取项目信息失败: ", e);
    }
});
</script>


<style scoped lang="scss">
.projectPage {
    width: 100%;
    height: 100%;

    .el-container {
        width: 100%;
        height: 100%;

        flex-direction: column;

        overflow-y: scroll;

        .el-main {
            overflow: visible;
            padding: 0;

            background-color: $backgroundDarkenColor;

            .infoBox {
                width: 70%;

                margin: 0 auto;

                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                align-items: center;

                padding: 30px 0;

                div {
                    width: 100%;
                }

                .title {
                    height: 30%;

                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: flex-start;

                    .el-text {
                        font-size: 22px;
                        font-weight: bold;
                        align-self: flex-start;
                    }
                }

                .info {
                    height: 70%;

                    display: flex;
                    flex-direction: row;
                    justify-content: flex-start;
                    align-items: flex-start;

                    padding-top: 10px;

                    box-sizing: border-box;

                    .el-avatar {
                        min-width: 50px;
                        margin-right: 20px;
                        cursor: pointer;
                    }

                    .el-text {
                        align-self: flex-start;
                    }

                    div {
                        height: 100%;
                        
                        display: flex;
                        flex-direction: column;
                        justify-content: flex-start;
                        align-items: flex-start;

                        .description {
                            padding-top: 5px;
                        }
                    }
                }
            }

            .actionBox {
                width: 70%;
                height: 60px;

                margin: 0 auto;

                display: flex;
                flex-direction: row;
                justify-content: flex-start;
                align-items: center;

                margin-bottom: 30px;

                div {
                    height: 100%;

                    margin-right: 40px;

                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;

                    cursor: pointer;

                    .el-text {
                        margin-top: 5px;
                        font-size: 16px;
                    }

                    i {
                        font-size: 22px;
                        color: $fontColor;
                    }
                }
            }
        }
    }
}
</style>
