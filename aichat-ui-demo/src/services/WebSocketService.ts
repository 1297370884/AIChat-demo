// WebSocketService.ts
import { InjectionKey } from 'vue';
import { ref, computed} from 'vue';

export interface MessageSender {
  text: string;
  sender: 'user' | 'ai' | 'system';
}

export class WebSocketService {
  private ws: WebSocket | null = null;
  private messageQueue: string[] = [];
  private currentAiMessage = ''; // 非响应式变量
  private aiMessageTimeout: any = null; // 用于检测流式响应结束
  public messages = ref<MessageSender[]>([]);
  public isConnected = ref(false);

  public async connect(): Promise<void> {
    this.ws = new WebSocket('ws://localhost:8000/ws');
    this.ws.onopen = this.onOpen;
    this.ws.onmessage = this.onMessage;
    this.ws.onclose = this.onClose;
    this.ws.onerror = this.onError;
  }

  public sendMessage(message: string): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(message);
    } else {
      this.messageQueue.push(message);
    }
  }

  private onOpen = (): void => {
    this.isConnected.value = true;
    console.log('WebSocket connected');
    this.messageQueue.forEach((msg) => this.ws?.send(msg));
    this.messageQueue = [];
  }

  private onMessage = (event: MessageEvent): void => {
    try {
      const data = JSON.parse(event.data);
      
      switch(data.type) {
        case 'stream_start':
          this.handleStreamStart(data.stream_id);
          break;
        case 'stream_chunk':
          this.handleStreamChunk(data.stream_id, data.content);
          break;
        case 'stream_end':
          this.handleStreamEnd(data.stream_id);
          break;
        case 'system':
          this.messages.value.push({ text: data.content, sender: 'system' });
          break;
        case 'error':
          this.messages.value.push({ text: data.content, sender: 'system' });
          break;
      }
    } catch (error) {
      console.error('消息解析失败:', error);
    }
  }

  private activeStreams: Map<string, {
    buffer: string;
    elementIndex: number;
  }> = new Map();

  private handleStreamStart(streamId: string) {
    // 创建新消息占位
    const newMessage: MessageSender = {
      text: '',
      sender: 'ai'
    };
    this.messages.value.push(newMessage);
    
    this.activeStreams.set(streamId, {
      buffer: '',
      elementIndex: this.messages.value.length - 1
    });
  }

  private handleStreamChunk(streamId: string, content: string) {
    const stream = this.activeStreams.get(streamId);
    if (!stream) return;

    stream.buffer += content;
    
    // 实时更新消息内容（带打字机效果）
    this.updateStreamContent(streamId);
  }

  private updateStreamContent(streamId: string) {
    const stream = this.activeStreams.get(streamId);
    if (!stream) return;

    // 使用动画帧优化渲染
    requestAnimationFrame(() => {
      const messages = [...this.messages.value];
      messages[stream.elementIndex].text = this.applyTypingEffect(stream.buffer);
      this.messages.value = messages;
    });
  }

  private applyTypingEffect(text: string): string {
    // 这里可以添加打字机效果逻辑
    return text; // 暂时直接返回
  }

  private handleStreamEnd(streamId: string) {
    const stream = this.activeStreams.get(streamId);
    if (!stream) return;

    // 最终更新一次内容
    const messages = [...this.messages.value];
    messages[stream.elementIndex].text = stream.buffer;
    this.messages.value = messages;

    this.activeStreams.delete(streamId);
  }

  private onClose = (): void => {
    this.isConnected.value = false;
    console.log('WebSocket closed');
  }

  private onError = (error: Event): void => {
    console.error('WebSocket error:', error);
  }
}

export const webSocketServiceKey: InjectionKey<WebSocketService> = Symbol('WebSocketService');
