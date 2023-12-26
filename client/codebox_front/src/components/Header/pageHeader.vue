<template>
    <el-header>
        <el-row>
            <el-col class="logoBox" :span="4" :offset="1" @click="routerToIndexPage">
                <el-image :src="require('@/assets/imgs/largeicon.png')"/>
                <!-- <el-text>代码盒子</el-text> -->
            </el-col>
            
            <el-col class="searchBox" :span="10" :offset="1">
                <input
                    class="searchInput"
                    v-model="searchQuery"
                    placeholder="搜索你想要的内容..."
                    @keydown.enter="searchProjects"
                />
            </el-col>
            
            <el-col class="userInfoBox" :span="8">
                <el-row>
                    <el-col class="avatarBox" :span="4">
                        <div>
                            <userInfoCard
                                :showDialog="showDialog"
                            />
                            <el-avatar 
                                class="avatar" 
                                :size="45"
                                :src="`/assets/avatars/${ store.state.userinfo ? store.state.userinfo.avatarurl : 'default.jpg' }`"
                                @click="showUserInfo"
                            />
                        </div>
                    </el-col>
                </el-row>
            </el-col>
        </el-row>

        <LoginOrSignupDialog
            :show="showLoginOrSignupDialog"
            :closeDialog="closeDialog"
        />
    </el-header>
</template>


<script lang="ts" setup>
import { ref, defineOptions, } from 'vue';
import { useStore } from "vuex";
import { useRouter } from 'vue-router';

import userInfoCard from './userInfoCard.vue';
import LoginOrSignupDialog from "../Dialog/loginOrSignupDialog.vue";


defineOptions({
    name: "pageHeaderComponent"
});

const store = useStore();
const router = useRouter();

const searchQuery = ref<string>("");
// 用户输入的关键字

const showLoginOrSignupDialog = ref<boolean>(false);
// 是否显示 "登录或注册对话框"

function searchProjects(): void {
    // 跳转到搜索项目 url 上
    router.push({
        path: "/search",
        query: {
            q: searchQuery.value
        }
    });
}

function showUserInfo(): void {
    // 跳转到用户详情页上

    const uid: number | null = store.state.userinfo?.uid;

    if (uid === undefined) {
        return ;
    }

    router.push({
        path: `/user/${uid}`,
    });
}

function showDialog(): void {
    // 设置显示 "登录或注册对话框"
    showLoginOrSignupDialog.value = true;
}

function closeDialog(): void {
    // 设置隐藏 "登录或注册对话框"
    showLoginOrSignupDialog.value = false;
}

function routerToIndexPage(): void {
    // 导航到首页
    router.push("/");
}
</script>


<style lang="scss" scoped>
.el-header {
    width: 100%;
    
    padding-left: 0;
    padding-right: 0;
    
    position: fixed;
    left: 0;
    top: 0;
    
    background-color: $backgroundColor;
    box-shadow: 0 1px 5px 1px $backgroundDarkenColor;
    
    z-index: 2000;

    .el-row {
        height: 100%;

        .logoBox {
            display: flex;
            flex-direction: row;
            justify-content: flex-start;
            align-items: center;

            cursor: pointer;

            .el-image {
                margin: 0 10px;
                width: 110px;
            }
        }

        .searchBox {
            display: flex;
            justify-content: center;
            align-items: center;

            .searchInput {
                width: 100%;
                height: 40px;
                font-size: 16px;
                outline: 0;
                border: 0;

                border-radius: 3px;

                padding-left: 6px;

                &::placeholder {
                    color: #6B6B6B;
                }
            }
        }

        .userInfoBox {
            .el-row {
                width: 100%;
                height: 100%;

                .avatarBox {
                    & > div {
                        width: 100%;
                        height: 100%;

                        cursor: pointer;

                        display: flex;
                        justify-content: center;
                        align-items: center;

                        position: relative;

                        .avatar {
                            box-shadow: none;
                            transition: all 0.3s ease;
                            z-index: 100;
                        }

                        :deep(.userInfoCard) {
                            width: 0px;
                            height: 0px;

                            position: absolute;
                            left: 50%;
                            top: 50%;

                            border-radius: 50%;

                            transform: translateX(-50%);
                        }
                        
                        &:hover {
                            :deep(.userInfoCard) {
                                width: 300px;
                                height: 200px;

                                border-radius: 5px;
                            }

                            .avatar {
                                box-shadow: 0px 5px 30px 5px $foregroundLightenColor;
                            }
                        }
                    }
                }
            }
        }
    }
}
</style>
