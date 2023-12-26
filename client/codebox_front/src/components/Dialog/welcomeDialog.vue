<template>
    <transition name="dialogTransition">
        <div 
            class="welcomeDialog"
            v-if="props.show"
        >
            <el-card
                class="dialog"
                :body-style="{width: '100%', height: '100%', padding: '0px'}"
                shadow="never"
            >
                <div
                    class="loginOrSignupDialogBody"
                >
                    <div class="intro">
                        <el-text class="title">感谢你能访问本网站，请在电脑端访问本网站！</el-text>
                        <el-text class="desc">如果你比较累，可以直接点击: <el-link @click="routeToAbout">这个链接</el-link> <br/> 里面有网站的概要介绍和视频形式的整个网站的效果演示。</el-text>
                    </div>

                    <div class="action">
                        <el-button type="primary" @click="props.closeDialog">好的</el-button>
                    </div>
                </div>
            </el-card>
        </div>
    </transition>
</template>


<script setup lang="ts">
import {
    defineOptions,
    defineProps,
} from "vue";
import { useRouter } from "vue-router"; 


defineOptions({
    name: "welcomeDialog"
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

const router = useRouter();


function routeToAbout() {
    // 导航至关于页
    router.push("/about");
}
</script>


<style scoped lang="scss">
.welcomeDialog {
    width: 100vw;
    height: 100vh;

    position: fixed;
    left: 0;
    top: 0;

    pointer-events: auto;

    z-index: 1000;

    .el-card {
        width: 500px;
        height: 200px;

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

            display: flex;
            flex-direction: column;

            .intro {
                height: 70%;

                display: flex;
                flex-direction: column;
                
                .el-text {
                    align-self: flex-start;

                    margin-top: 20px;
                    margin-left: 20px;

                    &.title {
                        font-size: 22px;
                        font-weight: bold;
                    }

                    &.desc {
                        font-size: 18px;

                        .el-link {
                            font-size: 18px;
                            margin-top: -4px;
                        }
                    }
                }
            }

            .action {
                display: flex;
                flex-direction: row;
                justify-content: flex-end;

                .el-button {
                    margin-right: 20px;
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
