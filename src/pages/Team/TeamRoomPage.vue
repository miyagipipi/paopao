<template>
    <div>
        <van-collapse v-model="activeNames">
            <van-collapse-item v-for="item in teamPlans" size="large" :title="item.title" :name="item.id" :key="item.id"
                :value="formatISO8601(item.createTime)">
                {{ item.description }}
            </van-collapse-item>
        </van-collapse>
        <van-button class="add-button" icon="plus" type="primary" @click="showPopup"></van-button>
        <van-popup v-model:show="showAddPlan" position="bottom" :style="{ height: '40%' }">
            <van-form @submit="onSubmit">
                <van-cell-group inset style="margin-top: 30px;">
                    <van-field v-model="addTeamPlan.title" name="title" label="计划标题" placeholder="请输入计划标题"
                        :rules="Rules.title" />

                    <van-field v-model="addTeamPlan.description" rows="1" autosize label="计划内容" type="textarea"
                        placeholder="请输入计划内容" :rules="Rules.description" />
                    <van-button round block type="primary" native-type="submit">
                        提交
                    </van-button>
                </van-cell-group>
            </van-form>
        </van-popup>
    </div>
</template>

<script setup>
import MyAxios from '@/plugins/myAxios';
import { UserStore } from '@/stores/userStore';
import { showToast } from 'vant';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { formatISO8601 } from '@/services/team';

const router = useRouter()
const route = useRoute()
const userStore = UserStore()

const teamPlans = ref([])
const showAddPlan = ref(false)
const initFormData = {
    "title": "",
    "description": "",
}
// 用户填写的表单数据
const addTeamPlan = ref({ ...initFormData })
const activeNames = ref(['1']);

let Rules = ref({
    title: [{ required: true, message: '请填写计划标题' }],
    description: [{ required: true, message: '请填写计划内容' }],
})

const showPopup = () => {
    showAddPlan.value = true
}

const onSubmit = async () => {
    const response = await MyAxios.post("/team/plan/add", {
        ...addTeamPlan.value,
        teamId: userStore.enterTeam.id
    })
    if (response.status === 200 && response.ret === 0) {
        showToast({
            message: '创建成功',
            type: 'success'
        })
    } else {
        showToast({
            message: response.msg || '创建失败',
            type: 'fail'
        })
    }
    showAddPlan.value = false
    await initData(userStore.enterTeam.id)
}

const initData = async (teamId) => {
    const res = await MyAxios.post('/team/plan', {
        teamId: teamId
    })
    if (res?.status === 200 && res?.ret === 0) {
        teamPlans.value = res.data
    } else {
        showToast({
            type: 'fail',
            message: res.msg || '加载队伍失败，请退出重试'
        })
        router.back()
    }
}

onMounted(async () => {
    const storeTeamId = userStore.enterTeam.id
    const queryTeamId = Number(route.query.teamId) || undefined
    if (storeTeamId && storeTeamId === queryTeamId) {
        initData(storeTeamId)
    } else {
        router.back()
    }
})
</script>

<style scoped></style>
