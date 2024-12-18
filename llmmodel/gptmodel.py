#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 任务类型: python
# ********************************************************************#
# #author:yangfei
# #create time:2024-12-17 11:16:35
# #desc: 使用gpt进行模型的探查
# #开源项目的连接：https://github.com/chatanywhere/GPT_API_free/blob/main/demo.py
# 需要考虑，之后的多用户访问的时候的会话留存问题
# #remind:请在资源引用中添加需要引用的资源
# ********************************************************************#
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPEN_API_KEY"),
    base_url="https://api.chatanywhere.tech/v1"
)


# 非流式响应
def gpt_35_api(messages: list):
    """
    为提供的对话消息创建新的回答
    Args:
        messages (list): 完整的对话消息
    """
    try:
        completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        response_content = completion.choices[0].message.content
        print(f"GPT API 返回: {response_content}")
        return response_content
    except Exception as e:
        print(f"GPT API 调用失败: {e}")
        return None

def gpt_35_api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)"""
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            return chunk.choices[0].delta.content
    return "没有返回内容"

if __name__ == '__main__':
    messages = [{'role': 'user','content': '鲁迅和周树人的关系'},]
    # 非流式调用
    # gpt_35_api(messages)
    # 流式调用
    gpt_35_api_stream(messages)
