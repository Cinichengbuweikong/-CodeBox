import { createStore } from "vuex";

import getUserInfo from "@/utils/getUserInfo";
import { UserInfo } from "@/types";


interface State {
    // state 定义

    userinfo: UserInfo | null,
    // 用户个人信息
}

interface Context {
    // actions 中 context 参数的类型定义

    commit: (mutationName: string, value: any) => void,
}


const state: State = {
    userinfo: null
};

const actions = {
    async fetchUserInfo(context: Context) {
        // 从网络上获取最新的用户信息

        try {
            const userInfo: UserInfo | null = await getUserInfo();

            if (userInfo !== null) {
                context.commit("UPDATE_USER_INFO", userInfo);
            }
        } catch(e) {
            console.log("获取用户信息时出错:", e);
        }
    }
};

const mutations = {
    UPDATE_USER_INFO(state: State, userInfo: UserInfo) {
        // 更新用户信息 如果用户没登陆的话就设置 state.userinfo = null;

        state.userinfo = userInfo;
    },

    REMOVE_USER_INFO(state: State) {
        // 删除登录用户信息
        state.userinfo = null;
    }
};

const getters = {};

export default createStore({
    state,
    actions,
    mutations,
    getters
});