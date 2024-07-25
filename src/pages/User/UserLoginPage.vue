<template>
    <van-form @submit="onSubmit">
        <van-cell-group inset>
            <van-field v-model="userAccount" name="userAccount" label="账号" placeholder="请输入账号"
                :rules="[{ required: true, message: '请填写用户名' }]" />
            <van-field v-model="userPassword" type="password" name="userPassword" label="密码" placeholder="请输入密码"
                :rules="[{ required: true, message: '请填写密码' }]" />
        </van-cell-group>
        <div style="margin: 16px;">
            <van-button style="margin-left: 15%;" type="primary" round @click="doRegisterAccoount">注册</van-button>
            <van-button style="margin-left: 30%;" round type="success" native-type="submit">
                登录
            </van-button>
        </div>
    </van-form>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MyAxios from '@/plugins/myAxios.ts';
import { showToast, showNotify } from 'vant';
import { UserStore } from '@/stores/userStore'

const router = useRouter()
const route = useRoute()

let store = UserStore()

let redirect = '/'

const userAccount = ref('');
const userPassword = ref('');
const onSubmit = async () => {
    const res =  await MyAxios.post('user/login', {
        userAccount: userAccount.value,
        userPassword: userPassword.value
    })
    if (res.status === 200 && res.ret === 0) {
        showToast('登录成功')
        await store.storeUserInfo()
        router.replace(redirect)
    } else {
        showToast({
            message: '登录失败',
            type: 'fail'
        })
    }
};

const doRegisterAccoount = () => {
    router.push({
        path: '/user/register'
    })
}

onMounted(() => {
    if (route.query.redirect) {
        showNotify({ type: 'warning', message: '请先登录' });
        redirect = String(route.query.redirect)
    }
})

</script>

<style scoped></style>