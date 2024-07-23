import { createRouter, createWebHistory } from 'vue-router';
import loginPage from '../views/loginPage.vue';
import mainPage from '../views/mainPage.vue';

const routes = [
  {
    path: '/',
    name: 'loginPage',
    component: loginPage,
  },
  {
    path: '/mainPage',
    name: 'mainPage',
    component: mainPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
