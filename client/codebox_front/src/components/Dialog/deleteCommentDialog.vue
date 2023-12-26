<template>
    <div 
        class="deleteCommentDialogBox"
        :style="computedStyle"
    >
        <div class="deleteCommentDialog">
            <el-row>
                真的要删除这条评论吗?
            </el-row>
    
            <el-row>
                <el-button class="normal" @click="props.close">算了</el-button>
                <el-button type="primary" @click="props.next">删!</el-button>
            </el-row>
        </div>
    </div>
</template>


<script setup lang="ts">
import {
    defineOptions,
    defineProps,
    computed,
} from "vue";


defineOptions({
    name: "deleteCommentDialog"
});

const props = defineProps({
    x: {
        // 用户需要点击删除按钮才能触发此对话框
        // 此 props 就是删除按钮点击事件的 clientX
        type: Number,
        defualt: 0
    },

    y: {
        // 用户需要点击删除按钮才能触发此对话框
        // 此 props 就是删除按钮点击事件的 clientY
        type: Number,
        defualt: 0
    },

    next: {
        // 当对话框需要删除评论执行的函数
        type: Function,
        required: true
    },

    close: {
        // 当对话框关闭时需要执行的函数
        type: Function,
        required: true
    },
});

const computedStyle = computed(function() {
    // 动态 css 变量
    return {
        "--left": `${props.x}px`,
        "--top": `${props.y}px`
    };
});
</script>


<style lang="scss" scoped>
.deleteCommentDialogBox {
    position: fixed;
    left: 0;
    top: 0;

    width: 100vw;
    height: 100vh;

    z-index: 1000;

    .deleteCommentDialog {
        width: 200px;
        height: 100px;

        position: fixed;
        left: var(--left);
        top: var(--top);

        background-color: $backgroundDarkenColor;

        border-radius: 3px;
        box-shadow: 0px 1px 5px 2px $backgroundDarkestColor;

        .el-row:first-child {
            height: 60%;

            padding-left: 10px;
            padding-top: 10px;
        }

        .el-row:last-child {
            height: 40%;

            display: flex;
            flex-direction: row;
            justify-content: flex-end;
            align-items: center;

            .el-button {
                margin-left: 0;
                margin-right: 10px;
                margin-bottom: 5px;

                &.normal {
                    color: $foregroundColor;
                }
            }
        }
    }
}
</style>
