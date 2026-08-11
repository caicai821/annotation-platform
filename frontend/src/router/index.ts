import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      component: () => import('../layouts/MainLayout.vue'),
      children: [
        { path: '', name: 'home', component: () => import('../views/dashboard/HomeView.vue') },
        { path: 'datasets', name: 'datasets', component: () => import('../views/datasets/DatasetListView.vue') },
        { path: 'tasks', name: 'tasks', component: () => import('../views/tasks/TaskListView.vue') },
        {
          path: 'annotate/text/:taskId',
          name: 'annotate-text',
          component: () => import('../views/annotate/text/TextAnnotationView.vue'),
          meta: { title: '文本标注' },
        },
        {
          path: 'annotate/image/:taskId',
          name: 'annotate-image',
          component: () => import('../views/annotate/image/ImageAnnotationView.vue'),
          meta: { title: '图像标注' },
        },
      ],
    },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('../views/NotFoundView.vue') },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (!to.meta.public && !auth.token) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.name === 'login' && auth.token) {
    return { name: 'home' }
  }
})

export default router
