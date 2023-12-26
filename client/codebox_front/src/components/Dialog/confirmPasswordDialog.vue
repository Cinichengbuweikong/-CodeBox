<template>
    <div 
        class="confirmPasswordDialogBox"
        v-if="props.showDialog"
    >
        <div class="confirmPasswordDialog">
            <el-row>
                <el-text class="title">你想要修改密码!</el-text>
                <el-text class="description">请重复一遍新密码 以确保你还记设置的密码是正确的</el-text>
                <el-text>{{ getTipMessage }}</el-text>

                <el-input 
                    v-model="confirmedPassword"
                    type="password"
                    placeholder="请重复密码"
                />
            </el-row>
    
            <el-row>
                <el-button class="cancel" @click="props.cancel">取消</el-button>
                <el-button type="primary" @click="submitAction">OK!</el-button>
            </el-row>
        </div>
    </div>
</template>


<script setup lang="ts">
import {
    defineOptions,
    defineProps,
    ref,
    withDefaults,
    computed
} from "vue";


defineOptions({
    name: "confirmPasswordDialog"
});

const props = withDefaults(
    defineProps<{
        showDialog?: boolean,
        // 是否显示此对话框

        cancel: () => void,
        // 当对话框需要隐藏时需要调用的函数

        submitAction: (confirmedPassword: string) => "wrong password" | void,
        // 当需要执行修改时需要执行的函数
    }>(),
    {
        showDialog: false,
    }
);

const confirmedPassword = ref<string>("");
// 用户再次输入的密码


const wrongPassword = ref<boolean>(false);
// 用户输入的两次密码是否不一致?


const getTipMessage = computed((): string => {
    // 获取需要显示在对话框中的提示信息

    if (wrongPassword.value) {
        return "两次输入的密码不一致 请重试";
    }

    return "";
});

function submitAction() {
    // 当 OK 删除按钮按下时

    const res = props.submitAction(confirmedPassword.value);

    if (res === "wrong password") {
        wrongPassword.value = true;
        return ;
    }

    props.cancel();
}
</script>


<style lang="scss" scoped>
.confirmPasswordDialogBox {
    position: fixed;
    left: 0;
    top: 0;

    width: 100vw;
    height: 100vh;

    z-index: 1000;

    .confirmPasswordDialog {
        width: 600px;
        height: 300px;

        position: fixed;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);

        background-color: $backgroundColor;

        border-radius: 3px;
        box-shadow: 0px 1px 5px 2px $backgroundDarkenColor;

        .el-row:first-child {
            height: 70%;

            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: flex-start;
            flex-wrap: nowrap;

            .el-text {
                align-self: flex-start;
                padding-left: 20px;
                padding-top: 10px;
            }

            .title {
                font-size: 22px;
                font-weight: bold;

                padding-top: 20px;
            }

            .description {
                font-size: 18px;
            }

            .el-input {
                width: calc(100% - 40px);
                margin: 10px auto;
                --el-text-color-regular: #{ $fontDarkColor };
            }
        }

        .el-row:last-child {
            height: 30%;

            display: flex;
            flex-direction: row;
            justify-content: flex-end;
            align-items: center;

            .el-button {
                margin-right: 20px;

                &.cancel {
                    --el-text-color-regular: #{ $foregroundColor };
                }
            }
        }
    }
}
</style>
