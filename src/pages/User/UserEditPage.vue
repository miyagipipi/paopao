<template>
    <van-form @submit="onSubmit">
        <van-cell-group inset>
            <van-field v-if="eidtUser.editKey === 'gender'" :name="eidtUser.editKey" :label="eidtUser.editName">
                <template #input>
                    <van-radio-group v-model="eidtUser.currentValue" direction="horizontal">
                        <van-radio name="1">男</van-radio>
                        <van-radio name="2">女</van-radio>
                    </van-radio-group>
                </template>
            </van-field>

            <van-field v-else-if="eidtUser.editKey === 'avatarUrl'" :name="eidtUser.editKey" label="上传头像">
                {{ eidtUser.editKey }}
                <template #input>
                    <van-uploader v-model="fileList" :multiple="false" max-count="1"
                    :after-read="afterRead" :before-delete="beforeDelete" />
                </template>
            </van-field>

            <van-field v-else v-model="eidtUser.currentValue" :name="eidtUser.editKey" :label="eidtUser.editName"
                :placeholder="`请输出${eidtUser.editName}`">
            </van-field>
            
        </van-cell-group>
        <div style="margin: 16px;">
            <van-button round block type="primary" native-type="submit">
                提交
            </van-button>
        </div>
    </van-form>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { ref } from 'vue';
import MyAxios from '@/plugins/myAxios.ts';
import { showToast } from 'vant';
import { UserStore } from '@/stores/userStore'

const router = useRouter()
const route = useRoute()
let store = UserStore()
const eidtUser = ref({
    editKey: route.query.editKey,
    editName: route.query.editName,
    currentValue: route.query.currentValue
})

const fileList = ref([]);
let formData = new FormData()

const afterRead = (file) => {
    // 此时可以自行将文件上传至服务器
    formData.append('avatar', file.file)
};

const beforeDelete = () => {
    formData = new FormData()
    fileList.value = []
}

const onSubmit = async () => {
    // todo editKey editName currentValue 提交到后台
    let res = null
    if (eidtUser.value.editKey === 'avatarUrl') {
        res = await MyAxios.post('/user/upload/avatar', formData, {
            headers: {
                'Content-Type': 'multipart/form-data', // 必须设置请求头
            },
        })
    } else {
        res = await MyAxios.post('user/update', {
            id: store.userInfo.id,
            [eidtUser.value.editKey as string]: eidtUser.value.currentValue
        })
    }
    if (res.status === 200 && res.ret === 0) {
        showToast({
            message: '修改成功',
            type: 'success',
        });
        await store.storeUserInfo()
        router.back()
    } else {
        showToast({
            message: '更新失败',
            type: 'fail'
        });
    }
}
</script>

<style scoped></style>