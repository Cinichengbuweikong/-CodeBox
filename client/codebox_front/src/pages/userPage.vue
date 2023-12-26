<template>
    <div class="userPage">
        <el-container>
            <PageHeader />

            <el-main>
                <el-row class="userInfoBox">
                    <div class="mask"></div>

                    <el-avatar :size="120" :src="`/assets/avatars/${userInfo?.avatarurl}`" />
                    
                    <el-text class="username">{{userInfo?.username}}</el-text>
                    <el-text class="description">{{userInfo?.description}}</el-text>
                    <el-text class="email">{{userInfo?.email}}</el-text>
                </el-row>

                <el-row class="userContentBox">
                    <el-col :span="24">
                        <el-tabs 
                            class="contentTab"
                            v-model="currentTabName"
                        >   
                            <el-tab-pane 
                                label="项目" 
                                name="projects"
                            >
                                <UserProjects :uid="userInfo!.uid" />
                            </el-tab-pane>
                            
                            <el-tab-pane 
                                label="临时项目" 
                                name="tempProjects" 
                                v-if="isOwn"
                            >
                                <UserTempProjects />
                            </el-tab-pane>

                            <el-tab-pane 
                                label="收藏" 
                                name="stars" 
                                v-if="isOwn"
                            >
                                <UserStars />
                            </el-tab-pane>
                            
                            <el-tab-pane 
                                label="设置" 
                                name="settings" 
                                v-if="isOwn"
                            >
                                <Suspense>
                                    <UserSettings />
                                </Suspense>
                            </el-tab-pane>
                        </el-tabs>
                    </el-col>
                </el-row>
            </el-main>

            <PageFooter />
        </el-container>
  </div>
</template>


<script lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

import PageHeader from '@/components/Header/pageHeader.vue';
import PageFooter from '@/components/Footer/pageFooter.vue';
import UserProjects from "@/components/User/userProjects.vue";
import UserTempProjects from "@/components/User/userTempProjects.vue";
import UserStars from "@/components/User/userStars.vue";
import UserSettings from "@/components/User/userSettings.vue";

import { UserInfo } from "@/types";
import axios from "axios";

import eventSub from "@/utils/eventSub";


export default {
    name: "userPage",

    async setup() {
        const route = useRoute();
        
        
        const userInfo = ref<UserInfo | null>(null);
        const currentTabName = ref<string>(getTabName());
        // 当前 tab 页的名字
        const isOwn = ref<boolean>(false);
        // 用户是否在查看自己的主页?


        watch(route, () => {
            // 监视路由变化 当路由变化时切换到指定的标签页显示
            currentTabName.value = getTabName();
        });


        function getTabName(): string {
            // 要显示哪个 tab?  获取要显示的 tab 的名字字符串

            if(
                route.query.tab !== "projects"
                && route.query.tab !== "tempProjects"
                && route.query.tab !== "stars"
                && route.query.tab !== "settings"
            ) {
                return "projects";
            }

            return route.query.tab;
        }

        async function getUserInfo(): Promise<void> {
            // 获取用户信息的函数

            try {
                const rep = await axios.get(`/api/user/`, {
                    params: {
                        uid: route.params.uid
                    }
                });
                
                if (rep.status != 200 || !rep.data || !rep.data.uid) {
                    throw rep;
                }

                const userInfoRep = await axios.get(`/api/user/`);

                if (
                    userInfoRep.status === 200 
                    && userInfoRep.data 
                    && userInfoRep.data.uid 
                    && userInfoRep.data.uid === rep.data.uid
                ) {
                    // 说明当前用户在查看自己的主页
                    isOwn.value = true;
                }

                userInfo.value = rep.data;
            } catch(e) {
                console.log("请求用户信息失败了", e);
            }
        }


        await getUserInfo();


        eventSub.on("userPageUpdateInfo", async () => {
            // 注册事件 更新用户信息
            await getUserInfo();
        });


        return {
            currentTabName,
            userInfo,
            isOwn
        };
    },

    components: {
        PageHeader,
        PageFooter,
        UserProjects,
        UserTempProjects,
        UserStars,
        UserSettings
    },
};
</script>


<style lang="scss" scoped>
.userPage {
    width: 100%;
    height: 100%;

    overflow-y: scroll;

    .el-container {
        flex-direction: column;
        width: 100%;
        height: 100%;

        .el-main {
            padding: 0;
            margin-top: 60px;

            overflow: visible;

            .userInfoBox {
                height: 310px;

                position: relative;

                background-image: url("../assets/imgs/header.jpg");
                background-size: cover;
                background-position: center, center;

                .mask {
                    position: absolute;
                    width: 100%;
                    height: 100%;

                    background-color: rgba($color: #000, $alpha: 0.2);
                }

                .el-avatar {
                    position: absolute;
                    left: 10%;
                    top: 170px;
                }

                .el-text {
                    position: absolute;
                }

                .username {
                    left: 10%;
                    top: 110px;

                    font-size: 44px;
                    font-weight: bold;
                }

                .description {
                    left: calc(116px + 12%);
                    top: 185px;

                    font-size: 16px;
                }

                .email {
                    left: calc(116px + 12%);
                    top: 160px;
                    font-size: 16px;
                }
            }

            .userContentBox {
                .el-col {
                    height: 100%;

                    .contentTab {
                        --el-text-color-primary: #{ $fontColor };

                        :deep(.el-tabs__header) {
                            margin-bottom: 0;
                            width: 80%;
                            margin: auto;
                        }
                    }
                }
            }
        }
    }
}
</style>
