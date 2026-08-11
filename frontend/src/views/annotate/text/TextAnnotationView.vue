<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <el-empty description="文本标注模块：A + B 组开发（NER 实体标注）">
    <template #description>
      <p>任务 ID：{{ route.params.taskId }}</p>
      <p class="tip">本页面由 A + B 同学负责开发，代码位于 src/views/annotate/text/</p>
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
