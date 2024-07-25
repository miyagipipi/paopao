<template>
  <BasicLayout></BasicLayout>
</template>

<script setup>
import BasicLayout from "@/layouts/BasicLayout.vue"
import { useRouter } from "vue-router";
import MyAxios from "@/plugins/myAxios";

const router = useRouter()
router.beforeEach(async (to, from) => {
  const res = await MyAxios.get('user/checkLogin')
  if (res.ret !== 0 && to.name != 'LOGIN' && to.name != 'Register') {
    return {name: 'LOGIN', query: { redirect: to.path || to.name } }
  }
})
</script>

<style scoped>

</style>
