<template>

  <div class="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 p-4">
    <div
      v-for="project in state.projects"
      :key="project.id"
      :class="[bg_color_mapping[project.pipeline.status], ' rounded']"
    >
      <div class="relative box-border h-32 p-2">
        <template
          v-if="project.web_url"
        >
          <a
            :href="project.web_url"
            target="_blank"
          >
            {{ project.name }}
          </a>
        </template>
        <template
          v-else
        >
          {{ project.name }}
        </template>
        <div class="absolute cc text-2xl text-gray-50">
          <a
            :href="project.pipeline.web_url"
            target="_blank"
          >
            {{ project.pipeline.ref }}
          </a>
        </div>
        <div class="absolute right-0 bottom-0 p-2">

          {{ format_time(project.last_activity_at) }}
        </div>
        <a
          v-if="project.pipeline.user"
          :href="project.pipeline.user.web_url" target="_blank"
        >
          <div class="inline-flex absolute left-0 bottom-0 p-2">
            <img class="h-8 rounded-full" :src="project.pipeline.user.avatar_url" alt="avatar">
            <span class="leading-8 pl-1.5">{{ project.pipeline.user.name }}</span>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import dayjs from 'dayjs'
import { reactive, ref } from 'vue'
import axios from '../axios/v1'

const state = reactive({
  projects: []
})

const bg_color_mapping = {
  undefined: 'animate-pulse bg-gray-400',
  created: 'bg-gray-400',
  waiting_for_resource: 'bg-gray-400',
  preparing: 'bg-gray-400',
  pending: 'bg-gray-400',
  running: 'animate-pulse bg-gray-400',
  success: 'bg-green-400',
  failed: 'bg-red-400',
  canceled: 'bg-gray-400',
  skipped: 'bg-gray-400',
  manual: 'bg-gray-400',
  scheduled: 'bg-gray-400'
}

const fetch_data = () => {
  axios.get('/projects').then(rs =>  {
    state.projects = rs.data
    state.projects.forEach(item => {
      let pipeline = ref({})
      item['pipeline'] = pipeline
      axios.get(`/projects/${item.id}/latest_pipelines`).then(rs => {
        pipeline.value = rs.data[0]
        axios.get(`/projects/${item.id}/pipelines/${rs.data[0].id}`).then(rs => {
          pipeline.value = rs.data
        })
      })
    })
  })
}

fetch_data()

setInterval(() => {
  fetch_data()
}, 60 * 5 * 1000)

const format_time = (txt) => {
  return dayjs(txt).format('YYYY/MM/DD HH:mm')
}

const intial_upper = (txt) => {
  if (txt) {
    return txt.substr(0, 1).toUpperCase() + txt.substring(1, txt.length)
  }
}

</script>

<style scoped>
.cc {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
</style>
