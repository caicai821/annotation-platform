<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { listDatasets, createDataset } from '../../api/datasets'
import type { Dataset } from '../../types'

const datasets = ref<Dataset[]>([])
const loading = ref(false)
const dialogVisible = ref(false)

const form = reactive({
  name: '',
  type: 'text' as 'text' | 'image',
  description: '',
})

async function load() {
  loading.value = true
  try {
    const data = await listDatasets({ page: 1, page_size: 50 })
    datasets.value = data.items
  } finally {
    loading.value = false
  }
}

async function onSubmit() {
  if (!form.name) {
    ElMessage.warning('请输入数据集名称')
    return
  }
  await createDataset({ ...form })
  ElMessage.success('创建成功')
  dialogVisible.value = false
  form.name = ''
  form.description = ''
  load()
}

onMounted(load)
</script>

<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="dialogVisible = true">新建数据集</el-button>
    </div>

    <el-table v-loading="loading" :data="datasets" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="type" label="类型" width="100">
        <template #default="{ row }">
          <el-tag :type="row.type === 'text' ? 'success' : 'warning'">
            {{ row.type === 'text' ? '文本' : '图像' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
    </el-table>

    <el-dialog v-model="dialogVisible" title="新建数据集" width="480px">
      <el-form :model="form" label-width="70px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="数据集名称" />
        </el-form-item>
        <el-form-item label="类型">
          <el-radio-group v-model="form.type">
            <el-radio value="text">文本</el-radio>
            <el-radio value="image">图像</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmit">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.toolbar {
  margin-bottom: 16px;
}
</style>
