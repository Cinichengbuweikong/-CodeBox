<template>
    <div
        class="indexPage"
        @scroll="pageBoxScroll($event)()"
    >
        <el-container>
            <PageHeader />
            
            <el-main ref="mainRef" :style="calcStyle">
                <section class="intro introOne" ref="sectionRef">
                    <div class="imageBox">
                        <img src="../assets/imgs/code.jpg">
                        <div class="mask"></div>
                    </div>
                </section>

                <section class="intro introTwo">
                    <div class="imageBox">
                        <img src="../assets/imgs/online.jpg">
                        <div class="mask"></div>
                    </div>
                </section>

                <section class="intro introThree">
                    <div class="imageBox">
                        <img src="../assets/imgs/teamwork.jpg">
                        <div class="mask"></div>
                    </div>
                </section>

                <div class="sloganBox">
                    <h2 class="title">代码盒子·CodeBox</h2>
                    <p class="desc">
                        代码盒子是一个供前端开发者们在线分享自己代码的一个平台。
                    </p>
                </div>
            </el-main>

            <PageFooter />
        </el-container>
    </div>
</template>


<script lang="ts" setup>
import {
    ref,
    ComponentPublicInstance,
    defineOptions,
    computed
} from "vue";

import PageHeader from "../components/Header/pageHeader.vue";
import PageFooter from "../components/Footer/pageFooter.vue";


defineOptions({
    name: "IndexPage"
});


const mainRef = ref<ComponentPublicInstance | null>(null);
const sectionRef = ref<HTMLElement | null>(null);
const scrollPercent = ref<number>(0);
// 记录整个 el-main 已经滚动了百分之几的 ref


const calcStyle = computed(() => ({
    // 计算 css 样式
    "--imageBoxTop": `-${ (40 + 60 * (scrollPercent.value / 20)).toFixed(2) }px`,
}));


function pageBoxScroll(event: Event) {
    // 当 .indexPage 滚动时所执行的回调

    // 获取到单个 section 高度
    const sectionComputedHeight: string = 
        getComputedStyle((sectionRef.value as HTMLElement)).height;

    // 获取到整个 el-main 元素高度
    const mainComputedHeight: string = 
        getComputedStyle((mainRef.value!.$el as HTMLElement)).height;

    // 从获取到的高度中截取出高度的数字 而后将其转换为 number
    const sectionHeigth: number = 
        +sectionComputedHeight.substring(0, sectionComputedHeight.length - 2);

    const mainTotalHeigth: number = 
        +mainComputedHeight.substring(0, mainComputedHeight.length - 2);

    
    function calcScrollPercent(): number {
        // 计算当前整个 .el-main 滚动完成的百分比
        // 当用户没有滚动时 该函数返回 0
        // 当用户将整个 .el-main 滚动完成时 函数返回 100 而后继续滚动的话函数也只返回 100

        const percent: number = (
            ((event.target as HTMLElement).scrollTop)  // 用户还没滚动时 默认 scrollTop == 0
            /
            (mainTotalHeigth - sectionHeigth)  // 有 n 个 section  那当用户滚动到底的时候实际走了 n-1 个 section 的距离
        ) * 100;

        return percent < 0 ? 0 : percent > 100 ? 100 : percent;
        // 将百分比值限定在 0-100 之间
    }

    return () => {
        const immediateScrollPercent = calcScrollPercent();
        // 计算容器滚动百分比

        const data = getText(immediateScrollPercent);
        (document.querySelector(".sloganBox > .title") as HTMLElement).innerText = data.title;
        (document.querySelector(".sloganBox > .desc") as HTMLElement).innerText = data.desc;
        // 在此处调用函数 获取此时需要显示的标题和介绍

        scrollPercent.value = immediateScrollPercent;
        // 最后更新 scrollPercent 以实现视差效果
    };
}

function getText(immediateScrollPercent: number) {
    // 在滚动时调用 函数会返回在当前 el-main 元素的滚动进度下需要显示的标题和文字

    // immediateScrollPercent 即当前的 el-main 容器滚动百分比
    // 为什么不使用存储在 ref 中的 "scrollPercent"  因为实践发现 容器滚动百分比的计算是很快的
    // 但 ref 在快速存储数据的时候却表现出了 "防抖" 的特点
    // 很多时候(尤其是在快速滚动页面的时候) 其实容器的滚动百分比已经是 0 了 但由于 ref 存在 "防抖"
    // 很有可能最后的那个 0 数据就被 "抖" 掉了 导致容器滚动百分比已经是 0 了 但函数获取到的滚动百分比仍不是 0 从而导致获取不到正确的数据
    // 因此 为了解决这个问题 我决定不再使用 vue 提供的功能 而让此函数直接从计算容器滚动百分比的函数中获取数据
    // 这样一来问题就解决了

    // 同时 因为 ref 的 "防抖" 机制 在实现 "页面滚动时标题和文字会动态变化" 的这个效果的时候
    // 我决定不在使用 vue  而是直接操作 DOM
    // 虽然所有人都建议在使用了 vue 后不要再操作 DOM 了 但在这里 由于数据变化非常频繁
    // 而 vue 的 ref 由于其 "防抖" 效果反而在这个效果中成了累赘 因此我决定直接操作 DOM
    // 总之就是不要被框架束缚住手脚


    const states = {
        // 要在各个百分比下显示的标题和介绍
        // 0 表示标题和介绍要在滚动到 0% 的时候显示

        0: {
            title: "代码盒子·CodeBox",
            desc: "代码盒子是一个供前端开发者们在线分享自己代码的一个平台。"
        },

        50: {
            title: "在线运行，即刻得到效果",
            desc: "代码盒子支持在线运行 Vue 代码。开发者们无需将代码拷贝到本地，在线即可预览代码的效果。"
        },

        100: {
            title: "共同学习，共同进步",
            desc: "开发者们可以将自己做好的功能的代码分享到代码盒子上，想做其他功能时可以直接在代码盒子上搜索并复用别人写好的功能代码。让前端开发者们在学习和分享的过程中增进自己的知识，提高自己的能力！"
        }
    };

    function genText(
        fromPercent: number, 
        toPercent: number, 
        fromText: string, 
        toText: string, 
        currentPercent: number,
        title = false
    ): string {
        // 计算在当前滚动进度下需要显示的文字  "文字" 可以是标题或是介绍

        // 首先计算当前滚动进度已经滚动到当前区间的的百分之多少了
        // 就直接 (currentPercent - fromPercent) / (toPercent - fromPercent) 即可
        // 例如 对于 0-45 这个区间来说  el-main 滚动了 30 的时候就已经走完这个区间的 66.66% 了
        // const currentRangePercent = +(
        //     (currentPercent - fromPercent) / (toPercent - fromPercent)
        // ).toFixed(2);


        // 再计算整个区间内所有文字全部更改完毕需要分几步完成
        // 我们以 title 的长度为依据 评判规则如下:
        const fromPercentTitle = (states as any)[fromPercent].title;
        const toPercentTitle = (states as any)[toPercent].title;

        let step = 0;

        if (fromPercentTitle.length >= toPercentTitle.length) {
            
            // 如果 states[fromPercent].title.length >= states[toPercent].title.length
            // states[toPercent].title.length 就是区间内的文字需要分几步变完
            step = toPercentTitle.length;

            // 例如 fromTitle 是 "hijkl" toTitle 是 "abc"
            // 那每次文字需要变化的时候 就都删除 fromTitle 中的两个文字 而后把一个 toTitle 中的文字塞进去
            // 例如: hijkl - ajkl - abl - abc  也就是 4 步走完
        } else {
            // 如果 states[fromPercent].title.length < states[toPercent].title.length
            // states[fromPercent].title.length 
            // + celi(
            //     (states[toPercent].title.length - states[fromPercent].title.length) / 2
            // ) 就是区间内的文字需要分几步变完
            step = fromPercentTitle.length + Math.ceil(
                (toPercentTitle.length - fromPercentTitle.length) / 2
            );

            // 例如 fromTitle 是 "abc"  toTitle 是 "hijklm"
            // 那在开始的时候 我们每次都从 toTitle 中删除一个文字 而后多显示 fromTitle 中的一个问题
            // 当 fromTitle 中的所有文字都显示完成后 toTitle 中剩余的文字再两个两个显示到屏幕上
            // 例如: aijklm - abjklm - abcklm - abcm -abc  也就是 5 步走完
        }


        // 再计算当前 el-main 滚动到此处的时候 我们应该显示第几步的文字
        let currentStep = 0;

        // 先计算每一步需要占多少滚动百分比
        // 例如对于 0-45 这个滚动区间来说 如果要分 5 步的话 那每步占 9%
        const percentPerStep = (toPercent - fromPercent) / step;

        // 再计算 celi((currentPercent - fromPercent) / 每一步滚动百分比)  这就是现在应显示第几步的文字了
        currentStep = Math.ceil((currentPercent - fromPercent) / percentPerStep);


        // 再计算每一步我们需要更改多少文字
        let codePerChange = 0;
        
        if (!title) {
            // 对于介绍文字来说 计算方式很简单 只需要 celi(toText.length / 步数) 即可
            // 例如 对于 "abcd...xyz" 来说 假设一共 5 步完成此次变化 那每次就是改变 5 个文字
            
            codePerChange = Math.ceil(toText.length / step);
        } else {
            // 对于标题文字来说 我们需遵循如下规则:

            if (fromPercentTitle.length >= toPercentTitle.length) {
                // 如果 states[fromPercent].title.length >= states[toPercent].title.length
                // 则 step = 2  具体解释见 "计算整个区间内所有文字全部更改完毕需要分几步完成" 部分

                codePerChange = 2;
            } else {
                // 如果 states[fromPercent].title.length < states[toPercent].title.length
                // 在 toText 中的所有字符没有取完之前 setp=1
                // 在 toText 中的所有字符都取完之后 setp=2
                // 具体解释见 "计算整个区间内所有文字全部更改完毕需要分几步完成" 部分

                if (currentStep * 1 <= toText.length) {
                    // 每一步显示一个字符
                    codePerChange = 1;
                } else {
                    // 如果步数 > states[fromPercent].title.length 则表示文字都取完了
                    codePerChange = 2;
                }
            }
        }


        // 最后 尝试删除 fromText 中前 当前步数 * 每步改多少的文字 个数的字符
        // 注意 这里说的是 "尝试删除"  如果 (当前步数 * 每步改多少的文字) > fromText.length 的话 那就直接清空 fromText 即可
        // 而后把 toText 中前 当前步数 * 每步改多少的文字 个数的字符的文字拼接再字符串的起始位置即可
        const lastStr = fromText.substring(currentStep*codePerChange - 1);
        const firstStr = toText.substring(0, currentStep*codePerChange);
        const finalStr = `${firstStr}${lastStr}`;

        // 返回处理结果

        return finalStr;
    }

    // 根据不同的滚动进度传递不同的函数参数 以获取在此滚动进度下要显示的标题和文字
    if (immediateScrollPercent === 0) {
        return states[0];
    } else if (immediateScrollPercent > 0 && immediateScrollPercent <= 45) {
        // 为什么这里的判断条件不是严格的 0-50-100?
        // 因为很多时候用户并不能滚动到那么严格的区间内 这里让区间稍微偏移一点 给了用户随便滚动的空间

        const data = {
            title: genText(0, 50, states[0].title, states[50].title, immediateScrollPercent, true),
            desc: genText(0, 50, states[0].desc, states[50].desc, immediateScrollPercent)
        };

        return data;
    } else if (immediateScrollPercent > 45 && immediateScrollPercent <= 95) {
        const data = {
            title: genText(50, 100, states[50].title, states[100].title, immediateScrollPercent, true),
            desc: genText(50, 100, states[50].desc, states[100].desc, immediateScrollPercent),
        };

        return data;
    } else {
        return states[100];
    }
}
</script>


<style lang="scss" scoped>
.indexPage {
    width: 100%;
    height: 100%;
    overflow-y: scroll;

    .el-container {
        width: 100%;
        flex-direction: column;
        
        .el-main, .el-footer {
            padding-left: 0;
            padding-right: 0;
        }

        .el-main {
            width: 100%;
            padding: 0;
            margin-top: 60px;

            .intro {
                height: calc(100vh - 60px);

                position: relative;

                overflow: hidden;

                .imageBox {
                    width: 100%;

                    position: absolute;
                    left: 0;
                    // top: var(--imageBoxTop);

                    transform: translateY(var(--imageBoxTop)) scale(1.48);

                    .mask {
                        width: 100%;
                        height: 100%;

                        position: absolute;
                        left: 0;
                        top: 0;

                        background-color: rgba($color: black, $alpha: 0.1);
                    }

                    img {
                        width: 100%;
                    }
                }
            }

            .sloganBox {
                    position: fixed;
                    left: 5%;
                    top: 20%;

                    color: transparent;
                    text-shadow: 0px 0px 0px rgba($color: white, $alpha: 0.8);
                    
                    h2 {
                        font-size: 60px;
                    }

                    p {
                        font-size: 22px;
                    }
                }
        }
    }
}
</style>
