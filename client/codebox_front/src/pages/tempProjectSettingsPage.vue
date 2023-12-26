<template>
    <div class="projectSettingsPage">
        <el-container>
            <PageHeader />

            <el-main>
                <iframe 
                    src="" 
                    frameborder="0" 
                    name="frame" 
                    style="width: 0; height: 0; display: none;"
                    @load="iframeLoad"
                ></iframe>
                
                <el-form
                    label-width="120px"
                    ref="formRef"
                >
                    <el-form-item class="descFormItem">
                        <el-text class="title">这是一个临时项目!</el-text>
                        <el-text class="description">你只有发布项目后才能修改项目的其他信息 例如设置项目名或设置效果图</el-text>
                    </el-form-item>

                    <el-form-item class="dangerActionFormItem">
                        <el-button 
                            type="danger" 
                            @click="PublishProjectDialogData.show = true"
                        >
                            发布此项目
                        </el-button>
                        
                        <el-button 
                            type="danger"
                            @click="DeleteProjectDialogData.show = true"
                        >
                            删除此项目
                        </el-button>
                    </el-form-item>
                </el-form>
            </el-main>
            
            <PageFooter />
        </el-container>

        <transition>
            <DeleleProjectDialog
                v-if="DeleteProjectDialogData.show"
                :cancel="DeleteProjectDialogData.cancel"
                :next="DeleteProjectDialogData.next"
            />
        </transition>

        <transition>
            <PublishProjectDialog
                v-if="PublishProjectDialogData.show"
                :cancel="PublishProjectDialogData.cancel"
                :next="PublishProjectDialogData.next"
            />
        </transition>
    </div>
</template>


<script setup lang="ts">
import {
    defineOptions,
    ref,
    onMounted,

    ComponentPublicInstance
} from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { ElMessage } from "element-plus";

import PageHeader from "@/components/Header/pageHeader.vue";
import PageFooter from "@/components/Footer/pageFooter.vue";
import DeleleProjectDialog from "@/components/Dialog/deleteProjectDialog.vue";
import PublishProjectDialog from "@/components/Dialog/publishProjectDialog.vue";
import { TempProject } from "@/types";
import hasUserLogin from "@/utils/premissions/hasUserLogin";
import hasThisTemporaryProject from "@/utils/premissions/hasThisTemporaryProject";
import hasUserOwnProject from "@/utils/premissions/hasUserOwnProject";


defineOptions({
    name: "projectSettingsPage"
});

const route = useRoute();
const router = useRouter();
const store = useStore();

const formRef = ref<ComponentPublicInstance | null>(null);
// form 表单的 ref

const DeleteProjectDialogData = ref({
    // 删除项目对话框所需的数据
    
    show: false,
    // 是否显示此对话框

    cancel: (): void => {
        // 当用户按下 "删除项目" 对话框的 "取消" 按钮时
        DeleteProjectDialogData.value.show = false;
    },
    
    next: async (): Promise<void> => {
        // 当用户按下 "删除项目" 对话框的 "删除" 按钮时

        ElMessage("正在删除项目");

        try {
            const rep = await axios.delete("/api/projects/temporaryproject", {
                data: {
                    tpid: route.params.tpid
                }
            });

            if (rep.status !==200 || !rep.data || rep.data.code !== 200) {
                throw rep;
            }

            DeleteProjectDialogData.value.show = false;

            // 删除完成后就返回到上上的页面即可
            router.go(-2);
        } catch(e) {
            console.log("删除项目时出错: ", e);
        }
    }
});

const PublishProjectDialogData = ref({
    // 发布项目对话框所需的数据
    
    show: false,
    // 是否显示此对话框
    cancel: (): void => {
        // 当用户按下 "发布项目" 对话框的 "取消" 按钮时
        PublishProjectDialogData.value.show = false;
    },
    next: async (): Promise<void> => {
        // 当用户按下 "发布项目" 对话框的 "发布" 按钮时

        ElMessage("正在发布项目");

        try {
            const rep = await axios.put("/api/projects/temporaryproject", {
                tpid: route.params.tpid
            });

            if (rep.status !==200 || !rep.data || rep.data.code !== 200) {
                throw rep;
            }

            PublishProjectDialogData.value.show = false;

            ElMessage("发布成功 正跳转到项目页");

            // 发布完成后就导航到发布的项目页即可
            router.replace(`/projects/${rep.data.pid}`);
        } catch(e) {
            console.log("删除项目时出错: ", e);
        }
    }
});


(async function() {
    // 鉴权函数  检查以下权限:
    // 用户是否已登录
    // 此临时项目是否存在
    // 用户是否拥有此临时项目

    await hasUserLogin(router);

    const pInfo = await hasThisTemporaryProject(router, (route.params.tpid as string));

    hasUserOwnProject(store, router, `${(pInfo as TempProject).uid}`);
})();


async function iframeLoad() {
    // 当 iframe load 的时候触发的回调 表示修改提交完成(不一定成功)
    
    console.log("信息修改完成");
}


onMounted(() => {
});
</script>


<style lang="scss" scoped>
.projectSettingsPage {
    width: 100vw;
    height: 100vh;

    .el-container {
        width: 100%;
        height: 100%;

        flex-direction: column;

        overflow-y: scroll;

        .el-main {
            width: 100%;

            padding-bottom: 60px;
            margin-top: 60px;

            overflow: visible;

            .el-form {
                width: 100%;

                .descFormItem {
                    height: 70px;

                    :deep(.el-form-item__content) {
                        flex-direction: column;
                    }

                    .title, .description {
                        display: block;
                        align-self: flex-start;
                    }

                    .title {
                        font-size: 32px;
                        font-weight: bold;
                    }

                    .description {
                        font-size: 16px;
                    }
                }

                .el-form-item {
                    width: 90%;
                    margin-bottom: 10px;
                    margin-left: auto;
                    margin-right: auto;
                }

                .effect-uploader .effect {
                    width: 300px;
                    aspect-ratio: 16/10;
                    display: block;
                }

                .dangerActionFormItem, .submitFormItem {
                    :deep(.el-form-item__content) {
                        flex-direction: column;
                        align-items: flex-start;

                        .el-button {
                            margin: 10px 0;
                        }
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
