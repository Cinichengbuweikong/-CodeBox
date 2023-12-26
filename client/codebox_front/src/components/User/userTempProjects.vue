<template>
    <div class="userProjects">
        <div
            class="itemBox"
        >
            <el-card
                class="newProjectCard"
                :body-style="{width: '100%', height: '100%', padding: '0px'}"
                shadow="never"
            >
                <div class="newProject" @click="createNewTempProject">
                    <el-text>+</el-text>
                    <el-text>新建项目</el-text>
                </div>
            </el-card>
        </div>
        
        <div 
            class="itemBox"
            v-for="proj in data"
            :key="proj.tpid"
        >
            <ItemCard
                :pid="+proj.tpid"
                :projectname="proj.name"
                :description="'临时项目'"
                :effectimg="'default.jpg'"
                :temp="true"
            />
        </div>
    </div>
</template>


<script setup lang="ts">
import {
    defineOptions,
    ref,
    onMounted
} from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

import ItemCard from "../Search/itemCard.vue";
import { TempProject } from "@/types";


defineOptions({
    name: "userProjects"
});

const router = useRouter();


const data = ref<Array<TempProject>>([]);
// 存储临时项目信息的 ref


async function fetchProjectData() { 
    // 从网络上获取临时项目信息

    try {
        const rep = await axios.get("/api/projects/temporaryproject");

        if (rep.status !== 200 || !rep.data || (rep.data.code && rep.data.code !== 200)) {
            throw rep;
        }

        data.value = rep.data;
    } catch(e) {
        console.log("个人临时项目数据获取失败了: ", e);
    }
}

async function createNewTempProject() {
    // 创建新临时项目
    
    try {
        const rep = await axios.post("/api/projects/temporaryproject");

        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            throw rep;
        }

        // 创建成功后就跳转到项目页
        router.push({
            path: `/projects/temp/${rep.data.tpid}`,
        });
    } catch(e) {
        console.log("新项目创建失败: ", e);
    }
}


onMounted(async () => {
    // 页面挂载后获取临时项目信息
    await fetchProjectData();
});
</script>


<style scoped lang="scss">
.userProjects {
    width: 80%;
    min-height: 400px;
    padding-bottom: 40px;
    
    margin: auto;

    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    flex-wrap: wrap;

    position: relative;

    .itemBox {
        width: 270px;
        height: 180px;

        margin-top: 20px;
        margin-left: 9px;
        margin-right: 9px;

        overflow: visible;

        .newProjectCard {
            width: 100%;
            height: 100%;
            transition: all 0.3s ease;
            cursor: pointer;

            background-color: $backgroundDarkenColor;
            border: 0;

            .newProject {
                width: 100%;
                height: 100%;

                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;

                .el-text:first-child {
                    font-size: 40px;
                }
            }

            &:hover {
                box-shadow: 0px 3px 20px 3px $foregroundColor;
            }
        }
    }
}
</style>
