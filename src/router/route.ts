import Index from '@/pages/Index.vue'
import Team from '@/pages/Team/TeamPage.vue'
import UserUpdate from '@/pages/User/UserUpdatePage.vue'
import SearchPage from '@/pages/SearchPage.vue'
import SearchResultPage from '@/pages/SearchResultPage.vue'
import UserEditPage from '@/pages/User/UserEditPage.vue'
import UserLoginPage from '@/pages/User/UserLoginPage.vue'
import TeamAddPage from '@/pages/Team/TeamAddPage.vue'
import TeamUpdatePage from '@/pages/Team/TeamUpdatePage.vue'
import UserPage from '@/pages/User/UserPage.vue'
import TeamRoomPage from '@/pages/Team/TeamRoomPage.vue'
import UserRegisterPage from '@/pages/User/UserRegisterPage.vue'
import UserEditTagsPage from '@/pages/User/UserEditTagsPage.vue'

const routes = [
  { path: '/', component: Index },
  { path: '/team', meta:{'title': '发现队伍'}, component: Team },
  { path: '/team/add', meta:{'title': '创建队伍'}, component: TeamAddPage },
  { path: '/team/update', meta:{'title': '更新队伍信息'}, component: TeamUpdatePage },
  { path: '/team/room', name: 'TeamRoom', meta:{'title': '当前队伍'}, component: TeamRoomPage },

  { path: '/user/update', meta:{'title': '更新个人信息'}, component: UserUpdate },
  { path: '/user', meta:{'title': '个人信息'}, component: UserPage },
  { path: '/user/list', meta:{'title': '用户列表'}, component: SearchResultPage },
  { path: '/user/edit', meta:{'title': '编辑信息'}, component: UserEditPage },
  { path: '/user/login', name: 'LOGIN', meta:{'title': '登录'}, component: UserLoginPage },
  { path: '/user/register', name: 'Register', meta:{'title': '注册用户'}, component: UserRegisterPage },
  { path: '/user/edit/tags', meta:{'title': '编辑标签'}, component: UserEditTagsPage },

  { path: '/search', meta:{'title': '搜索用户'}, component: SearchPage },
]

export default routes