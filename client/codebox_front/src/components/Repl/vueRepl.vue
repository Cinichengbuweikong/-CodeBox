<template>
    <el-row class="replBox">
        <Repl 
            :editor="CodeMirror"
            :showImportMap="false"
            :showTsConfig="false"
            :store="replStore"
        />
    </el-row>
</template>


<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { Repl, ReplStore, File } from "@vue/repl";
import CodeMirror from "@vue/repl/codemirror-editor";
import axios from "axios";
import { ElMessage } from "element-plus";

import eventSub from "@/utils/eventSub";
import { BaseCodeInfo, CodeInfo } from "@/types";


class CustomReplStore extends ReplStore {
    // 继承 Repl 的 ReplStore 对象 重写其中的方法

    // 重写 addFile 方法 在其中同服务器进行交互
    addFile(fileOrFilename: string | File): void {
        if (typeof fileOrFilename === "string") {
            const fname = fileOrFilename.replace(/^src\//, '');

            // 在服务端添加文件
            ElMessage("正在同步信息");
            serverAddFile(fname);
        }

        super.addFile(fileOrFilename);
    }

    // 重写 deleteFile 方法 在删除文件的时候同服务器进行交互
    deleteFile(filename: string) {
        const fname = filename.replace(/^src\//, '');

        if ( confirm(`你确定要删除 ${fname} 吗?`) ) {
            if (this.state.activeFile.filename === filename) {
                this.state.activeFile = this.state.files[this.state.mainFile]
            }
            
            delete this.state.files[filename];

            // 在服务端删除文件
            ElMessage("正在同步信息");
            serverDeleteFile(fname);
        }
    }
}


const replStore = new CustomReplStore({
    defaultVueRuntimeURL: "/assets/serverStatics/scripts/runtime-dom.esm-browser-3.3.11.js",
    defaultVueRuntimeProdURL: "/assets/serverStatics/scripts/runtime-dom.esm-browser.prod-3.3.11.js",
    defaultVueServerRendererURL: "/assets/serverStatics/scripts/server-renderer.esm-browser-3.3.11.js"
});
const route = useRoute();

const code = ref<CodeInfo>({});
// 保存代码信息的 ref

const updateCodeInfoTimer = ref<number | null>(null);
// 更新代码信息的计时器  当代码修改请求完成后我们不能立即请求服务器给我们新代码信息
// 因为此时服务器还没能将数据存储到服务器中(服务端异步存储数据)
// 因此 我们需要在请求完成后等一小会 等服务端将数据存储完成 而后再请求代码信息
// 这个 timer 就是 "等一小会" 的计时器的 timer


async function getProjectCode(): Promise<void> {
    // 获取当前项目的代码

    try {
        // 先获取代码信息
        const codeInfoRep = await axios.get(`/api/projects/${route.params.pid}/code/`);

        if (codeInfoRep.status !== 200 || !codeInfoRep.data) {
            throw codeInfoRep;
        }

        const baseCodeInfo: BaseCodeInfo = codeInfoRep.data;
        const codeInfo: CodeInfo = {};

        // 再根据代码信息获取代码内容
        for (const cid in baseCodeInfo) {
            const codeRep = await axios.get(`/api/projects/${route.params.pid}/code/${cid}`);

            if (codeRep.status !== 200 || !codeRep.data) {
                throw codeRep;
            }

            codeInfo[cid] = {
                ...baseCodeInfo[cid],
                cid,
                code: codeRep.data.content,
            };
        }

        code.value = codeInfo;
    } catch(e) {
        ElMessage("获取代码信息失败");
        console.log("获取项目代码信息失败", e);
    }
}

function initCode(): void {
    // 将从网络上获取到的数据都放进 Repl 中

    // 先将 repl 中的代码文件全部删除
    for (const key in replStore.state.files) {
        if (key === "src/App.vue") {
            continue;
        }

        delete replStore.state.files[key];
    }

    // 而后将从网络上获取到的代码信息放在 repl 中
    for (const cid in code.value) {
        const c = code.value[cid];

        const filename = `${c.name}.${c.type}`;

        if (filename === "App.vue") {
            // 对于 App.vue 我们只需更改其中的内容即可
            replStore.state.files["src/App.vue"].code = c.code;
            continue;
        }

        // 对于其他情况 我们需要新建 File 对象 然后把它添加到 repl 中即可
        const f = new File(`src/${c.name}.${c.type}`, c.code);
        replStore.addFile(f);
    }

    // 最后设置被激活的组件为 App.vue
    replStore.setActive("src/App.vue");
}

function serverAddFile(fname: string) {
    // 向服务端发消息 新建文件

    // 先进行一些检查 并获取到要新建的文件名
    let [filename, filetype] = (fname as string).split(".");

    filetype = filetype.toLowerCase();

    if (filetype !== "vue" && filetype !== "js") {
        return;
    }

    // 和服务器沟通 新建文件
    axios.post(`/api/projects/${route.params.pid}/code/`, {
        name: filename,
        type: filetype
    })
    .then(rep => {
        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            throw rep;
        }
    })
    .catch(err => {
        ElMessage("在服务端新建文件失败");
        console.log("在服务器端新建文件失败了: ", err);
    });

    // 刷新代码信息
    if (updateCodeInfoTimer.value !== null) {
        clearTimeout(updateCodeInfoTimer.value);
    }

    updateCodeInfoTimer.value = setTimeout(() => {
        // 定时 在 1s 后再更新代码信息
        getProjectCode()
        .then(() => {
            ElMessage("同步完成");
        })
        .catch(err => {
            ElMessage("代码刷新失败");
            console.log("刷新代码失败了: ", err);
        });
    }, 1000);
}

function serverDeleteFile(fname: string) {
    // 从服务端删除代码文件

    // 首先寻找需要被删除的代码文件的 cid
    const filename = fname.split(".")[0];
    let cid = "";

    for (const _cid in code.value) {
        if (code.value[_cid].name === filename) {
            cid = _cid;
            break;
        }
    }

    if (cid === "") {
        console.log("删除代码时未找到指定名字的组件的 id: ", fname);

        return true;
    }

    // 而后删除项目
    axios.delete(`/api/projects/${route.params.pid}/code/${cid}`)
    .then(rep => {
        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            throw rep;
        }
    })
    .catch(err => {
        ElMessage("在服务端删除代码时失败了");
        console.log("在服务器端删除文件失败了: ", err);
    });

    // 刷新代码信息
    if (updateCodeInfoTimer.value !== null) {
        clearTimeout(updateCodeInfoTimer.value);
    }

    updateCodeInfoTimer.value = setTimeout(() => {
        // 定时 在 1s 后再更新代码信息
        getProjectCode()
        .then(() => {
            ElMessage("同步完成");
        })
        .catch(err => {
            ElMessage("代码刷新失败");
            console.log("刷新代码失败了: ", err);
        });
    }, 1000);
}

async function saveChanges(): Promise<void> {
    // 在服务器中保存用户对代码做的修改

    ElMessage("正在保存代码");

    for (const _cid in code.value) {
        const {name, type} = code.value[_cid];

        const codestr = replStore.state.files[`src/${name}.${type}`].code;

        const rep = await axios.patch(`/api/projects/${route.params.pid}/code/${_cid}`, {
            content: codestr
        });

        if (rep.status !== 200 || !rep.data || rep.data.code !== 200) {
            ElMessage("保存代码时出错");

            console.log("保存代码时出错了: ", rep);
        }
    }

    ElMessage("代码保存完成");
}


onMounted(async () => {
    ElMessage("正在获取最新代码 请等待...");

    // 获取代码
    await getProjectCode();

    // 初始化代码
    initCode();

    ElMessage("代码获取完成 现在可以继续了");

    // 注册事件
    // 保存代码事件 这个事件将由 projectPage 触发
    // 注册事件之前先取消注册事件
    try {
        eventSub.off("saveChanges");
    } catch {}
    // 而后再注册事件
    eventSub.on("saveChanges", saveChanges);
});
</script>


<style lang="scss" scoped>
.replBox {
    width: 100%;
    height: 100vh;

    .vue-repl {
        width: 100%;
        height: 100%;

        --bg: #1a1a1a;
        --bg-soft: #242424;
        --border: #383838;
        --text-light: #aaa;
        --color-branding: #42d392;
        --color-branding-dark: #89ddff;

        :deep(.import-map-wrapper) {
            background: linear-gradient( 90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0) 25% );
        }

        :deep(.CodeMirror) {
            // 设置 codeMirror 的主题

            --symbols: #e0e0e0;
            color: var(--symbols);
            --base: #8684bc;
            --comment: hsl(212, 16%, 49%);
            --keyword: #e07ae2;
            --variable: var(--base);
            --function: #ed792b;
            --string: #2ba46d;
            --number: #e87c33;
            --tags: #348ada;
            --brackets: var(--comment);
            --qualifier: #ff6032;
            --important: var(--string);
            --attribute: #c080eb;
            --property: #86abe5;
            --selected-bg: #656080;
            --selected-bg-non-focus: #6a6969;
            --cursor: #eee;
        }
    }
}
</style>