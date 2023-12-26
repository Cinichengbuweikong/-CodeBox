<template>
    <div class="userProjects">
        <div
            class="itemBox"
            @click="createNewProject"
        >
            <el-card
                class="newProjectCard"
                :body-style="{width: '100%', height: '100%', padding: '0px'}"
                shadow="never"
            >
                <div class="newProject">
                    <el-text>+</el-text>
                    <el-text>新建项目</el-text>
                </div>
            </el-card>
        </div>
        
        <div 
            class="itemBox"
            v-for="proj in data"
            :key="proj.pid"
        >
            <ItemCard
                :pid="+proj.pid"
                :projectname="proj.projectname"
                :description="proj.description"
                :effectimg="proj.effectimg"
            />
        </div>
    </div>
</template>


<script setup lang="ts">
import {
    defineOptions,
    defineProps,
    ref,
    onMounted
} from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { nanoid } from "nanoid";

import ItemCard from "../Search/itemCard.vue";
import { Project } from "@/types";


defineOptions({
    name: "userProjects"
});

const props = defineProps({
    uid: {
        // 要显示那个 uid 用户的项目?
        type: String,
        required: true
    }
});

const router = useRouter();


const data = ref<Array<Project>>([]);


async function fetchProjectData() {
    // 获取网络上的最新的用户项目数据

    const rep = await axios.get("/api/user/projects", {
        params: {
            uid: props.uid
        }
    });

    if (rep.status !== 200 || !rep.data) {
        console.log("个人项目数据获取失败了: ", rep);
        return ;
    }

    data.value = rep.data;
}

async function createNewProject() {
    // 创建新项目
    
    try {
        const rep = await axios.patch("/api/user/projects", {
            projectname: `新项目: ${nanoid()}`
        });

        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            throw rep;
        }

        // 创建成功后就跳转到项目页
        router.push({
            path: `/projects/${rep.data.pid}`
        });
    } catch(e) {
        console.log("新项目创建失败: ", e);
    }
}


onMounted(async () => {
    await fetchProjectData();
});
</script>


<style scoped lang="scss">
.userProjects {
    width: 80%;
    min-height: 400px;
    padding-bottom: 40px;
    
    margin: auto;

    // display: grid;
    // grid-template-columns: repeat(3, auto);
    // justify-items: center;
    // align-items: center;
    // justify-content: start;
    // align-content: start;

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
                box-shadow: 0px 3px 20px 3px $actionColor;
            }
        }
    }
}
</style>
