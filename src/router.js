import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('./views/HomeView.vue') },
  { path: '/science/dashboard', name: 'science-dashboard', component: () => import('./views/ScienceDashboardView.vue') },
  { path: '/science/vimig', name: 'science-vimig', component: () => import('./views/VisualMigrationView.vue') },
  { path: '/science/molting', name: 'science-molting', component: () => import('./views/MoltingView.vue') },
  { path: '/science/data', name: 'science-data', component: () => import('./views/DataView.vue') },
  { path: '/science/publications', name: 'publications', component: () => import('./views/PublicationsView.vue') },
  { path: '/about/history', name: 'history', component: () => import('./views/HistoryView.vue') },
  { path: '/about/team', name: 'team', component: () => import('./views/TeamView.vue') },
  { path: '/about/partners', name: 'partners', component: () => import('./views/PartnersView.vue') },
  { path: '/participate/volunteer', name: 'volunteer', component: () => import('./views/VolunteerView.vue') },
  { path: '/participate/visit', name: 'visit', component: () => import('./views/VisitView.vue') },
  { path: '/participate/donate', name: 'donate', component: () => import('./views/DonateView.vue') },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('./views/NotFoundView.vue') }
]

export default createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})
