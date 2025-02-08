<template>
  <el-container class="app">
    <el-header>
      <h1 class="app__title">AI 聊天室</h1>
    </el-header>
    <el-main>
      <ChatBox />
      <InputBox />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { onMounted, provide } from 'vue';
import { webSocketServiceKey } from './services/WebSocketService';
import ChatBox from './components/ChatBox.vue';
import { WebSocketService } from './services/WebSocketService';
import InputBox from './components/InputBox.vue';

const webSocketService = new WebSocketService();
provide(webSocketServiceKey, webSocketService);

onMounted(() => {
  webSocketService.connect();
});
</script>

<style scoped>
.app {
  max-width: 800px;
  height: calc(100vh - 20px); /* 视口高度减去边距 */
  display: flex;
  flex-direction: column;
  margin: 10px auto; /* 上下边距各10px */
  padding: 0;
}

.el-header {
  flex-shrink: 0; /* 防止header被压缩 */
  text-align: center;
  padding: 20px 0;
}

.app__title {
  margin: 0;
}

:deep(.el-main) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0 !important;
  overflow: hidden; /* 防止内容溢出 */
}
</style>
