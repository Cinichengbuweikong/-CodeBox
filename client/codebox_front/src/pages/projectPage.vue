<template>
    <div class="projectPage">
        <el-container>
            <el-main>
                <suspense>
                    <VueRepl />
                </suspense>

                <el-row class="infoBox">
                    <div class="title">
                        <el-text>{{ projectInfo ? projectInfo.projectname : "Title" }}</el-text>
                    </div>
                    
                    <div class="info">
                        <el-avatar 
                            :size="50" 
                            :src="`/assets/avatars/${projectOwnerInfo? projectOwnerInfo.avatarurl : 'default.jpg'}`"
                            @click="routeToUserPage"
                        />

                        <div>
                            <el-text class="username">{{ projectOwnerInfo ? projectOwnerInfo.username : "username" }}</el-text>
                            <el-text class="description">{{ projectInfo ? projectInfo.description : "Title" }}</el-text>
                        </div>
                    </div>
                </el-row>

                <el-row 
                    class="actionBox"
                    v-if="store.state.userinfo !== null"
                >
                    <div 
                        @click="toggleStarProject"
                    >
                        <i class="iconfont" :class="starIconComputedClass"></i>
                        <el-text>收藏</el-text>
                    </div>

                    <div 
                        @click="copyProjectAsTemporary"
                    >
                        <i class="iconfont icon-xiangmu"></i>
                        <el-text>复制此项目为临时项目</el-text>
                    </div>
                    
                    <div
                        v-if="isOwn"
                        @click="routerToProjectSettingsPage"
                    >
                        <i class="iconfont icon-modify"></i>
                        <el-text>修改此项目</el-text>
                    </div>

                    <div
                        v-if="isOwn"
                        @click="eventSub.emit('saveChanges')"
                    >
                        <i class="iconfont icon-baocun"></i>
                        <el-text>保存修改</el-text>
                    </div>
                </el-row>
                
                <el-row class="commentBox">
                    <el-container>
                        <el-row>
                            <el-text>评论</el-text>
                        </el-row>

                        <el-row class="newCommentBox">
                            <el-input
                                    v-model="newComment"
                                    type="textarea"
                                    placeholder="来几句... (Shift+Enter 发布)"
                                    @keyup.shift.enter="addNewComment"
                            />
                        </el-row>

                        <el-row class="commentList">
                            <ul>
                                <li v-if="comments.length === 0">
                                    <el-text>本项目还没有评论哟~</el-text>
                                </li>

                                <CommentItem
                                    v-else

                                    v-for="c in comments"
                                    :key="c.cid"
                                    :cid="c.cid"
                                    :uid="c.uid"
                                    :comment="c.comment"
                                    :date="c.date"
                                    :like="c.like"
                                    :youlike="c.youlike"
                                    :getComment="getComment"
                                />
                            </ul>

                            <el-pagination
                                v-if="comments.length !== 0"
                                background
                                layout="prev, pager, next"
                                :page-size="perPageCommentNum"
                                :total="totalCommentsNum"
                            />
                        </el-row>
                    </el-container>
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
    computed
} from "vue";
import { useStore } from "vuex";
import {
    useRoute,
    useRouter
} from "vue-router";
import axios from "axios";
import VueRepl from "@/components/Repl/vueRepl.vue";
import { ElMessage } from "element-plus";

import PageFooter from "@/components/Footer/pageFooter.vue";
import CommentItem from "@/components/Comment/commentItem.vue";
import { UserInfo } from "@/types";
import eventSub from "@/utils/eventSub";
import { Project, Comment } from "@/types";
import hasThisProject from "@/utils/premissions/hasThisProject";


defineOptions({
    name: "projectPage"
});

const route = useRoute();
const router = useRouter();
const store = useStore();

const newComment = ref<string>("");
// 用户输入的评论

const isOwn = ref<boolean>(false);
// 这个项目是不是当前用户自己的?

const projectInfo = ref<Project | null>(null);
// 当前项目信息

const projectOwnerInfo = ref<UserInfo | null>(null);
// 当前项目拥有者的信息

const userStaredProject = ref<boolean>(false);
// 当前登录用户是否收藏了此项目?

const comments = ref<Array<Comment>>([]);
// 评论数据

const totalCommentsNum = ref<number>(0);
// 总共有几条评论数据

const perPageCommentNum = ref<number>(0);
// 一页有几条评论数据

const page = ref<number>(1);
// 现在看的是第几页的评论


(async function() {
    // 鉴权函数  鉴定如下内容:
    // 此项目是否存在
    
    await hasThisProject(router, (route.params.pid as string));
})();


const starIconComputedClass = computed(() => {
    // "收藏项目" 元素的动态 class

    return {
        "icon-gerenzhongxinqietu": userStaredProject.value,
        "icon-shoucang": !userStaredProject.value,
    };
});


function routerToProjectSettingsPage(): void {
    // 当 "修改此项目按钮" 点击时 跳转到项目设置页
    router.push({
        path: `/projects/${route.params.pid}/settings`
    });
}

async function starProject(): Promise<void> {
    // 当用户点击 "收藏" 按钮时 执行此回调以收藏项目

    try {
        const rep = await axios.post("/api/user/stars", {
            pid: route.params.pid
        });

        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            throw rep;
        }

        userStaredProject.value = true;
    } catch(e) {
        console.log("收藏请求失败了: ",e);
    }
}

async function unstarProject(): Promise<void> {
    // 当用户已经收藏项目后 再次点击 "收藏" 图标即可取消收藏

    try {
        const rep = await axios.delete("/api/user/stars", {
            data: {
                pid: route.params.pid
            }
        });

        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            throw rep;
        }

        userStaredProject.value = false;
    } catch(e) {
        console.log("收藏请求失败了: ",e);
    }
}

async function toggleStarProject() {
    // 当用户点击 "收藏" 按钮后 根据当前项目的收藏状态决定执行哪个函数

    if (userStaredProject.value) {
        ElMessage("正在取消收藏");
        await unstarProject();
    } else {
        ElMessage("正在收藏");
        await starProject();
    }
}

async function getComment(): Promise<void> {
    // 从网络上获取当前项目的评论

    try {
        const rep = await axios.get(`/api/projects/${route.params.pid}/comments`, {
            params: {
                page: page.value
            }
        });

        if(rep.status !== 200 || !rep.data) {
            throw rep;
        }

        comments.value = rep.data.data;
        totalCommentsNum.value = rep.data.total;
        perPageCommentNum.value = rep.data.perpage;
    } catch(e) {
        console.log("获取评论数据失败了: ", e);
    }
}

async function addNewComment(): Promise<void> {
    // 新建评论

    ElMessage("正在发送评论");
    
    if (newComment.value === "") {
        // 用户没输入内容 那就返回
        return ;
    }

    try {
        const rep = await axios.post(`/api/projects/${route.params.pid}/comments`, {
            comment: newComment.value
        });

        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            throw rep;
        }

        // 新建成功 清除输入框中的内容
        newComment.value = "";

        ElMessage("评论发送成功");

        // 重新获取评论
        await getComment();
    } catch(e) {
        ElMessage("评论发送失败 请稍后再试");
        console.log("评论新建失败: ", e);
    }
}

function routeToUserPage(): void {
    // 当用户点击头像后 我们需要重定向至用户信息页

    router.push(`/user/${projectOwnerInfo.value?.uid}`);
}

async function copyProjectAsTemporary(): Promise<void> {
    // 当 "复制此工程为临时工程" 按钮按下时执行此回调

    ElMessage("正在复制");

    try {
        const rep = await axios.post("/api/projects/temporaryproject", {
            pid: route.params.pid
        });

        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            throw rep;
        }

        ElMessage("复制成功 正在前往临时项目页");
        router.push(`/projects/temp/${rep.data.tpid}`);
    } catch(e) {
        ElMessage("复制失败");
        console.log("复制项目失败: ", e);
    }
}


onBeforeMount(() => {
    console.clear = () => {};
});

onMounted(async () => {
    try{
        // 从网络获取数据 判断当前项目是否是用户自己的

        // 获取项目信息
        const rep = await axios.get(`/api/projects/${route.params.pid}/`);

        if (rep.status !== 200 || !rep.data) {
            throw rep;
        }

        if (
            store.state.userinfo !== null 
            && rep.data.uid === store.state.userinfo.uid
        ) {
            isOwn.value = true;
        }

        projectInfo.value = rep.data;
    } catch(e) {
        console.log("获取项目信息失败: ", e);
    }

    try {
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
        console.log("获取项目所有者信息失败: ", e);
    }

    try {
        // 从网络上获取收藏信息 用户是否收藏了此项目?

        const starsRep = await axios.get("/api/stars/", {
            params: {
                pid: route.params.pid
            }
        });

        if (starsRep.status !== 200 || !starsRep.data || starsRep.data.code !== 200) {
            throw starsRep;
        }

        userStaredProject.value = starsRep.data.star;
    } catch(e) {
        console.log("获取收藏信息失败: ", e);
    }

    // 获取评论数据
    await getComment();
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

                        &.icon-gerenzhongxinqietu {
                            color: $actionColor;
                        }
                    }
                }
            }

            .commentBox {
                width: 100%;
                overflow: visible;

                .el-container {
                    width: 100%;
                    min-height: 400px;
                    overflow: visible;

                    display: flex;
                    flex-direction: column;
                    align-items: center;

                    .el-row:first-child {
                        width: 70%;
                        height: 120px;

                        display: flex;
                        flex-direction: row;
                        justify-content: space-between;
                        align-items: flex-end;

                        border-bottom: 1px solid #ccc;
                        
                        .el-text {
                            align-self: flex-end;

                            font-size: 44px;
                            font-weight: bold;

                            margin-bottom: 5px;

                        }

                        .el-link {
                            margin-bottom: 5px;
                        }
                    }

                    .newCommentBox {
                        width: 70%;

                        display: flex;
                        justify-content: center;
                        align-items: center;

                        padding: 10px 0;

                        transform-origin: center top;

                        --el-text-color-regular: #{ $fontDarkColor };
                    }

                    .commentList {
                        width: 70%;
                        padding-bottom: 76px;

                        ul {
                            width: 100%;
                            list-style: none;
                        }

                        .el-pagination {
                            margin-top: 30px;
                        }
                    }
                }
            }
        }
    }
}
</style>
