const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: '/dasijpatchnotes/'
},
{
  publicPath: process.env.NODE_ENV === 'production'
    ? '/HOTS-dasij/'
    : '/'
})
