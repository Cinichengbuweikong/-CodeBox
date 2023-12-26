<template>
  <suspense>
    <router-view></router-view>
  </suspense>
</template>


<script setup lang="ts">
import { defineOptions, onMounted } from 'vue';
import { useStore } from 'vuex';
import "element-plus/theme-chalk/el-message.css";


defineOptions({
  name: "App"
});


const store = useStore();


onMounted(() => {
  // 在页面挂载时即从服务端获取用户信息

  store.dispatch("fetchUserInfo");
});
</script>


<style lang="scss">
#app {
  width: 100vw;
  height: 100vh;
  overflow: hidden;

  background-color: $backgroundColor;

}
</style>


<style lang="scss">
#app {
  // 重写 element-plus 的默认样式

  --el-color-primary: #{ $foregroundColor };
  --el-text-color-regular: #{ $fontColor };
}
</style>
