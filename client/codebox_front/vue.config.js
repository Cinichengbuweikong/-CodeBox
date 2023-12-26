const AutoImport  = require("unplugin-auto-import/webpack");
const Components = require('unplugin-vue-components/webpack');
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers');
const ElementPlus = require('unplugin-element-plus/webpack');

const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,

  configureWebpack: {
    resolve: {
      alias: {
        components: "@components"
      }
    },

    plugins: [
      AutoImport({
        resolvers: [ElementPlusResolver()]
      }),

      Components({
        resolvers: [ElementPlusResolver()]
      }),

      ElementPlus({
        useSource: true
      }),
    ],
  },

  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/assets/globalStyles/global.scss";`,
      }
    }
  },

  devServer: {
    proxy: {
      '/api': {
        target: "http://localhost",
        pathRewrite: {
          "^/api": "/api"
        },
        changeOrigin: true
      },

      "/assets": {
        target: "http://localhost",
        pathRewrite: {
          "^/assets": "/assets"
        },
        changeOrigin: true
      }
    }
  },

})
