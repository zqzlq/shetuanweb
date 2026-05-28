import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/AboutView.vue'),
  },
  {
    path: '/members',
    name: 'members',
    component: () => import('@/views/MembersView.vue'),
  },
  {
    path: '/projects',
    name: 'projects',
    component: () => import('@/views/ProjectsView.vue'),
  },
  {
    path: '/projects/awards',
    name: 'awards',
    component: () => import('@/views/AwardsView.vue'),
  },
  {
    path: '/awards/:slug',
    name: 'award-detail',
    component: () => import('@/views/AwardDetailView.vue'),
  },
  {
    path: '/project/:slug',
    name: 'project-detail',
    component: () => import('@/views/ProjectDetailView.vue'),
  },
  {
    path: '/blog',
    name: 'blog',
    component: () => import('@/views/BlogView.vue'),
  },
  {
    path: '/join',
    name: 'join',
    component: () => import('@/views/JoinView.vue'),
  },
  {
    path: '/recruitment',
    name: 'recruitment',
    component: () => import('@/views/RecruitmentView.vue'),
  },
  {
    path: '/open-source',
    name: 'open-source',
    component: () => import('@/views/OpenSourceView.vue'),
  },
  {
    path: '/timeline',
    name: 'timeline',
    component: () => import('@/views/TimelineView.vue'),
  },
  {
    path: '/onboarding',
    name: 'onboarding',
    component: () => import('@/views/OnboardingView.vue'),
  },
  {
    path: '/yuji',
    name: 'yuji',
    component: () => import('@/views/YujiView.vue'),
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('@/views/AdminView.vue'),
  },
  {
    path: '/user',
    name: 'user',
    component: () => import('@/views/UserDashboard.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  },
})

export default router
