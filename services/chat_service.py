from services.client_init import client


class ChatService:
    def __init__(self):
        self.model="qwen-long"
    
    def get_response(self, messages: str) ->str:
        try:
            return client.chat.completions.create(
                model = self.model,
                messages = messages,
                temperature = 0.1,
                stream=True,
                # response_format={"type": "json_object"},
                # stream_options={"include_usage": True}
            )
        except Exception as e:
            raise Exception(f"回答生成失败: {str(e)}")
        
    def get_content(self, completion):
        full_content = ""
        # 非流式输出
        # full_content += completion.choices[0].message.content
        # 流式输出
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                # 拼接输出内容
                full_content += chunk.choices[0].delta.content
                # print(chunk.model_dump())
        return full_content

    # 删除上传的文件
    def delete_file(self, file_id):
        file_object = client.files.delete(file_id)
        print(file_object.model_dump_json())    
    
    