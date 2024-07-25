<template>
    <div id="teamAdd">
        <van-form @submit="onSubmit">
            <van-cell-group inset>
                <van-field v-model="addTeamDate.name" name="name" label="队伍名称" placeholder="请输入队伍名称"
                    :rules="Rules.name" />

                <van-field v-model="addTeamDate.description" rows="1" autosize label="队伍描述" type="textarea" placeholder="请输入队伍描述"
                    :rules="Rules.description" />

                <van-field name="radio" label="队伍状态">
                    <template #input>
                        <van-radio-group v-model.number="addTeamDate.status" direction="horizontal"
                            @change="changeStatus">
                            <van-radio :name="0">公开</van-radio>
                            <van-radio :name="1">加密</van-radio>
                            <van-radio :name="2">私有</van-radio>
                        </van-radio-group>
                    </template>
                </van-field>

                <van-field v-model="addTeamDate.password" type="password" name="password" 
                    label="队伍密码" placeholder="请输入密码"
                    :disabled="passwordDisabled">
                </van-field>
                
                <div style="padding: 10px 16px 10px 16px;">
                    <span style="font-size: 14px; margin-right: 16px; color: #323233;">
                        过期时间
                    </span>
                    <el-date-picker
                        v-model="addTeamDate.expireTime"
                        type="datetime"
                        placeholder="点击选择过期时间"
                        format="YYYY-MM-DD hh:mm:ss"
                        value-format="YYYY-MM-DD hh:mm:ss"
                        :clearable="true"
                    />
                </div>
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
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import MyAxios from '@/plugins/myAxios.ts';
import { showToast } from 'vant';

const router = useRouter()
const route = useRoute()

const initFormData = {
    "name": "",
    "description": "",
    "maxNum": 2,
    "expireTime": "",
    "userId": 0,
    "status": 0,
    "password": ""
}

const id = route.query.id

// 用户填写的表单数据
const addTeamDate = ref({})

onMounted(async () => {
    if (id <= 0) {
        showToast({
            type: 'fail',
            message: '加载队伍失败'
        })
        return
    }
    const response = await MyAxios.get("team/get", {
        params: {
            id: id
        }
    })
    if (response?.status === 200 && response?.ret === 0) {
        addTeamDate.value = response.data
    } else {
        showToast({
            type: "fail",
            message: response.msg || '获取队伍信息失败'
        })
    }
})

let initStatus = addTeamDate.value.status == 0
const passwordDisabled = ref(initStatus)

let Rules = ref({
    name: [{ required: true, message: '请填写队伍名称' }],
    description: [{ required: true, message: '请填写队伍描述' }],
})

const changeStatus = () => {
    if (addTeamDate.value.status !== 0) {
        passwordDisabled.value = false
    } else {
        passwordDisabled.value = true
    }
}

const checkSubmit = () => {
    const { password, status, expireTime } = addTeamDate.value
    let now = new Date();
    if (status !== 0 && password === '') {
        showToast({
            message: '非公开队伍需要设置密码',
            type: 'fail'
        })
        return false
    } else if (now >= new Date(expireTime)) {
        showToast({
            message: '过期时间必须大于当前时间',
            type: 'fail'
        })
        return false
    }
    return true
}

const onSubmit = async () => {
    // let check_res = checkSubmit()
    // if (!check_res) {
    //     return
    // }

    const response = await MyAxios.post("/team/update", {
        ...addTeamDate.value
    })
    if (response.status === 200 && response.teamId != -1) {
        showToast({
            message: '更新成功',
            type: 'success'
        })
        router.push({
            path: route.query.redirect || '/team',
            replace: true,
        })
    } else {
        showToast({
            message: response.msg || '更新失败',
            type: 'fail'
        })
    }
}
</script>

<style scoped>

</style>