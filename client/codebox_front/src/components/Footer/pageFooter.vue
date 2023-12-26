<template>
    <el-footer>
        <el-row>
            <el-col :span="8">
                <div @click="routerToIndexPage">
                    <el-image :src="require('@/assets/imgs/largeicon.png')" />
                    <el-text>一个让前端开发者交流分享代码的地方</el-text>
                </div> 
            </el-col>

            <el-col :span="16">
                <div>
                    <el-text>其他链接</el-text>

                    <ul>
                        <li>
                            <el-link 
                                :underline="false"
                                @click="routerToAboutPage"
                            >
                                关于本站
                            </el-link>
                        </li>
                    </ul>
                </div>
            </el-col>
        </el-row>
    </el-footer>
</template>


<script lang="ts" setup>
import {
    defineOptions
} from "vue";

import { useRouter } from "vue-router";


defineOptions({
    name: "PageFooter"
});

const router = useRouter();

function routerToAboutPage(): void {
    // 导航到关于页
    router.push({
        path: "/about"
    });
}

function routerToIndexPage(): void {
    // 导航到首页
    router.push("/");
}
</script>


<style lang="scss" scoped>
.el-footer {
    height: 300px;

    background-color: rgb(30, 30, 30);


    .el-row {
        height: 100%;

        .el-col:nth-child(1) {
            height: 100%;

            div {
                padding-left: 20px;
                padding-top: 20px;

                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                align-items: flex-start;

                cursor: pointer;

                .el-image {
                    padding: 0;
                    width: 160px;
                }

                .el-text {
                    align-self: flex-start;
                    font-size: 18px;
                    padding-top: 5px;
                }
            }
        }

        .el-col:nth-child(2) {
            display: flex;
            flex-direction: row;

            div {
                margin: 20px 20px 0;

                .el-text {
                    font-size: 18px;
                }

                ul {
                    list-style: none;
                }
            }
        }
    }
}
</style>
