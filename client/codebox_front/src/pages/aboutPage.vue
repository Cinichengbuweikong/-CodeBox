<template>
    <div class="aboutPage">
        <el-container>
            <PageHeader />
            
            <el-main>
                <el-row>
                    <el-text class="title">感谢你能访问本网站!</el-text>

                    <el-text>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        这个网站是我为了找工作所做的一个 demo 网站。如果你能看到这里，说明你还对本项目还挺感兴趣的。
                        谢谢你，不管你觉得我做的这个项目是否简陋，我是否能胜任你们的工作，我都很感谢你能访问我的网站。
                    </el-text>

                    <el-text>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        说实话，这个网站其实算不上是一个较大型的项目，虽然本网站写的口号挺响亮，但实际整个网站的页面只有那么几个。
                        本网站的前端和后端开发只用了 1 个月的时间，虽然这个项目的亮点确实不多
                        （我认为本项目唯数不多的优点就是动画还不错，而后就是很简洁，至少我自己是有想使用这个网站的欲望的！）
                        但好在本项目是一个全栈项目（虽然前后端都很简单就是了），而且这个项目全程是我自己想自己做的！没有参考别人！（功能设计上参考了 CodePen 这个网站，在此表示感谢。）
                    </el-text>

                    <el-text>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        说一下这个项目使用的技术栈吧！前端用的就是 Vue 3 全家桶了（Vue3、Vuex、VueRouter、ElementPlus）
                        后端用的是 Python + FastAPI，使用了 Docker 做容器化部署，同时使用 Redis 做了缓存，数据库用的是 MySQL。
                        我用了一个月多一点的时间来完成这个项目，其实本来还想做个后台页面的，但奈何时间不够了，我该找工作了，于是就作罢了。
                        后端接口的开发大概用了 10 天的时间，使用 RESTFul 风格设计的后端 API，剩余的时间都用来开发前台了。
                    </el-text>

                    <el-text>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        本项目使用 1 个月就完成了，时间确实是很仓促了，但 “要做个项目” 这件事并不是只准备了一个月的时间。
                        在这个项目之前我其实还做了另一个项目，是一个 “在线的可视化的快速的页面布局工具”，只可惜它烂尾了。
                        我发现我实际做出来的东西和我想要的东西不一样，并且即使我把它做出来了，我也不喜欢使用它。
                        那对于一个工具来说，如果一个创造它的人他都不喜欢使用这个工具的话，那这个工具的意义在哪里呢？故而我停止了那个项目的开发。
                        而此时那个项目已经花掉我 2 个月的时间了。如果你想看看那个项目，可见链接：<el-link>填写链接</el-link>
                    </el-text>

                    <el-text>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        最后，感谢你能来到这里！谢谢！
                        下面还有整个项目的演示视频，包含了整个项目的演示视频（包括你可能没注意到的细节部分）你可以去看看它。它不长，不会花费很多时间。
                    </el-text>

                    <el-text>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        本项目在 github 上开源，链接：<el-link>填写链接</el-link>
                    </el-text>
                </el-row>

                <el-row>
                    <el-text class="title">项目演示</el-text>
                    <div>
                        <video src="/assets/serverStatics/descVideo/desc.mp4" type="video/mp4" controls preload="auto"></video>
                    </div>
                </el-row>
            </el-main>
            
            <PageFooter />
        </el-container>
    </div>
</template>


<script lang="ts" setup>
import {
    defineOptions
} from "vue";

import PageHeader from "@/components/Header/pageHeader.vue";
import PageFooter from "@/components/Footer/pageFooter.vue";


defineOptions({
    name: "aboutPage",
});
</script>


<style lang="scss" scoped>
.aboutPage {
    width: 100vw;
    height: 100vh;

    overflow-y: scroll;

    .el-container {
        width: 100%;

        flex-direction: column;

        .el-main {
            width: 100%;

            margin: 60px 0;
            padding: 0;

            .el-row {
                width: 100%;

                &:last-child {
                    flex-direction: column;
                    align-items: flex-start;

                    div {
                        height: 300px;
                        aspect-ratio: 16/9;
                        margin-left: 10%;
                    }
                }
            }

            .el-text {
                display: block;
                width: 80%;

                margin: 20px auto;

                font-size: 20px;

                word-wrap: break-word;
                word-break: normal;
            }

            .el-link {
                font-size: 20px;
                margin-top: -4px;
            }

            .title {
                font-size: 44px;
                font-weight: bold;

                margin-top: 40px;
            }

            video {
                width: 500px;
            }
        }
    }
}
</style>
