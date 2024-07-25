import { getCurrentUser, getMyTeam } from '@/services/user'
import { defineStore } from 'pinia'
import { showToast } from 'vant';
import { teamType } from '@/models/team';

export const UserStore = defineStore('UserStore', {
    state: () => {
        return {
            userInfo: {
                id: undefined,
                username: '',
                userAccount: '',
                avatarUrl: '',
                gender: undefined,
                phone: '',
                email: '',
                userState: undefined,
                userRole: undefined,
                planetCode: '',
                tags: [],
                createTime: '',
                profile: '',
            },
            myJoinTeam: [] as teamType[],
            myCreateTeam: [] as teamType[],
            enterTeam: {} as teamType,
        }
    },
    getters: {
        getState: (state) => {
            return state.userInfo
        },
    },
    actions: {
        async storeUserInfo() {
            const res = await getCurrentUser()
            if (res.status === 200 && res.ret === 0) {
                this.userInfo = res.data
            } else {
                showToast({
                    message: '获取用户信息失败',
                    type: 'fail'
                });
            }
        },
        async storeMyTeam(teamType: string = 'myCreate')  {
            const response = await getMyTeam(teamType)
            if (response?.status === 200 && response?.ret === 0) {
                if (teamType === 'myCreate') {
                    this.myCreateTeam = response.data
                } else if (teamType === 'myJoin') {
                    this.myJoinTeam = response.data
                }
            } else {
                showToast({
                    type: 'fail',
                    message: response.msg || '加载队伍失败，请刷新重试'
                })
            }
        }
    }
})