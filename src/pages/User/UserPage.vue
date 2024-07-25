<template>
    <template v-if="user">
        <van-card
            :desc="user.profile"
            :title="`${user.username}(ID: ${user.id})`"
        >
            <template #thumb>
                <van-image round width="4rem" height="4rem" :src="user.avatarUrl"></van-image>
            </template>
            <template #num>
                <van-button icon="setting-o" type="primary" plain round size="small" to="/user/update">编辑资料</van-button>
            </template>
        </van-card>

        <van-tabs v-model:active="TeamActiveName" @click-tab="onClickTeamTab">
            <van-tab title="创建的队伍" name="myCreate">
                <team-card-list :team-list="store.myCreateTeam" @refresh-event="refreshTimeList"></team-card-list>
                <van-empty v-if="store.myCreateTeam.length < 1" description="数据为空"></van-empty>
            </van-tab>
            <van-tab title="加入的队伍" name="myJoin">
                <team-card-list :team-list="store.myJoinTeam" @refresh-event="refreshTimeList"></team-card-list>
                <van-empty v-if="store.myJoinTeam.length < 1" description="数据为空"></van-empty>
            </van-tab>
        </van-tabs>
    </template>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { UserStore } from '@/stores/userStore'
import TeamCardList from '@/components/TeamCardList.vue';
import MyAxios from '@/plugins/myAxios';

const router = useRouter()
const route = useRoute()
let store = UserStore()
let user = ref()

const TeamActiveName = ref('myCreate')

const onClickTeamTab = async ({name}) => {
    await store.storeMyTeam(name)
}

const refreshTimeList = async () => {
    await store.storeMyTeam(TeamActiveName.value)
}

onMounted(async () => {
    if (!store.userInfo.id) {
        await store.storeUserInfo()
    }
    user.value = store.getState
    await store.storeMyTeam()
})

</script>

<style scoped>
    
</style>