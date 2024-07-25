<template>
    <slot name="search">
        <form action="/">
            <van-search v-model="searchText" show-action placeholder="请输入要搜索的标签" @search="onSearch"
                @update:model-value="watchUpdate" @cancel="onCancel" />
        </form>
    </slot>
    <slot :tagList="tagList" :rawTagList="rawTagList" :activeIds="activeIds">
        <van-divider content-position="center">
            已选标签
        </van-divider>
        <div v-if="activeIds.length === 0">请选择标签</div>

        <van-row gutter="16" style="padding: 0, 16px;">
            <van-col v-for="tag in activeIds" span="4">
                <van-tag :show="true" closeable size="large" type="primary" @close="doClose(tag)">
                    {{ tag }}
                </van-tag>
            </van-col>
        </van-row>

        <van-divider content-position="center">
            选择标签
        </van-divider>
        <van-tree-select v-model:active-id="activeIds" v-model:main-active-index="activeIndex" :items="tagList" />
    </slot>

    <slot name="footer" :tagList="tagList" :rawTagList="rawTagList" :activeIds="activeIds">
        <div style="padding: 12px;">
            <van-button block style="" type="primary" @click="doSearchResult">搜索</van-button>
        </div>
    </slot>
</template>

<script setup>
import { getTotalTags } from '@/services/user';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const searchText = ref('');
const activeIds = ref([]);
const activeIndex = ref();
const rawTagList = ref([]);
const tagList = ref([])

const eidtUser = ref({
    editKey: route.query.editKey,
    editName: route.query.editName,
    currentValue: route.query.currentValue
})

const doClose = (tag) => {
    activeIds.value = activeIds.value.filter(item => {
        return item !== tag
    })
}

const onSearch = () => {
    tagList.value = rawTagList.value.map(parent => ({
        text: parent.text,
        children: parent.children.filter(child => child.text.includes(searchText.value))
    }))
};

const onCancel = () => {
    searchText.value = ''
    tagList.value = rawTagList.value.slice()
};

const watchUpdate = (val) => {
    if (val === '') {
        tagList.value = rawTagList.value.slice()
    }
}

/**
 * 执行搜索后
 */
const doSearchResult = () => {
    router.push({
        path: '/user/list',
        query: {
            tags: activeIds.value
        }
    })
}

onMounted(async () => {
    const res = await getTotalTags()
    if (res.status === 200 && res.ret === 0) {
        rawTagList.value = res.data
        tagList.value = res.data
    }
    if (Array.isArray(eidtUser.value.currentValue)) {
        activeIds.value = eidtUser.value.currentValue
    }

})

</script>