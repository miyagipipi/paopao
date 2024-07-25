<template>
    <div id="teamPage">
        <van-search v-model="searchText" placeholder="搜索队伍" @search="onSearch" />
        <van-tabs v-model:active="active" @click-tab="onClickTab">
            <van-tab title="公开" name='public'>
                <team-card-list :team-list="publicTeam" @refresh-event="refreshTimeList"></team-card-list>
            </van-tab>
            <van-tab title="加密" name='secret'>
                <team-card-list :team-list="secretTeam" @refresh-event="refreshTimeList"></team-card-list>
            </van-tab>
        </van-tabs>
        <div style="margin-bottom: 16px;"></div>
        <van-empty v-if="publicTeam.length < 1" description="数据为空"></van-empty>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import TeamCardList from '@/components/TeamCardList.vue';
import { nextTick, onMounted, ref } from 'vue';
import MyAxios from '@/plugins/myAxios.ts';
import { showToast } from 'vant';
import { getTeamList } from '@/services/team';

const router = useRouter()

const searchText = ref('')
const active = ref('public')
const publicTeam = ref([])
const secretTeam = ref([])

const onClickTab = async ({ name }) => {
    if (name === 'public') {
        await listTeam(searchText.value, 0)
    } else {
        await listTeam(searchText.value, 1)
    }
};

const onSearch = async (val) => {
    const status = active.value === 'public' ? 0 : 1
    await listTeam(val, status)
};

const refreshTimeList = async () => {
    if (active.value === 'public') {
        await listTeam(searchText.value, 0)
    } else {
        await listTeam(searchText.value, 1)
    }
    console.log('publicTeam.value', publicTeam.value)
}

const listTeam = async(val='', status=0) => {
    const res = await getTeamList(val, status)
    if (res?.status === 200 && res?.ret === 0) {
        if (status === 0) {
            publicTeam.value = res.data
        } else {
            secretTeam.value = res.data
        }
    } else {
        showToast({
            type: 'fail',
            message: res.msg || '加载队伍失败，请刷新重试'
        })
    }
}

onMounted(async () => {
    await listTeam()
})
</script>

<style scoped>
    
</style>