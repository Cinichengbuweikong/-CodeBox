<template>
    <div class="userSettings">
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
            
            enctype="multipart/form-data"
            method="post"
            action="/api/user"
            target="frame"
        >
            <el-form-item label="头像">
                <el-upload
                    class="avatar-uploader"
                    accept=".jpg,.png"
                    name="avatarimg"
                    :show-file-list="true"
                    :auto-upload="false"
                    :limit="1"
                >
                    <el-text>点击选择</el-text>
                </el-upload>
            </el-form-item>

            <el-form-item label="用户名">
                <el-input name="username" v-model="formData.username" />
            </el-form-item>

            <el-form-item label="密码">
                <el-input name="password" v-model="formData.password" />
            </el-form-item>

            <el-form-item label="自我介绍">
                <el-input name="description" v-model="formData.description" />
            </el-form-item>

            <el-form-item class="submitFormItem">
                <el-button 
                    type="primary"
                    @click="onSubmitButtonClick"
                >
                    OK!
                </el-button>
            </el-form-item>
        </el-form>

        <transition>
            <ConfirmPasswordDialog
                :showDialog="showConfirmPasswordDialog"
                :cancel="cancelShowConfirmPasswordDialog"
                :submitAction="onConfirmPasswordDialogClose"
            />
        </transition>
    </div>
</template>


<script setup lang="ts">
import {
    defineOptions,
    reactive,
    ref,

    ComponentPublicInstance
} from "vue";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";

import ConfirmPasswordDialog from "../Dialog/confirmPasswordDialog.vue";
import { UserInfo } from "@/types";
import eventSub from "@/utils/eventSub";


defineOptions({
    name: "userSettings"
});

const store = useStore();

const showConfirmPasswordDialog = ref<boolean>(false);
// 是否要显示 "确认密码" 对话框

const userInfo = ref<UserInfo>(store.state.userinfo);
// 用户信息

const formData = reactive({
    // 表单数据 没啥用  只是因为 el-form 不写 v-model 的话它就无法输入内容
    username: userInfo.value.username,
    password: "",
    email: userInfo.value.email,
    description: userInfo.value.description,
    avatar: userInfo.value.avatarurl
});

const formRef = ref<ComponentPublicInstance | null>(null);
// 表单元素的引用


function iframeLoad() {
    // iframe 触发 load 事件 表示数据已经更新完成
    // 此时设置 vuex 重新加载页面中的信息即可
    
    store.dispatch("fetchUserInfo");
    
    eventSub.emit("userPageUpdateInfo");
    // 触发更新 userPage 信息事件

    ElMessage("内容刷新完成");
    console.log("iframe reloaded!");
}

function cancelShowConfirmPasswordDialog() {
    // 当 "确认密码" 对话框的取消按钮按下时需要执行的回调
    showConfirmPasswordDialog.value = false;
}

function submitForm(): void {
    // 提交表单

    ElMessage("正在提交信息");

    if (formRef.value === null) {
        ElMessage("除了一点错误 请稍后再试");
        console.log("意外地没获取到 form 组件实例对象");
        return ;
    }

    try {
        (formRef.value.$el as HTMLFormElement).submit();
    } catch(e) {
        ElMessage("信息提交失败了 请稍后再试");
        console.log("信息修改出错", e);
    }
}

function onConfirmPasswordDialogClose(
    enteredPassword: string,
): "wrong password" | void {
    // 当 "确认密码" 对话框的 "OK!" 按钮按下后需要执行的回调

    // enteredPassword  用户再次输入的内容
    // "wrong password" 表示用户再次输入的密码错误

    if (enteredPassword !== formData.password) {
        return "wrong password";
    }

    submitForm();
    showConfirmPasswordDialog.value = false;

    return ;
}

function onSubmitButtonClick() {
    // 当页面上的 "OK!" 按钮下后执行的回调

    if (formData.password !== "") {
        // 如果用户要修改密码的话 那就需要发送验证码 而后显示验证密码对话框

        showConfirmPasswordDialog.value = true;
        return ;
    }

    // 否则就直接进行修改即可
    submitForm();
}
</script>


<style lang="scss" scoped>
.userSettings {
    width: 80%;
    margin: auto;

    padding: 40px 0;

    .el-form {        
        .avatar-uploader .avatar {
            width: 100px;
            height: 100px;
            display: block;
        }

        .submitFormItem {
            --el-color-primary: #{ $actionColor };
            --el-color-primary-light-3: #{ $actionColor };

            :deep(.el-form-item__content) {
                flex-direction: row;
                justify-content: flex-start;
            }
        }

        .el-form-item {
            .el-input {
                --el-text-color-regular: #{ $fontDarkColor };
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
