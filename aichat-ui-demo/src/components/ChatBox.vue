<template>
  <div class="chat-box">
    <el-scrollbar class="chat-box__content">
      <template v-for="(message, index) in messages" :key="index">
        <Message :message="message" />
      </template>
      <!-- 显示 AI 回复的累加内容 -->
      <div class="message message--ai" v-if="currentAiMessage">
        <div v-html="renderedMessageText"></div>
      </div>
    </el-scrollbar>
    <div class="chat-box__gradient"></div>
  </div>
</template>

<script setup lang="ts">
import { computed, inject, ref, nextTick, watch } from 'vue';
import { webSocketServiceKey } from '../services/WebSocketService';
import { WebSocketService, MessageSender } from '../services/WebSocketService';
import Message from './Message.vue';
import { marked } from 'marked';

const webSocketService = inject<WebSocketService>(webSocketServiceKey)!;

const messages = computed(() => webSocketService.messages.value);
const currentAiMessage = ref('');

const renderedCurrentMessage = computed(() => {
  return marked.parse(currentAiMessage.value);
});

const renderedMessageText = computed(() => {
  return marked.parse(
    currentAiMessage.value
      .split('')
      .map((c, i) => `<span class="char" style="opacity: ${i < visibleChars.value ? 1 : 0}">${c}</span>`)
      .join('')
  );
});

const visibleChars = ref(0);
watch(currentAiMessage, (newVal) => {
  let count = 0;
  const animate = () => {
    if (count < newVal.length) {
      visibleChars.value = count;
      count++;
      requestAnimationFrame(animate);
    }
  };
  animate();
});
</script>

<style scoped>
.chat-box {
  flex: 1;
  min-height: 0;
  border: 1px solid #ccc;
  margin: 10px 0;
  position: relative;
  display: flex;
  flex-direction: column;
}

.chat-box__content {
  height: 100%;
  padding: 10px;
  border-radius: 4px;
}
.chat-box__gradient {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 20px;
  background: linear-gradient(rgba(255, 255, 255, 0), rgba(255, 255, 255, 1));
  pointer-events: none; /* 防止遮罩影响点击 */
}

.chat-box .el-scrollbar {
  flex: 1;
  min-height: 0; /* 重要：修复滚动容器高度问题 */
}

.el-scrollbar__wrap {
  overflow-x: hidden;
}

.el-scrollbar__view {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  padding-bottom: 30px; /* 增加底部空间 */
  min-height: 100%; /* 强制填满容器 */
}
</style>
