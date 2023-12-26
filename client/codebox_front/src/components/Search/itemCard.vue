<template>
    <el-card 
        class="itemCard"
        :class="cardClassList"
        :body-style="{width: '100%', height: '100%', padding: '0px'}"
        shadow="never"
        @mouseenter="mouseEnterCard"
        @mouseleave="mouseLeaveCard"
        @click="routerToProjectPage"
    >
        <el-image :src="`/assets/effects/${props.effectimg}`" fit="cover" />

        <div>
            <el-text>{{props.projectname}}</el-text>
            <el-text>{{props.description}}</el-text>
        </div>
    </el-card>
</template>


<script lang="ts" setup>
import {
    defineOptions,
    defineProps,
    ref
} from "vue";

import {
    useRouter
} from "vue-router";


defineOptions({
    name: "itemCard"
});

const props = defineProps({
    propsClass: {
        type: Array,
        default: () => []
    },

    pid: {
        // 项目 id
        type: Number,
        required: true
    },

    projectname: {
        // 项目名
        type: String,
        required: true
    },

    description: {
        // 项目介绍
        type: String,
        required: true
    },

    effectimg: {
        // 项目效果图文件名
        type: String,
        required: true
    },

    temp: {
        // 项目是否是临时项目
        type: Boolean,
        default: false
    }
});

const router = useRouter();

const mouseEnterTimer = ref<number | null>(null);
// 当鼠标 hover 卡片的时候 我开启的定时器的 id

const cardClassList = ref<Array<string>>([ ...(props.propsClass as Array<string>) ]);
// 需要动态为卡片添加的类的列表

function mouseEnterCard() {
    // 当鼠标 hover 卡片的时候 我们需要启动一个定时器
    // 定时器时间到后我们需要为卡片添加一个类

    if (mouseEnterTimer.value != null) {
        return ;
    }

    mouseEnterTimer.value = setTimeout(() => {
        cardClassList.value.push("preview");
    }, 500);
}

function mouseLeaveCard() {
    // 当鼠标离开卡片后 我们需要删除定时器

    if (mouseEnterTimer.value == null) {
        return ;
    }

    clearTimeout(mouseEnterTimer.value);
    mouseEnterTimer.value = null;

    cardClassList.value = [];
}

function routerToProjectPage() {
    // 当点击卡片后 需要跳转到卡片表示的页面处

    router.push({
        path:  props.temp ? `/projects/temp/${props.pid}` : `/projects/${props.pid}`
    });
}
</script>


<style lang="scss" scoped>
.el-card {
    width: 100%;
    height: 100%;

    box-shadow: none;

    position: relative;

    z-index: 0;

    transition: all 0.3s ease;

    background-color: $backgroundDarkenColor;

    border: 0;

    .el-image {
        position: absolute;
        left: 0;
        top: 0;

        width: 100%;
        height: 60%;

        transition: all 0.3s ease;
    }

    div {
        position: absolute;
        left: 0;
        top: 60%;

        width: 100%;
        height: 40%;

        display: flex;
        flex-direction: column;
        justify-content: flex-start;

        transition: all 0.3s ease;
        
        .el-text {
            display: block;
            width: 90%;

            align-self: flex-start;
            padding-left: 10px;
            padding-top: 10px;

            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;

            &:first-child {
                font-size: 22px;
                font-weight: bold;
            }
        }
    }

    &:hover {
        cursor: pointer;

        box-shadow: 0px 3px 20px 5px $backgroundDarkenColor;

        z-index: 1000;

        &.preview {
            width: 150%;
            height: 110%;

            box-shadow: 0px 3px 30px 15px $backgroundDarkenColor;

            .el-image {
                left: 0;
                top: 0;

                width: 60%;
                height: 100%;
            }

            div {
                left: 60%;
                top: 0;

                width: 40%;
                height: 100%;
            }
        }
    }
}
</style>