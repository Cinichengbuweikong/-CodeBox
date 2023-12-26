import axios from "axios";

import { UserInfo } from "@/types";


export default async function getUserInfo(): Promise<UserInfo | null> {
    // 获取用户信息的函数

    try {
        const response = await axios.get("/api/user/");

        if (response.status != 200 || response.data.code) {
            console.log(`请求成功 但信息不可用: ${JSON.stringify(response.data)}`);
            return null;
        }

        return response.data;
    } catch(e) {
        console.log(`请求失败: ${e}`);

        return null;
    }
}
