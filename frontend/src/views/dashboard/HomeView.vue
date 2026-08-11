<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const cards = [
  { title: '数据集', desc: '上传文本或图像数据', path: '/datasets' },
  { title: '标注任务', desc: '创建文本 / 图像标注任务', path: '/tasks' },
]
</script>

<template>
  <div>
    <h2 class="welcome">欢迎使用数据标注平台</h2>
    <el-row :gutter="20" class="cards">
      <el-col v-for="c in cards" :key="c.path" :span="8">
        <el-card shadow="hover" class="card" @click="router.push(c.path)">
          <h3>{{ c.title }}</h3>
          <p>{{ c.desc }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.welcome {
  margin-bottom: 24px;
}

.cards {
  max-width: 900px;
}

.card {
  cursor: pointer;
}

.card p {
  color: #909399;
  margin-top: 8px;
}
</style>
