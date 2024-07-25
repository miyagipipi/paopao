<template>
    <van-cell center title="心动模式">
        <template #right-icon>
            <van-switch v-model="isMatchMode" @change="changeUserList" />
        </template>
    </van-cell>
    <div v-infinite-scroll="loadMore" :infinite-scroll-disabled="busy" infinite-scroll-distance="0">
        <user-card-list :user-list="userList" :loading="loading"></user-card-list>
    </div>
    <!-- <user-card-list :user-list="userList" :loading="loading"></user-card-list> -->
    <van-empty v-if="!userList || userList.length < 1" description="数据为空"></van-empty>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import MyAxios from '@/plugins/myAxios.ts';
import { showToast } from 'vant';
import UserCardList from '@/components/UserCardList.vue'

// 模式切换
const isMatchMode = ref<boolean>(false)

let userList = ref([])
const loading = ref(true)
const pageSize = ref(10)
const pageNum = ref(1)
const busy = ref(false)

const loadData = async () => {
    let userListData = []
    loading.value = true
    // 心动模式匹配用户
    if (isMatchMode.value) {
        userListData = await MyAxios.get('user/match', {
            params: {
                num: 10
            }
        })
        .then(response => {
            return response?.data
        })
        .catch(error => {
            console.log(error);
            showToast({
                message: '请求失败',
                type: 'fail'
            })
        })
    } else {
        userListData = await loadRecommendUser()
        if (userListData.length === 0) { 
            loading.value = false
            return
        }
        pageNum.value += 1
    }
    userList.value = userListData
    loading.value = false
}

const loadMore = () => {
    busy.value = true;
    setTimeout(async () => {
        const partUserList = await loadRecommendUser()
        if (partUserList.length === 0) {return}
        pageNum.value += 1
        for (let partUser of partUserList) {
            userList.value.push(partUser)
        }
        busy.value = false
    }, 1000);
}

const loadRecommendUser = async () => {
    const response = await MyAxios.get('index/recommend', {
        params: {
            pageSize: pageSize.value,
            pageNum: pageNum.value
        }
    })
    if (response?.status !== 200 || response?.ret === 1) {
        showToast({
            type: 'fail',
            message: response.msg || '操作失败'
        })
    }
    return response.data
}

const changeUserList = () => {
    pageNum.value = 1
    loadData()
}

onMounted(() => {
    loadData()
})

</script>