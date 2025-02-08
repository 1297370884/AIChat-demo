<template>
  <div class="input-box">
    <el-input
      v-model="inputMessage"
      placeholder="输入消息..."
      @keyup.enter="sendMessage"
    />
    <el-button type="primary" @click="sendMessage">发送</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue';
import { webSocketServiceKey } from '../services/WebSocketService';
import { MessageSender } from '../services/WebSocketService';

const webSocketService = inject<WebSocketService>(webSocketServiceKey)!;
const inputMessage = ref('');

const sendMessage = () => {
  if (inputMessage.value.trim()) {
    webSocketService.messages.value.push({
      text: inputMessage.value,
      sender: 'user'
    });
    webSocketService.sendMessage(inputMessage.value);
    inputMessage.value = '';
  }
};
</script>

<style scoped>
.input-box {
  position: sticky;
  bottom: 0;
  background: white;
  z-index: 1;
  padding: 10px 0;
  margin-top: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.el-input {
  flex: 1;
  min-width: 0;

}
:deep(.el-input) {
  height: 40px;
  overflow: hidden; /* 防止内容溢出 */
}

.el-button {
  flex-shrink: 0;
  height: 40px;
  padding: 0 20px;
}
</style>
