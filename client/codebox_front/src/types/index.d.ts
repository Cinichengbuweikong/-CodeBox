export interface UserInfo {
    // 用户信息定义

    uid: string,  // 当前登录用户的 uid
    username: string,  // 用户名
    avatarurl: string,  // 用户头像地址
    coin: string,  // 用户的硬币数
    description: string,  // 用户自我介绍
    email: string,  // 用户的邮箱
}

export interface Project {
    // 项目对象定义
    
    pid: string,  // 项目 id
    uid: string,  // 项目所属用户 id
    projectname: string,  // 项目名
    description: string,  // 项目介绍
    effectimg: string  // 效果图文件名
}

export interface TempProject {
    // 临时项目对象定义

    tpid: number,  // 临时项目 id
    uid: number,  // 临时项目所属用户 id
    spid: number | null,  // 临时项目的源项目 id
    name: string  // 临时项目名
}

export interface Comment {
    // 评论对象定义

    cid: number,  // 评论 id
    uid: number,  // 评论的用户的 id
    comment: string,  // 评论内容
    date: string,  // 评论日期
    like: number,  // 赞数
    youlike: boolean  // 当前登录用户是否赞此评论
}

export interface BaseCodeInfo {
    // 基本代码对象结构

    [propName: string]: {
        name: string,
        type: "vue" | "js"
    }
}

export interface CodeInfo {
    // 代码对象结构

    [propName: string]: {
        // propName 是 cid

        cid: string,
        name: string,
        type: "vue" | "js",
        code: string  // 代码文件内容
    }
}

