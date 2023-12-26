<template>
    <li class="commentItem">
        <el-row>
            <el-col class="avatarBox" :span="2">
                <el-avatar 
                    :size="50" 
                    :src="`/assets/avatars/${userInfo ? userInfo.avatarurl : 'default.jpg'}`"
                    @click="routeToUserPage"
                />
            </el-col>

            <el-col class="commentBox" :span="22">
                <el-text class="username">{{ userInfo ? userInfo.username : "" }}</el-text>

                <el-text class="comment">{{ props.comment }}</el-text>

                <div 
                    class="actionBox"
                    @click="onCommentBoxClick"
                >
                    <span>
                        <span>{{ props.like }}</span>
                        <i class="iconfont" :class="zanIconComputedClass" @click="onCommentLike"></i>
                    </span>

                    <span
                        v-if="commentIsYours"
                        class="iconDeleteBox" 
                        id="iconDeleteBox"
                    >
                        <i class="iconfont icon-shanchu1" id="iconShanchu"></i>
                        
                        <transition>
                            <DeleteCommentDialog
                                v-if="deleteCommentDialogData.show"
                                :x="deleteCommentDialogData.x"
                                :y="deleteCommentDialogData.y"
                                :next="deleteCommentDialogData.next"
                                :close="deleteCommentDialogData.close"
                            />
                        </transition>
                    </span>
                </div>
            </el-col>
        </el-row>
    </li>
</template>


<script setup lang="ts">
import "@/assets/iconfonts/iconfont.css";

import {
    defineOptions,
    ref,
    defineProps,
    onMounted,
    computed
} from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import DeleteCommentDialog from "../Dialog/deleteCommentDialog.vue";
import { UserInfo } from "@/types";
import axios from "axios";


defineOptions({
    name: "commentItem",
});

const props = defineProps({
    cid: {
        // 此评论的 id
        type: Number,
        required: true
    },

    uid: {
        // 评论的用户 id
        type: Number,
        required: true
    },

    comment: {
        // 评论内容
        type: String,
        required: true
    },

    date: {
        // 评论日期
        type: String,
        required: true
    },

    like: {
        // 评论赞数
        type: Number,
        required: true
    },

    youlike: {
        // 当前登录用户是否赞这个评论
        type: Boolean,
        required: true
    },

    getComment: {
        // 重新获取评论的函数
        type: Function,
        defualt: async () => {}
    },
});

const store = useStore();

const route = useRoute();
const router = useRouter();


const deleteCommentDialogData = ref<{
    // 保存关于删除评论对话框的数据
    show: boolean,
    x: number,
    y: number,
    next: Function,
    close: Function
}>({
    show: false,
    x: 0,
    y: 0,
    next: async () => {
        // 删除评论时所需执行的函数
        
        ElMessage("正在删除评论");

        try {
            const rep = await axios.delete(`/api/projects/${route.params.pid}/comments`, {
                data: {
                    cid: props.cid
                }
            });

            if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
                throw rep;
            }
            
            deleteCommentDialogData.value.show = false;

            ElMessage("评论删除成功");

            // 评论删除成功 刷新评论列表
            await props.getComment!();
        } catch(e) {
            ElMessage("评论删除失败");
            console.log("评论删除失败: ", e);
        }
    },
    close: () => {
        // 当 "算了" 按钮按下时的回调 需要取消显示对话框
        deleteCommentDialogData.value.show = false;
    }
});

const userInfo = ref<UserInfo | null>(null);
// 当前评论的用户的信息


const commentIsYours = computed(() => {
    // 本条评论是否时当前用户发出的?
    return store.state.userinfo?.uid === userInfo.value?.uid;
});

const zanIconComputedClass = computed(() => {
    // 评论中 "赞" 按钮的计算 class

    return {
        "icon-zan": !props.youlike,
        "icon-zan1": props.youlike
    };
});


function onCommentBoxClick(event: MouseEvent): void {
    // 当 .commentBox 点击时触发的事件
    // 主要在这里通过事件委托处理删除评论按钮的功能

    if ((event.target as HTMLElement).classList.contains("icon-shanchu1")) {
        // 用户按了删除按钮

        deleteCommentDialogData.value.show = true;
        deleteCommentDialogData.value.x = event.clientX;
        deleteCommentDialogData.value.y = event.clientY;
    }
}

async function likeComment() {
    // 赞一条评论

    try {
        const rep = await axios.patch(`/api/projects/${route.params.pid}/comments`, {
            cid: props.cid,
            like: true
        });

        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            throw rep;
        }
    } catch(e) {
        console.log("赞失败了: ", e);
    }
}

async function unlikeComment() {
    // 取消赞一条评论

    try {
        const rep = await axios.patch(`/api/projects/${route.params.pid}/comments`, {
            cid: props.cid,
            like: false
        });

        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            throw rep;
        }
    } catch(e) {
        console.log("赞失败了: ", e);
    }
}

async function onCommentLike() {
    // 当用户点击评论的 "赞" 按钮时执行此回调 根据实际情况选择执行赞或是取消赞的动作

    if (props.youlike) {
        await unlikeComment();
    } else {
        await likeComment();
    }

    // 最后更新评论状态
    await props.getComment!();
}

function routeToUserPage() {
    // 当用户点击评论的头像后 我们需要将用户导航到用户信息页
    router.push(`/user/${userInfo.value?.uid}`);
}


onMounted(async () => {
    try {
        // 获取用户信息
        const rep = await axios.get("/api/user/", {
            params: {
                uid: props.uid
            }
        });

        if (rep.status !== 200 || !rep.data) {
            throw rep;
        }

        userInfo.value = rep.data;
    } catch(e) {
        console.log("获取用户数据时出错: ", e);
    }
});
</script>


<style scoped lang="scss">
.commentItem {
    width: 100%;
    min-height: 100px;

    border-bottom: 1px solid #ccc;

    margin: 5px 0;

    .el-row {
        width: 100%;

        .avatarBox {
            .el-avatar {
                cursor: pointer;
            }
        }

        .commentBox {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;

            .el-text {
                align-self: flex-start;
                font-size: 16px;
            }

            .username {
                display: block;
                width: 100%;
                height: 30px;

                font-weight: bold;
            }

            .comment {
                display: block;
                width: 100%;
            }

            .actionBox {
                margin: 10px 0;

                span {
                    vertical-align: top;
                    color: darken($color: $fontColor, $amount: 20);

                    i {
                        font-size: 22px;
                        margin-right: 15px;
                        cursor: pointer;

                        &.icon-zan1 {
                            color: $actionColor;
                        }
                    }

                    &.iconDeleteBox {
                        position: relative;
                    }
                }
            }
        }
    }
}

.v-enter-active, .v-leave-active {
    transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.v-enter-active {
    opacity: 0;
}

.v-enter-to, .v-leave-active {
    opacity: 1;
}

.v-leave-to {
    opacity: 0;
}

</style>
