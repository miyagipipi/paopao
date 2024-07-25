<template>
    <van-skeleton v-for="user in props.userList" title avatar :row="3" :loading="props.loading">
        <van-card :title="`${user.username} (${user.id})`" :desc="user.profile" :thumb="user.avatarUrl">
            <template #tags>
                <van-tag style="margin-right: 8px; margin-top: 8px;" v-for="tag in user.tags" plain type="danger">
                    {{ tag }}
                </van-tag>
            </template>
            <template #footer>
                <van-button size="small">联系</van-button>
            </template>
        </van-card>
    </van-skeleton>
</template>

<script setup lang="ts">
import { userType } from '@/models/user'

interface UserCardListProps {
    loading: boolean;
    userList: userType[];
}
const props = withDefaults(defineProps<UserCardListProps>(), {
    loading: true,
    userList: () => [] as userType[]
})
</script>

<style scoped></style>