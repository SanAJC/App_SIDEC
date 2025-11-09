import { createRouter, createWebHistory } from "vue-router";

import Landing from "../../views/Landing.vue";
import Login from "../../views/Login.vue";
import Dashboard from "../../views/Dashboard.vue";
import ReportForm from "../../views/ReportForm.vue";
import { getProfile } from "@/api/auth";
import Profile from "../../views/Profile.vue";

const routes = [
  { path: "/", name: "Landing", component: Landing },
  { path: "/login", name: "Login", component: Login },
  { path: "/dashboard", name: "Dashboard", component: Dashboard, meta: { requiresAuth: true } },
  { path: "/profile", name: "Profile", component: Profile, meta: { requiresAuth: true } },
  { path: "/report", name: "ReportForm", component: ReportForm },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (!to.meta?.requiresAuth) return next();
  try {
    await getProfile();
    next();
  } catch (e) {
    next({ name: 'Login' });
  }
});

export default router;
