import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router/dist/vue-router";

import indexPage from "@/pages/indexPage.vue";
import searchPage from "@/pages/searchPage.vue";
import projectPage from "@/pages/projectPage.vue";
import projectSettingsPage from "@/pages/projectSettingsPage.vue";
import tempProjectPage from "@/pages/tempProjectPage.vue";
import tempProjectSettingsPage from "@/pages/tempProjectSettingsPage.vue";
import userPage from "@/pages/userPage.vue";
import aboutPage from "@/pages/aboutPage.vue"


const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        name: "indexPage",
        component: indexPage,
        children: []
    },
    {
        path: "/search",
        name: "searchPage",
        component: searchPage,
        children: []
    },
    {
        path: "/about",
        name: "aboutPage",
        component: aboutPage,
        children: []
    },
    {
        path: "/user/:uid",
        name: "userPage",
        component: userPage,
        children: []
    },
    {
        path: "/projects/:pid",
        name: "projectsPage",
        component: projectPage,
        children: []
    },
    {
        path: "/projects/:pid/settings",
        name: "projectSettingsPage",
        component: projectSettingsPage,
        children: []
    },
    {
        path: "/projects/temp/:tpid",
        name: "tempProjectPage",
        component: tempProjectPage,
        children: []
    },
    {
        path: "/projects/temp/:tpid/settings",
        name: "tempProjectSettingPage",
        component: tempProjectSettingsPage,
        children: []
    },
];


export default createRouter({
    history: createWebHistory(),
    routes
});
