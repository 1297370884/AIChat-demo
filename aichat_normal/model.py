from openai import OpenAI

class AiChat:
    def __init__(self):
        self.history = [
        {"role": "system",
         "content": "你是 xxx，由 xxx AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。xxx AI 为专有名词，不可翻译成其他语言。"}
    ]

    def chat(self, role="user", content=None):
        if content is None:
            return "没有输入问题，请重新提问"

        client = OpenAI(
            api_key="",  # 模型api接口
            base_url="",  # 模型服务地址
        )

        messages = {
            "role": role,
            "content": content
        }
        self.history.append(messages)

        response = client.chat.completions.create(
            model="",  # 模型名称
            messages=self.history,
            temperature=0.3,
            stream=False
        )

        chat_response = response.choices[0].message.content

        self.history.append(response.choices[0].message)
        return chat_response

    def get_chat_history(self):
        # 返回聊天记录的JSON格式
        return self.history

if __name__ == "__main__":
    chat = AiChat()
    response = chat.chat(content="你好呀")
    print(response)
    response = chat.chat(content="你是谁呀")
    print(response)
    chat_history = chat.get_chat_history()
    print(chat_history)