<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <el-empty description="图像标注模块：C + D 组开发（Bounding Box 目标框选）">
    <template #description>
      <p>任务 ID：{{ route.params.taskId }}</p>
      <p class="tip">本页面由 C + D 同学负责开发，代码位于 src/views/annotate/image/</p>
    </template>
  </el-empty>
</template>

<style scoped>
.tip {
  color: #909399;
  font-size: 13px;
  margin-top: 8px;
}
</style>
