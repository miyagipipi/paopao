<template>
    <div id="teamPage">
        <van-search v-model="searchText" placeholder="搜索队伍" @search="onSearch" />
        <van-tabs v-model:active="active" @click-tab="onClickTab">
            <InfiniteList :data="publicTeam" :width="'100%'" :height="800" :itemSize="200"
                 v-slot="{ item, index }">
                <team-card-list-test :item="item" @refresh-event="refreshTeamList"></team-card-list-test>
            </InfiniteList>
        </van-tabs>
        <div style="margin-bottom: 16px;"></div>
        <van-empty v-if="publicTeam.length < 1" description="数据为空"></van-empty>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import TeamCardListTest from '@/components/TeamCardListTest.vue';
import { nextTick, onMounted, ref } from 'vue';
import MyAxios from '@/plugins/myAxios.ts';
import { showToast } from 'vant';
import { getTeamList } from '@/services/team';
import InfiniteList from 'vue3-infinite-list';

const router = useRouter()

const searchText = ref('')
const active = ref('public')
const publicTeam = ref([])
const secretTeam = ref([])
const debug = ref(true)

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

const refreshTeamList = async () => {
    console.log('get emit from child component')
    if (active.value === 'public') {
        await listTeam(searchText.value, 0)
    } else {
        await listTeam(searchText.value, 1)
    }
}

const listTeam = async(val='', status=0) => {
    console.log('team ready to update')
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
    console.log('team update finish')
}

onMounted(async () => {
    await listTeam()

})
</script>

<style scoped>
    
</style>