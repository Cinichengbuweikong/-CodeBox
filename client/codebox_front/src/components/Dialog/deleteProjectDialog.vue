<template>
    <div 
        class="deleteProjectDialogBox"
    >
        <div class="deleteProjectDialog">
            <el-row>
                <el-text>真的要删除此项目吗?</el-text>
                <el-text>请确认</el-text>
            </el-row>
    
            <el-row>
                <el-button class="cancel" @click="props.cancel">算了</el-button>
                <el-button type="primary" @click="props.next">删!</el-button>
            </el-row>
        </div>
    </div>
</template>


<script setup lang="ts">
import {
    defineOptions,
    defineProps,
} from "vue";


defineOptions({
    name: "deleteProjectDialog"
});

const props = defineProps({
    cancel: {
        // 当对话框取消按钮按下时需要执行的函数
        type: Function,
        required: true
    },

    next: {
        // 当对话框删除按钮按下时需要执行的函数
        type: Function,
        required: true
    }
});
</script>


<style lang="scss" scoped>
.deleteProjectDialogBox {
    position: fixed;
    left: 0;
    top: 0;

    width: 100vw;
    height: 100vh;

    z-index: 1000;

    .deleteProjectDialog {
        width: 260px;
        height: 160px;

        position: fixed;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);

        background-color: $backgroundColor;

        border-radius: 3px;
        box-shadow: 0px 1px 5px 2px $backgroundDarkenColor;

        .el-row:first-child {
            height: 60%;

            padding-left: 20px;
            padding-right: 20px;
            padding-top: 20px;

            .el-text:first-child {
                font-size: 20px;
                font-weight: bold;
            }
        }

        .el-row:last-child {
            height: 40%;

            display: flex;
            flex-direction: row;
            justify-content: flex-end;
            align-items: center;

            .el-button {
                margin-left: 0;
                margin-right: 20px;
                margin-bottom: 20px;

                &.cancel {
                    --el-text-color-regular: #{ $foregroundColor };
                }
            }
        }
    }
}
</style>
