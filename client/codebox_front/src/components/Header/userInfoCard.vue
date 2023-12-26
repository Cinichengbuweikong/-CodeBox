<template>
    <div class="userInfoCard">
        <el-row class="userInfoBox">
            <el-col :span="24">
                <el-text class="userName">{{ store.state.userinfo?.username || "匿名用户" }}</el-text>
                <el-text class="userCoin">硬币数: {{ store.state.userinfo?.coin || 0 }}</el-text>
            </el-col>
        </el-row>

        <el-row class="userActionBox">
            <el-col
                v-if="store.state.userinfo != null"
            >
                <el-link :underline="false" @click="routeToTab('projects')">
                    我的项目
                </el-link>

                <el-link :underline="false" @click="routeToTab('tempProjects')">
                    我的临时项目
                </el-link>

                <el-link :underline="false" @click="routeToTab('stars')">
                    我的收藏
                </el-link>

                <el-link
                    :underline="false"
                    @click="logout"
                >
                    退出登录
                </el-link>
            </el-col>

            <el-col
                v-else
            >
                <el-link 
                    :underline="false"
                    @click="props.showDialog"
                >
                    登录/注册
                </el-link>
            </el-col>
        </el-row>
    </div>
</template>


<script lang="ts" setup>
import { defineOptions, defineProps } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import axios from "axios";


defineOptions({
    name: "userInfoCard"
});

const props = defineProps({
    showDialog: {
        type: Function,
        required: true
    }
});

const store = useStore();
const router = useRouter();


async function logout(): Promise<void> {
    // 退出登录的函数

    try {
        // 退出登录
        const rep = await axios.post("/api/logout");

        if (rep.status !== 200) {
            throw rep;
        }

        // 重新获取用户信息
        store.commit("REMOVE_USER_INFO");

        // 重定向到首页
        router.replace("/");
    } catch(e) {
        console.log("请求出错: ", e);
    }
}

function routeToTab(tabName: string) {
    // 将路由导航到用户信息页中指定名字的 tab 中

    const uid: number | null = store.state.userinfo?.uid;

    if (uid === undefined) {
        return ;
    }

    router.push(`/user/${uid}?tab=${tabName}`);
}
</script>


<style lang="scss" scoped>
.userInfoCard {
    overflow: hidden;
    transition: all 0.3s ease;

    background-color: $backgroundColor;
    box-shadow: 0px 2px 30px 1px $backgroundDarkenColor;

    .userInfoBox {
        height: 50%;

        .el-col {
            width: 100%;
            height: 100%;

            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;

            .userName {
                margin-bottom: 10px;
                font-size: 18px;
                font-weight: bold;
            }

            .userCoin {
                margin-bottom: 10px;
            }
        }
    }

    .userActionBox {
        height: 50%;

        .el-col {
            width: 100%;
            height: 100%;

            display: flex;
            flex-direction: row;
            justify-content: space-evenly;
            align-items: flex-start;
            flex-wrap: wrap;

            padding-top: 10px;

            container-type: inline-size;

            .el-link {
                font-size: 5cqw;
                padding: 3px 4px;
                border-radius: 3px;

                transition: background-color 0.1s ease;

                &:hover {
                    color: rgb(220, 220, 220);
                    background-color: rgba($color: $actionColor, $alpha: 0.7);
                }
            }
        }
    }
}
</style>
