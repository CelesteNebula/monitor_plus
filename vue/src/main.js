import { createApp } from 'vue';
import App from './App.vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'; // 引入样式文件
import * as echarts from 'echarts';
import router from './router';

const app = createApp(App);
app.config.globalProperties.$echarts = echarts;
app.use(ElementPlus);
app.use(router).mount('#app');