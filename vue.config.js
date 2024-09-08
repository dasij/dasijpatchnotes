const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');

module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/dasijpatchnotes/' : '/',
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_OPTIONS_API__: true,
        __VUE_PROD_DEVTOOLS__: false,
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
      }),
    ],
  },
  chainWebpack: config => {
    config.plugin('html').tap(args => {
      args[0].title = 'Heroes of the Storm Patch Notes';
      args[0].meta = {
        'og:title': { property: 'og:title', content: 'Dasij Notes' },
        'og:description': { property: 'og:description', content: 'Dasij fanmade Heroes of the storm Patch Notes' },
        'og:image': { property: 'og:image', content: 'https://dasij.github.io/dasijpatchnotes/img/logo_hots.ecce837e.png' },
        'og:url': { property: 'og:url', content: 'https://dasij.github.io/dasijpatchnotes/#/' },
      };
      return args;
    });
  },
});