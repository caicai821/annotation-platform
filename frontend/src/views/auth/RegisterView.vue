<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '../../api/auth'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({
  username: '',
  password: '',
  confirm: '',
})
const loading = ref(false)

async function onSubmit() {
  if (!form.username || !form.password || !form.confirm) {
    ElMessage.warning('请填写完整信息')
    return
  }
  if (form.username.length < 2) {
    ElMessage.warning('用户名至少 2 个字符')
    return
  }
  if (form.password.length < 6) {
    ElMessage.warning('密码至少 6 位')
    return
  }
  if (form.password !== form.confirm) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  loading.value = true
  try {
    await register(form.username, form.password)
    await auth.login(form.username, form.password)
    ElMessage.success('注册成功，已自动登录')
    router.push('/')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-page">
    <el-card class="register-card">
      <h2 class="title">注册账号</h2>
      <el-form :model="form" label-width="70px" @submit.prevent="onSubmit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="至少 2 个字符" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="至少 6 位" />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="form.confirm" type="password" show-password placeholder="再次输入密码" />
        </el-form-item>
        <el-button type="primary" class="submit" :loading="loading" @click="onSubmit">
          注册
        </el-button>
      </el-form>
      <div class="footer">
        已有账号？<router-link to="/login">去登录</router-link>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.register-page {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #001529 0%, #409eff 100%);
}

.register-card {
  width: 400px;
  padding: 20px 12px;
}

.title {
  text-align: center;
  margin-bottom: 24px;
  color: #303133;
}

.submit {
  width: 100%;
}

.footer {
  margin-top: 16px;
  text-align: center;
  color: #909399;
  font-size: 13px;
}
</style>