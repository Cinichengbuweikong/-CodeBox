<template>
    <div class="searchPage">
        <el-container>
            <PageHeader />

            <el-main>
                <el-row class="searchTitle">
                    <el-col :span="18" :offset="3">
                        <el-text>搜索 "{{ route.query.q }}" 的结果</el-text>
                    </el-col>
                </el-row>

                <el-row class="searchResults">
                    <el-col :span="18" :offset="3">
                        <div class="searching" v-if="fetchingData">
                            <el-text>正在搜索...</el-text>
                        </div>

                        <div v-if="!fetchingData && data !== null && data.length === 0">
                            <el-text>没有搜索到内容</el-text>
                        </div>

                        <div
                            v-if="!fetchingData && data !== null"
                        >
                            <div 
                                class="itemContainer"
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
                    </el-col>
                </el-row>

                <el-row class="paginatorRow" v-if="!fetchingData">
                    <el-col :span="18" :offset="3">
                        <el-pagination 
                            background
                            layout="prev, pager, next"
                            :page-size="perpage"
                            :total="totalDataNum"
                            :prev-click="prevPage"
                            :next-click="nextPage"
                        />
                    </el-col>
                </el-row>
            </el-main>
            
            <PageFooter/>
        </el-container>
  </div>
</template>


<script lang="ts" setup>
import {
    defineOptions,
    computed,
    ref,
    onMounted
}  from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

import PageHeader from '@/components/Header/pageHeader.vue';
import PageFooter from "@/components/Footer/pageFooter.vue";
import ItemCard from "@/components/Search/itemCard.vue";
import { Project } from "@/types";


defineOptions({
    name: "searchPage",
});

const route = useRoute();


const data = ref<Array<Project> | null>(null);
// 查询出的项目数据

const fetchingData = ref<boolean>(true);
// 现在是否在从网络上查询数据?

const totalDataNum = ref<number>(0);
// 符合搜索条件的数据总共有多少?

const perpage = ref<number>(6);
// 一页有多少数据?

const page = ref<number>(1);
// 现在是在第几页?


async function search(): Promise<void> {
    // 根据关键字搜索数据

    fetchingData.value = true;

    try {
        const rep = await axios.get("/api/projects/", {
            params: {
                q: route.query.q,
                page: page.value
            }
        });

        if (rep.status !== 200 || !rep.data) {
            throw rep;
        }

        totalDataNum.value = rep.data.total;
        perpage.value = rep.data.perpage;
        page.value = rep.data.page;
        data.value = rep.data.data;

        // 更改搜索状态
        fetchingData.value = false;
    } catch(e) {
        console.log("搜索时出错: ", e);
    }
}

async function nextPage(): Promise<void> {
    // 切换下一页所需执行的函数
    
    if (page.value < Math.ceil(totalDataNum.value / perpage.value)) {
        page.value += 1;
        await search();
    }
}

async function prevPage(): Promise<void> {
    // 切换上一页所需执行的函数

    if (page.value > 1) {
        page.value -= 1;
        await search();
    }
}


onMounted(async () => {
    await search();
});
</script>


<style lang="scss" scoped>
.searchPage {
    height: 100%;
    overflow-y: scroll;

    .el-container {
        flex-direction: column;

        .el-main {
            padding: 0;
            margin-top: 60px;
            padding-bottom: 60px;
            min-height: calc(100vh - 60px - 300px);

            .searchTitle {
                height: 150px;

                .el-col {
                    display: flex;
                    flex-direction: column;
                    justify-content: flex-end;

                    padding: 0 3%;

                    .el-text {
                        align-self: flex-start;

                        font-size: 44px;
                        font-weight: bold;
                        margin-bottom: 40px;
                    }
                }

            }
        }

        .searchResults {
            .el-col {
                padding: 0 3%;

                position: relative;

                .searching {
                    .el-text {
                        font-size: 22px;
                    }
                }

                & > div {
                    display: flex;
                    flex-direction: row;
                    justify-content: flex-start;
                    flex-wrap: wrap;

                    .itemContainer {
                        width: 300px;
                        height: 225px;

                        margin-top: 20px;
                        margin-bottom: 20px;
                        margin-right: calc(calc(100% - 900px) / 3);
                        // 100% - 3个盒子的宽度 再除以 3 份 就是每个盒子的 margin-right
                    }

                    .gap {
                        margin-right: auto;
                    }
                }
            }
        }

        .paginatorRow {
            margin-top: 20px;
            
            .el-col {
                padding: 0 3%;
            }
        }
    }
}
</style>
