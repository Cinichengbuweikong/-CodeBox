<template>
    <transition name="dialogTransition">
        <div 
            class="loginOrSignupDialog"
            v-if="show"
        >
            <el-card
                class="dialog"
                :body-style="{width: '100%', height: '100%', padding: '0px'}"
                shadow="never"
            >
                <div
                    class="loginOrSignupDialogBody"
                >
                    <el-row class="titleBox">
                        <el-text>你好! 请</el-text>

                        <div class="actionNameBox">
                            <transition-group name="actionNameTransition">
                                <el-text class="actionName" v-if="actionType === 'login'">登录</el-text>
                                <el-text class="actionName" v-if="actionType === 'signup'">注册</el-text>
                                <el-text class="actionName" v-if="actionType === 'verifyCode'">输入验证码</el-text>
                            </transition-group>
                        </div>
                    </el-row>

                    <transition-group>
                        <el-row 
                            class="formBox"
                            v-if="actionType === 'login'"
                        >
                            <el-input
                                v-model="email"
                                placeholder="请输入你的邮箱"
                            />

                            <el-input 
                                type="password"
                                v-model="password"
                                placeholder="请输入你的密码"
                            />

                            <el-link
                                class="signup"
                                :underline="false"
                                @click="
                                    actionType = 'signup';
                                    prevActionType = 'signup';
                                    actionResult = null
                                "
                            >
                                我想注册一个账号
                            </el-link>

                            <el-text class="actionInfo" v-if="actionResult !== null">
                                {{ actionResult }}
                            </el-text>
                        </el-row>

                        <el-row 
                            class="formBox"
                            v-if="actionType === 'signup'"
                        >
                            <el-input
                                v-model="username"
                                placeholder="为你的账号起一个名字"
                            />

                            <el-input
                                v-model="email"
                                placeholder="请输入你的邮箱"
                            />

                            <el-input 
                                type="password"
                                v-model="password"
                                placeholder="请输入你的密码"
                            />

                            <el-link
                                class="signup"
                                :underline="false"
                                @click="
                                    actionType = 'login';
                                    prevActionType = 'login';
                                    actionResult = null
                                "
                            >
                                我想登录我的账号
                            </el-link>

                            <el-text class="actionInfo" v-if="actionResult !== null">
                                {{ actionResult }}
                            </el-text>
                        </el-row>

                        <el-row 
                            class="formBox"
                            v-if="actionType === 'verifyCode'"
                        >
                            <el-text>
                                我们已将验证码发送到你的邮箱，你可能需要等一会才会收到它。
                                (这里直接把验证码显示在这里了，因为我用的是个人邮箱，频繁地发送相似内容的邮件会被邮件服务商认为我在发垃圾邮件 然后直接一个限流 我就发不出去邮件了)。
                            </el-text>

                            <el-text>验证码是: {{ gettedVerifyCode }}</el-text>

                            <el-text class="actionInfo" v-if="actionResult !== null">
                                {{ actionResult }}
                            </el-text>

                            <el-input
                                v-model="verifyCode"
                                placeholder="请输入您接收到的验证码"
                            />
                        </el-row>
                    </transition-group>

                    <el-row class="actionBox">
                        <el-button
                            @click="closeDialog"
                        >
                            取消
                        </el-button>
                        
                        <el-button 
                            type="primary"
                            @click="onNextButtonClick"
                        >{{actionName}}</el-button>
                    </el-row>
                </div>
            </el-card>
        </div>
    </transition>
</template>


<script setup lang="ts">
import {
    defineOptions,
    defineProps,
    ref,
    computed
} from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import axios from "axios";
import { AxiosResponse } from "axios";
import { ElMessage } from "element-plus";


defineOptions({
    name: "loginOrSignupDialog"
});

const props = defineProps({
    show: {
        // 是否显示本对话框
        type: Boolean,
        default: false
    },

    closeDialog: {
        // 关闭本对话框时所需显示的函数
        type: Function,
        required: true
    }
});

const store = useStore();
const router = useRouter();


const actionType = ref<"login" | "signup" | "verifyCode">("login");
// 当前对话框的功能

const prevActionType = ref<"login" | "signup">("login");
// 在用户想要执行当前操作之前 上一个用户想执行的操作是什么?

const email = ref<string>("");
// 用户邮箱

const password = ref<string>("");
// 用户密码

const username = ref<string>("");
// 用户名

const verifyCode = ref<string>("");
// 验证码

const gettedVerifyCode = ref<string>("");
// 从网络上获取到的验证码

const actionResult = ref<string | null>(null);
// 操作执行结果


const actionName = computed(function(): string {
    // 对话框右下角 "执行操作" 按钮所需显示的文字
    if (actionType.value === "login" || actionType.value === "signup") {
        return "发送验证码";
    }

    return "完成";
});


function clearState(): void {
    // 发现当 v-if=false 后 组件内的数据不会被清空
    // 于是在这里设置当用户想要隐藏对话框的时候清空组件内的 state

    email.value = "";
    password.value = "";
    username.value = "";
    verifyCode.value = "";

    actionType.value = "login";
    prevActionType.value = "login";
}

function sendVerifyCode(): void {
    // 发送验证码的函数

    axios
    .post("/api/sendVerifyCode", {
        email: email.value
    })
    .then((rep: AxiosResponse) => {
        if (rep.status !== 200 || !rep.data.code || rep.data.code !== 200) {
            throw rep;
        }

        gettedVerifyCode.value = rep.data.verifyCode;
    })
    .catch(rej => {
        console.log("请求失败:", rej);
        actionResult.value = "请求失败了, 请稍后再试";
    });
}

function loginOrSignup(): void {
    // 执行登录或注册操作的函数

    if (prevActionType.value === "signup") {
        // 执行注册

        ElMessage("正在注册");

        axios
        .post("/api/signup", {
            username: username.value,
            email: email.value,
            password: password.value,
            verifyCode: verifyCode.value
        })
        .then((rep: AxiosResponse) => {
            if (rep.status !== 200 || !rep.data.code) {
                throw rep;
            }

            const { data } = rep;

            if (data.reason === "wrong verifyCode") {
                actionResult.value = "验证码错误";
                return ;
            }

            if (data.reason === "duplicate name") {
                actionResult.value = "名字重复了 请换一个用户名";
                return ;
            }

            if (data.reason === "user already registered") {
                actionResult.value = "你已经注册过了 请去登录";
                return ;
            }

            ElMessage("注册成功  1s 后将自动跳转到登录页");

            setTimeout(() => {
                actionResult.value = null;
                actionType.value = "login";
            }, 1000);
        })
        .catch(rej => {
            ElMessage("请求错误 请稍后再试");
            console.log("请求失败: ", rej);
        });

        return ;
    }
    
    if (prevActionType.value === "login") {
        // 执行登录

        ElMessage("正在登录");
        
        axios
        .post("/api/login", {
            email: email.value,
            password: password.value,
            verifyCode: verifyCode.value
        })
        .then((rep: AxiosResponse) => {
            if (rep.status !== 200 || !rep.data.code) {
                throw rep;
            }

            const { data } = rep;

            if (data.reason === "user not found") {
                actionResult.value = "没有找到此用户 请注册";
                return ;
            }

            if (data.reason === "wrong password") {
                actionResult.value = "密码错误 请重试";
                return ;
            }

            if (data.reason === "wrong verifyCode") {
                actionResult.value = "验证码错误 请重试";
                return ;
            }

            ElMessage("登录成功  1s 后此对话框将自动取消显示");

            setTimeout(() => {
                actionResult.value = null;
                closeDialog();

                // 更新信息
                store.dispatch("fetchUserInfo");

                // 重定向到首页
                router.replace("/");
            }, 1000);
        })
        .catch(rej => {
            ElMessage("请求错误 请稍后再试");
            console.log("请求失败: ", rej);
        });

        return ;
    }
}

function onNextButtonClick(): void {
    // 当 "执行接下来的操作" 的按钮按下时会执行的回调

    const emailReg: RegExp = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    // 匹配邮箱的正则

    // 对数据进行校验
    if (email.value === "") {
        actionResult.value = "邮箱不能为空";
        return ;
    }

    if (password.value === "") {
        actionResult.value = "密码不能为空";
        return ;
    }

    if (emailReg.test(email.value) === false) {
        actionResult.value = "邮箱不符合格式";
        return ;
    }


    if (actionType.value === "login") {
        // 如果用户要登录的话

        actionResult.value = null;
        prevActionType.value = "login";
        actionType.value = "verifyCode";
        sendVerifyCode();

        // 清空用户输入的验证码
        verifyCode.value = "";
    } else if (actionType.value === "signup") {
        // 如果用户要注册的话

        if (username.value === "") {
            // 检查用户名是否为空
            actionResult.value = "用户名不能为空";
            return ;
        }

        actionResult.value = null;
        prevActionType.value = "signup";
        actionType.value = "verifyCode";
        sendVerifyCode();

        // 清空用户输入的验证码
        verifyCode.value = "";
    } 
    else {
        loginOrSignup();
    }
}

function closeDialog(): void {
    // "关闭对话框" 按钮按下时的回调

    clearState();
    // 清空状态

    actionResult.value = null;
    // 清空信息

    props.closeDialog();
    // 而后调用关闭对话框的函数
}
</script>


<style scoped lang="scss">
.loginOrSignupDialog {
    width: 100vw;
    height: 100vh;

    position: fixed;
    left: 0;
    top: 0;

    pointer-events: auto;

    z-index: 1000;

    .el-card {
        width: 600px;
        height: 400px;

        position: absolute;
        left: 50%;
        top: 30%;
        transform: translate(-50%, -30%);

        background-color: $backgroundColor;

        box-shadow: 0px 3px 40px 5px $backgroundDarkestColor;
        border: none;

        .loginOrSignupDialogBody {
            width: 100%;
            height: 100%;

            .titleBox {
                height: 20%;
                display: flex;
                flex-direction: row;
                justify-content: flex-start;
                align-items: flex-end;

                .el-text {
                    height: 100%;

                    align-self: flex-end;

                    display: flex;
                    flex-direction: row;
                    align-items: flex-end;


                    margin-left: 5%;
                    font-size: 22px;
                }

                .actionNameBox {
                    height: 32px;

                    margin-left: 5px;

                    flex-grow: 1;

                    position: relative;

                    overflow: hidden;

                    .actionName {
                        padding-top: 3px;
                        margin-left: 0px;

                        position: absolute;

                        font-size: 32px;
                        font-weight: bold;

                        color: $foregroundLightenColor;
                    }
                }
            }

            .formBox {
                width: 100%;
                height: 50%;

                flex-direction: column;
                justify-content: flex-start;
                align-items: center;
                flex-wrap: nowrap;

                position: absolute;

                .el-input, .el-text {
                    width: 90%;
                    margin: 10px 0;

                    --el-text-color-regular: #{ $fontDarkColor };

                    &:first-child {
                        margin-top: 20px;
                    }
                }

                .el-text {
                    --el-text-color-regular: #{ $fontColor };
                }

                .signup {
                    margin-left: 5%;
                    align-self: flex-start;
                }

                .actionInfo {
                    color: rgb(255, 61, 61);
                }
            }

            .actionBox {
                position: absolute;
                top: 70%;

                width: 100%;
                height: 30%;
                display: flex;
                flex-direction: row;
                justify-content: flex-end;
                align-items: center;

                .el-button {
                    margin-left: 0;
                    margin-right: 20px;

                    background-color: $actionColor;
                    border-color: $actionDarkenColor;
                    color: $fontColor;
                }
            }
        }
    }
}


.v-enter-active, .v-leave-active {
	transition: all 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.v-enter-active {
    left: -100%;
    opacity: 0;
}

.v-enter-to, .v-leave-active {
    left: 0;
    opacity: 100;
}

.v-leave-to {
    left: 100%;
    opacity: 0;
}


.actionNameTransition-enter-active, .actionNameTransition-leave-active {
    transition: all 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.actionNameTransition-enter-active {
    top: 100%;
}

.actionNameTransition-enter-to, .actionNameTransition-leave-active {
    top: 0;
}

.actionNameTransition-leave-to {
    top: -100%;
}


.dialogTransition-enter-active, .dialogTransition-leave-active {
    transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.dialogTransition-enter-active {
    opacity: 0;
}

.dialogTransition-enter-to, .dialogTransition-leave-active {
    opacity: 1;
}

.dialogTransition-leave-to {
    opacity: 0;
}
</style>
