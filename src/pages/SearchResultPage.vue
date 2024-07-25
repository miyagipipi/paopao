<template>
    <user-card-list :user-list="userList" :loading="loading"></user-card-list>
    <van-empty v-if="!userList || userList.length < 1" description="搜索结果为空"></van-empty>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MyAxios from '@/plugins/myAxios.ts';
import UserCardList from '@/components/UserCardList.vue'

const router = useRouter()
const route = useRoute()

const { tags } = route.query
let userList = ref([])
const loading = ref(true)

onMounted(() => {
    MyAxios.post('user/searchUsersByTags', {
        data: tags
    })
    .then(response => {
        userList.value = response.data
        loading.value = false
    })
    .catch(error => {
        console.log(error);
    })
})
</script>