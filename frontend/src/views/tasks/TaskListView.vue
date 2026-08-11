<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { listTasks, createTask } from '../../api/tasks'
import { listDatasets } from '../../api/datasets'
import type { Task, Dataset } from '../../types'

const router = useRouter()
const tasks = ref<Task[]>([])
const datasets = ref<Dataset[]>([])
const loading = ref(false)
const dialogVisible = ref(false)

const statusMap: Record<string, string> = {
  pending: '待开始',
  in_progress: '进行中',
  done: '已完成',
}

const form = reactive({
  dataset_id: 0 as number,
  name: '',
  type: 'text' as 'text' | 'image',
})

async function load() {
  loading.value = true
  try {
    const data = await listTasks({ page: 1, page_size: 50 })
    tasks.value = data.items
  } finally {
    loading.value = false
  }
}

async function onSubmit() {
  if (!form.name || !form.dataset_id) {
    ElMessage.warning('请填写任务名称并选择数据集')
    return
  }
  await createTask({ ...form })
  ElMessage.success('创建成功')
  dialogVisible.value = false
  form.name = ''
  load()
}

function openDialog() {
  form.dataset_id = 0
  dialogVisible.value = true
}

function onTypeChange(type: 'text' | 'image') {
  form.type = type
  form.dataset_id = 0
}

function enterAnnotation(task: Task) {
  router.push(task.type === 'text' ? `/annotate/text/${task.id}` : `/annotate/image/${task.id}`)
}

onMounted(async () => {
  load()
  const data = await listDatasets({ page: 1, page_size: 50 })
  datasets.value = data.items
})
</script>

<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog">创建标注任务</el-button>
    </div>

    <el-table v-loading="loading" :data="tasks" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="任务名称" />
      <el-table-column prop="type" label="类型" width="100">
        <template #default="{ row }">
          <el-tag :type="row.type === 'text' ? 'success' : 'warning'">
            {{ row.type === 'text' ? '文本' : '图像' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="row.status === 'done' ? 'success' : row.status === 'in_progress' ? 'primary' : 'info'">
            {{ statusMap[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" type="primary" @click="enterAnnotation(row)">进入标注</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="创建标注任务" width="480px">
      <el-form :model="form" label-width="70px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="任务名称" />
        </el-form-item>
        <el-form-item label="类型">
          <el-radio-group :model-value="form.type" @update:model-value="onTypeChange">
            <el-radio value="text">文本</el-radio>
            <el-radio value="image">图像</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="数据集">
          <el-select v-model="form.dataset_id" placeholder="选择数据集" style="width: 100%">
            <el-option
              v-for="d in datasets.filter((d) => d.type === form.type)"
              :key="d.id"
              :label="d.name"
              :value="d.id"
            />
          </el-select>
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
