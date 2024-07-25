<template>
    <div id="teamAdd">
        <van-form @submit="onSubmit">
            <van-cell-group inset>
                <van-field v-model="registerUserDate.userAccount" name="userAccount" label="用户名" placeholder="请输入用户名"
                    :rules="Rules.userAccount" />

                <van-field v-model="registerUserDate.username" name="username" label="用户昵称" placeholder="请输入用户昵称"
                    :rules="Rules.username" />

                <van-field name="gender" label="性别">
                    <template #input>
                        <van-radio-group v-model="registerUserDate.gender" direction="horizontal">
                            <van-radio :name="1">男</van-radio>
                            <van-radio :name="2">女</van-radio>
                        </van-radio-group>
                    </template>
                </van-field>

                <van-field v-model="registerUserDate.userPassword" type="password" name="userPassword" label="密码"
                    placeholder="请输入密码" :rules="Rules.userPassword" />

                <van-field v-model="registerUserDate.phone" name="phone" label="电话号码" placeholder="请输入电话号码"
                    :rules="Rules.phone" />
                <van-field v-model="registerUserDate.email" name="email" label="邮箱地址" placeholder="请输入邮箱地址"
                    :rules="Rules.email" />
            </van-cell-group>
            <div style="margin: 16px;">
                <van-button round block type="primary" native-type="submit">
                    提交
                </van-button>
            </div>
        </van-form>

    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router'
import MyAxios from '@/plugins/myAxios.ts';
import { showToast } from 'vant';

const router = useRouter()

let Rules = ref({
    username: [{ required: true, message: '请填写用户昵称' }],
    description: [{ required: true, message: '请填写队伍描述' }],
    userAccount: [{ required: true, message: '请填写用户名' }],
    userPassword: [{ required: true, message: '请填写密码' }],
    phone: [{ required: true, message: '请填写密码' }],
    email: [{ required: true, message: '请填写密码' }],
})

const initFormData = {
    "username": "",
    "userAccount": "",
    "gender": 1,
    "userPassword": "",
    "phone": null,
    "email": null,
}
// 用户填写的表单数据
const registerUserDate = ref({ ...initFormData })

let initStatus = registerUserDate.value.status == 0
const passwordDisabled = ref(initStatus)

const checkSubmit = async () => {
    const userAccount = registerUserDate.value.userAccount
    if (!userAccount || !userAccount.trim()) {
        showToast({
            message: '请填写用户名且前后不要加空格',
            type: 'fail'
        })
        return false
    }
    const res = await MyAxios.post('/user/account/exist', {
        userAccount
    })
    if (res.ret === 0) {
        return true
    } else {
        showToast({
            message: '用户名已存在',
            type: 'fail'
        })
        return false
    }
}

const onSubmit = async () => {
    let check_res = await checkSubmit()
    if (!check_res) {
        return
    }

    const response = await MyAxios.post("/user/register", {
        ...registerUserDate.value
    })
    if (response.status === 200 && response.ret === 0) {
        showToast({
            message: '注册成功',
            type: 'success'
        })
        router.replace({
            name: 'LOGIN',
        })
    } else {
        showToast({
            message: response.msg || '注册失败',
            type: 'fail'
        })
    }
}
</script>

<style scoped></style>