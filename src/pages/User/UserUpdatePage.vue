<template>
    <template v-if="user">
        <van-cell title="昵称" is-link to="/user/edit/" :value="user.username" @click="toEdit('username', '昵称', user.username)" />
        <van-cell title="账号" :value="user.userAccount" />
        <van-cell title="头像" is-link to="/user/edit/" @click="toEdit('avatarUrl', '头像', user.avatarUrl)">
            <van-image round width="2.5rem" height="2.5rem" :src="user.avatarUrl"></van-image>
        </van-cell>
        <van-cell title="性别" is-link :value="unionGender(user.gender)" to="/user/edit/" 
            @click="toEdit('gender', '性别', user.gender)" />
        <van-cell title="电话" is-link :value="user.phone" to="/user/edit/" @click="toEdit('phone', '电话', user.phone)" />
        <van-cell title="邮箱" is-link :value="user.email" to="/user/edit/" @click="toEdit('email', '邮箱', user.email)" />
        <van-cell title="简介" is-link :value="user.profile" to="/user/edit/" @click="toEdit('profile', '简介', user.profile)" />
        <van-cell title="我的标签" is-link :value="formatTags(user.tags)" to="/user/edit/tags" @click="toEditTags('tags', '标签', user.tags)" />
        <van-cell title="注册时间" :value="user.createTime" />
        <van-button block color="linear-gradient(to right, #ff6034, #ee0a24)" @click="doQuitLogin">
            退出登录
        </van-button>

    </template>
        
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { UserStore } from '@/stores/userStore'
import { showConfirmDialog, showToast } from 'vant';
import MyAxios from '@/plugins/myAxios';

const router = useRouter()
const route = useRoute()
let store = UserStore()
let user = ref()

const doQuitLogin = () => {
    showConfirmDialog({
        title: '退出登录',
        message:
            '是否确定退出账号',
        })
        .then(async () => {
            const res = await MyAxios.post('/user/quit', {
                id: store.userInfo.id
            })
            if (res.status === 200 && res.ret === 0) {
                showToast({
                    message: '账号已退出',
                    type: 'success'
                })
                router.replace({name: 'LOGIN'})
            } else {
                showToast({
                    message: res.msg || '账号异常',
                    type: 'fail'
                })
            }
        })
        .catch(() => {
            // on cancel
    });
}

onMounted(async () => {
    if (!store.userInfo.id) {
        await store.storeUserInfo()
    }
    user.value = store.userInfo
})

const toEdit = (editKey: string, editName: string, currentValue: string) => {
    router.push({
        path: '/user/edit',
        query: {
            editKey,
            editName,
            currentValue,
        }
    })
}

const toEditTags = (editKey: string, editName: string, currentValue: Array<string>) => {
    router.push({
        path: '/user/edit/tags',
        query: {
            editKey,
            editName,
            currentValue,
        }
    })
}

const unionGender = (gender: number) => {
    return gender === 1 ? '男' : '女'
}

const formatTags = (tags: Array<string>) => {
    return tags.join(', ')
}
</script>

<style scoped>
    
</style>