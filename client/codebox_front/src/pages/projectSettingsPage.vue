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
                    :model="formData" 
                    label-width="120px"
                    ref="formRef"

                    method="post"
                    action="/api/user/projects"
                    enctype="multipart/form-data"
                    target="frame"
                >
                    <input name="pid" :value="projectInfo?.pid" type="hidden"/>

                    <el-form-item label="效果图">
                        <el-upload
                            class="effect-uploader"
                            :show-file-list="true"
                            :auto-upload="false"
                            :limit="1"
                            accept=".jpg,.png"
                            name="effectimg"
                        >
                            <img :src="`/assets/effects/${projectInfo?.effectimg ?? 'default.jpg'}`" class="effect" />
                        </el-upload>
                    </el-form-item>

                    <el-form-item label="项目名">
                        <el-input v-model="formData.projectName" name="projectname" />
                    </el-form-item>

                    <el-form-item label="项目介绍">
                        <el-input v-model="formData.projectDescription" name="description" />
                    </el-form-item>

                    <el-form-item class="dangerActionFormItem">
                        <el-button 
                            type="danger"
                            @click="DeleteProjectDialogData.show = true"
                        >
                            删除此项目
                        </el-button>
                    </el-form-item>

                    <el-form-item class="submitFormItem">
                        <el-button type="primary" @click="formSubmit">OK!</el-button>
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
    </div>
</template>


<script setup lang="ts">
import {
    defineOptions,
    ref,
    reactive,
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
import { Project } from "@/types";
import hasUserLogin from "@/utils/premissions/hasUserLogin";
import hasThisProject from "@/utils/premissions/hasThisProject";
import hasUserOwnProject from "@/utils/premissions/hasUserOwnProject";


defineOptions({
    name: "projectSettingsPage"
});

const route = useRoute();
const router = useRouter();
const store = useStore();


const formData = reactive({
    // 表单数据 没啥用 没了它表单就输入不了内容了
    projectName: "",
    projectDescription: ""
});

const projectInfo = ref<Project | null>(null);
// 项目数据

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

        ElMessage("正在删除");

        try {
            const rep = await axios.delete("/api/user/projects", {
                data: {
                    pid: route.params.pid
                }
            });

            if (rep.status !==200 || !rep.data || rep.data.code !== 200) {
                throw rep;
            }

            DeleteProjectDialogData.value.show = false;

            // 删除完成后就返回到上上的页面即可
            router.go(-2);
        } catch(e) {
            ElMessage("删除失败 请稍后再试");
            console.log("删除项目时出错: ", e);
        }
    }
});


(async function() {
    // 鉴权函数  鉴定如下内容:
    // 用户是否登录
    // 用户是否拥有此项目
    // 此项目是否存在

    await hasUserLogin(router);

    const pInfo = await hasThisProject(router, (route.params.pid as string));
    projectInfo.value = (pInfo as Project);

    hasUserOwnProject(store, router, projectInfo.value.uid);
})();


function formSubmit() {
    // 当用户按下提交表单按钮时所触发的函数

    ElMessage("正在提交数据");

    (formRef.value?.$el as HTMLFormElement).submit();
}

async function iframeLoad() {
    // 当 iframe load 的时候触发的回调 表示修改提交完成(不一定成功)

    // 数据提交完成后刷新页面中的数据
    await fetchProjectInfo();

    ElMessage("数据更新完成");
}

async function fetchProjectInfo(): Promise<void> {
    // 获取项目信息的函数

    ElMessage("正在获取项目信息 请等待...");

    try {
        // 获取项目信息

        const projectRep = await axios.get(`/api/projects/${route.params.pid}/`);
        
        if (projectRep.status !== 200 || !projectRep.data) {
            throw projectRep;
        }

        projectInfo.value = projectRep.data;

        formData.projectName = projectInfo.value?.projectname ?? "";
        formData.projectDescription = projectInfo.value?.description ?? "";

        ElMessage("项目信息获取完成 可以继续了");
    } catch(e) {
        ElMessage("获取项目信息时出错");
        console.log("请求项目数据时出错: ", e);
    }
}


onMounted(async () => {
    formData.projectName = projectInfo.value?.projectname ?? "";
    formData.projectDescription = projectInfo.value?.description ?? "";
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

                .el-form-item {
                    width: 90%;
                    margin-bottom: 10px;
                    margin-left: auto;
                    margin-right: auto;

                    .el-input {
                        --el-text-color-regular: #{ $fontDarkColor };
                    }
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
