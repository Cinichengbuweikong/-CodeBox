<template>
    <div class="userProjects">

        <div 
            class="emptyStarTip"
            v-if="data.length === 0"
        >
            <el-text>用户还没有收藏哦!</el-text>
        </div>
        
        <div 
            class="itemBox"
            v-else

            v-for="p in data"
            :key="p.pid"
        >
            <ItemCard
                :pid="+p.pid"
                :projectname="p.projectname"
                :description="p.description"
                :effectimg="p.effectimg"
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
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

import ItemCard from "../Search/itemCard.vue";
import { Project } from "@/types"; 


defineOptions({
    name: "userProjects"
});

const route = useRoute();
const router = useRouter();

const data = ref<Array<Project>>([]);


async function fetchStarData() {
    // 获取用户收藏信息

    try {
        const rep = await axios.get("/api/user/stars");
    
        if (rep.status !== 200 || !rep.data) {
            throw rep;
        }
        
        data.value = rep.data;
    } catch(e) {
        console.log("个人收藏数据获取失败了: ", e);
    }
}


onMounted(async () => {
    await fetchStarData();
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

    .emptyStarTip {
        width: 100%;
        height: 100%;

        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;

        .el-text {
            align-self: flex-start;

            font-size: 18px;
            margin-top: 10px;
        }
    }

    .itemBox {
        width: 270px;
        height: 180px;

        margin-top: 20px;
        margin-left: 9px;
        margin-right: 9px;

        overflow: visible;

        position: relative;

        .newProjectCard {
            width: 100%;
            height: 100%;
            transition: all 0.3s ease;
            cursor: pointer;

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
                box-shadow: 0px 3px 20px 5px #cacaca;
            }
        }
    }
}
</style>
