const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        xfwd: true,
      },
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        xfwd: true,
      },
    },
  },
})
