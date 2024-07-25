<template>
    <div>
            <RecycleScroller
                class="scroller"
                :items="teamList"
                :item-size="5"
                key-field="id"
                v-slot="{ item }"
            >
            <van-card :title="`${item.name}`" :desc="item.description" :key="item.id">
                <template #thumb>
                    <van-image style="height: 128px; object-fit: unset;" :src="ikun"></van-image>
                </template>
                <template #tags>
                    <van-tag style="margin-right: 8px; margin-top: 8px;" plain type="danger">
                        {{ teamStatusEnum(item.status) }}
                    </van-tag>
                </template>
                <template #bottom>
                    <div>
                        {{ `队伍人数: ${item.userInfo.length}/${item.maxNum}` }}
                    </div>
                    <div v-if="item.expireTime">
                        {{ `过期时间: ${formatISO8601(item.expireTime)}` }}
                    </div>
                    <div>
                        <span v-for="userInfo in item.userInfo">
                            <van-image style="margin-right: 1.5px; width: 28px; height: 28px;" round
                                :src="userInfo.avatarUrl"></van-image>
                        </span>
                    </div>
                </template>
                <template #footer>
                    <van-button v-if="item.hasJoin" size="small" type="primary" plain
                        @click="doEnterTeam(item)">进入
                    </van-button>
                    <van-button v-if="item.userId !== store.userInfo?.id && !item.hasJoin" size="small" type="primary"
                        @click="doJoinTeam(item)">加入</van-button>
                    <van-button v-if="item.userId == store.userInfo.id" size="small" type="warning" plain
                        @click="doUpdateTeam(item.id)">更新
                    </van-button>
                    <van-button v-if="item.userId !== store.userInfo?.id && item.hasJoin" size="small" type="primary" plain
                        @click="doQuitTeam(item.id)">退出
                    </van-button>
                    <van-button v-if="item.userId === store.userInfo?.id" size="small" type="danger" plain
                        @click="doDeleteTeam(item.id)">解散
                    </van-button>
                </template>
            </van-card>
        </RecycleScroller>
        <van-dialog v-model:show="showPasswordDialog" title="请输入密码" show-cancel-button @confirm="joinSecretTeam"
            @cancel="cancelJoinSecretTeam">
            <van-field v-model="password" type="password" />
        </van-dialog>
    </div>
</template>

<script setup lang="ts">
import { teamStatusEnum } from '@/constants/team';
import { teamType } from '@/models/team'
import ikun from '@/assets/ikun.png'
import MyAxios from '@/plugins/myAxios.ts';
import { showToast } from 'vant';
import { UserStore } from '@/stores/userStore';
import { useRoute, useRouter } from 'vue-router';
import { onMounted, ref, defineEmits } from 'vue';
import { formatISO8601 } from '@/services/team';

const router = useRouter()
const route = useRoute()
const store = UserStore()

interface TeamCardListProps {
    teamList: teamType[];
}
const props = withDefaults(defineProps<TeamCardListProps>(), {
    teamList: () => [] as teamType[]
})

const emit = defineEmits(['refresh-event'])

const showPasswordDialog = ref(false);
const password = ref('')
const curTeam = ref<teamType>({})

const doEnterTeam = async (team: teamType) => {
    store.enterTeam = team
    router.push({
        name: 'TeamRoom',
        query: {
            teamId: team.id
        }
    })
}

const doJoinTeam = async (team: teamType) => {
    if (team.status === 0) {
        await joinPublicTeam(team.id)
    } else if (team.status === 1) {
        showPasswordDialog.value = true
        curTeam.value = team
    }
}

const joinPublicTeam = async (teamId: number) => {
    const response = await MyAxios.post('/team/join', {
        teamId
    })
    commonToast(response, '加入成功')
    showPasswordDialog.value = false
    emit('refresh-event')
    console.log('props.teamList', props.teamList)
}

const joinSecretTeam = async () => {
    const response = await MyAxios.post('/team/join', {
        teamId: curTeam.value.id,
        password: password.value
    })
    commonToast(response, '加入成功')
    cancelJoinSecretTeam()
    emit('refresh-event')
}

const cancelJoinSecretTeam = () => {
    showPasswordDialog.value = false
    curTeam.value = <teamType>{}
    password.value = ''
}

const doUpdateTeam = (id: number) => {
    router.push({
        path: "/team/update",
        query: {
            id,
            redirect: route.path
        }
    })
}

const doQuitTeam = async (id: number) => {
    const response = await MyAxios.post('/team/quit', {
        teamId: id
    })
    commonToast(response)
    emit('refresh-event')
    console.log(props.teamList)
}

const doDeleteTeam = async (id: number) => {
    const response = await MyAxios.post('/team/delete', {
        id
    })
    commonToast(response)
    emit('refresh-event')
}

const commonToast = (response: any, msg: string = '操作成功') => {
    if (response?.status === 200 && response?.ret === 0) {
        showToast({
            type: 'success',
            message: msg
        })
    } else {
        showToast({
            type: 'fail',
            message: response.msg || '操作失败'
        })
    }
}

onMounted(async () => {
    if (!store.userInfo.id) {
        await store.storeUserInfo()
    }
})
</script>

<style scoped>
.scroller {
  height: 100%;
}
</style>