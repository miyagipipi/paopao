<template>
    <van-nav-bar
        :title="title"
        left-arrow
        @click-left="onClickLeft"
    >
        <template #right>
            <van-icon v-show="showSearchIcon()" name="search" size="18" @click="onClickRight" />
        </template>
    </van-nav-bar>

    <div id="content">
        <RouterView></RouterView>
    </div>

    <van-tabbar route @change="onChange" v-model="active">
        <van-tabbar-item to="/" icon="home-o" name="index">主页</van-tabbar-item>
        <van-tabbar-item to="/team/add" icon="add-o" name="create">创建</van-tabbar-item>
        <van-tabbar-item to="/team" icon="search" name="team">队伍</van-tabbar-item>
        <van-tabbar-item to="/user" icon="friends-o" name="user">个人</van-tabbar-item>
    </van-tabbar>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const active = ref('index')

/**
 * 切换标题
 */
const DEFAULT_TITLE = '活动匹配系统'
const title = ref(DEFAULT_TITLE)
router.beforeEach((to, from) => {
    if (to.meta?.title) {
        title.value = to.meta.title
    } else {
        title.value = DEFAULT_TITLE
    }
    
})

const onClickLeft = () => {
    router.back()
}
const onClickRight = () => {
    router.push('/search')
}
const onChange = (index) => {};

const showSearchIcon = () => {
    return route.path === '/' ? true : false
}

</script>

<style scoped>
#content {
    padding-bottom: 50px;
}
</style>
